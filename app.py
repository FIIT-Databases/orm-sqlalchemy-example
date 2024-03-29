import os
from datetime import datetime, date
from enum import Enum

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "POSTGRES_CONNECTION", os.getenv('POSTGRES_CONNECTION')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

role_permissions = db.Table(
    'role_permissions',
    db.Model.metadata,
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)


class Permission(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    deleted_at = db.Column(db.DateTime(), nullable=True)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), unique=True)
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    deleted_at = db.Column(db.DateTime(), nullable=True)

    government_members = relationship("GovernmentMember", back_populates="role")


class Party(db.Model):
    __tablename__ = 'parties'

    class PartyEnum(Enum):
        NAZI = 'nazi'
        LIBERAL = 'liberals'
        POPULIST = 'populists'
        COMMUNIST = 'communists'
        CONSERVATIVES = 'conservatives'
        SOCIALISTS = 'socialists'
        NATIONALISTS = 'nationalists'
        DEMOCRATS = 'democrats'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=200), unique=True, nullable=False)
    color = db.Column(db.String(length=200), nullable=True)
    type = db.Column(db.Enum(PartyEnum), nullable=True)
    founded_at = db.Column(db.Date(), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    deleted_at = db.Column(db.DateTime(), nullable=True)

    government_members = relationship("GovernmentMember", back_populates="party")


class Government(db.Model):
    __tablename__ = 'governments'

    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime(), nullable=False)
    end_at = db.Column(db.DateTime(), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    deleted_at = db.Column(db.DateTime(), nullable=True)

    government_members = relationship("GovernmentMember", back_populates="government")


class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50))
    surname = db.Column(db.String(length=50))
    born_at = db.Column(db.Date(), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    deleted_at = db.Column(db.DateTime(), nullable=True)

    government_members = relationship("GovernmentMember", back_populates="member")


class GovernmentMember(db.Model):
    __tablename__ = 'government_members'

    id = db.Column(db.Integer, primary_key=True)

    government_id = db.Column(db.Integer, db.ForeignKey('governments.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))

    government = relationship("Government", back_populates="government_members")
    member = relationship("Member", back_populates="government_members")
    role = relationship("Role", back_populates="government_members")
    party = relationship("Party", back_populates="government_members")

    created_at = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)
    deleted_at = db.Column(db.DateTime(), nullable=True)


@click.command(name='example')
@with_appcontext
def example():
    # 1. Select all users in table members using model Member
    result = Member.query.all()

    # 2. Return exactly one member (if possible) with surname `Poliačik`
    result = Member.query.filter(Member.surname == "Poliačik").one()

    # 3. Select first record from table parties
    result = Party.query.first()

    # 4. Select the youngest member of parliament ever
    result = Member.query.order_by(Member.born_at.desc()).first()

    # 5. Create party with name: `Friends of Douglas Adams`
    db.session.add(Party(name="Friends of Douglas Adams", color="unicorn-blue"))
    db.session.commit()

    # 6. Is there a party with name `Združenie robotníkov Slovenska`?
    print(Party.query.where(Party.name == "Združenie robotníkov Slovenska").exists())
    print(db.session.query(Party.query.where(Party.name == "Združenie robotníkov Slovenska").exists()).scalar())

    # 7. The longest party name
    result = Party.query.order_by(func.length(Party.name).desc()).first()
    print(result)

    # 8. Most experienced member
    result = Member.query.join(GovernmentMember).filter(
        GovernmentMember.member_id == Member.id
    ).group_by(Member.id).order_by(
        func.count(GovernmentMember.id).desc()
    ).first()
    assert result.surname == "Fico"

    # 9. Select all parties where type is SOCIALISTS or LIBERAL
    result = Party.query.filter(
        (Party.type == Party.PartyEnum.LIBERAL) | (Party.type == Party.PartyEnum.SOCIALISTS)
    ).all()
    print(result)

    # 10. The best tourist
    result = Member.query.join(GovernmentMember).filter(
        GovernmentMember.member_id == Member.id
    ).group_by(Member.id).order_by(
        func.count(func.distinct(GovernmentMember.party_id)).desc()
    ).first()
    print(result)

    # 11. Disco people
    result = Member.query.filter(
        (Member.born_at >= date(1960, 1, 1)) & (Member.born_at <= date(1969, 12, 31))
    ).all()


app.cli.add_command(example)

if __name__ == '__main__':
    app.run()
