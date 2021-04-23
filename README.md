# Django ORM example

Tento repozitá prezentuje fungovanie ORM architektonického vzoru na príklade SQLAlchemy ORM.

Príklad je postavený na dátovom modeli podľa repozitára
[fiit-orm-django-example](https://github.com/Sibyx/fiit-orm-django-example).

Príklady sa nachádzajú v súbore `app.py`.

Projekt používa [poetry](https://python-poetry.org/) ako balíčkovací systém. Prihlasovacie údaje sa čítajú z env
premennej POSTGRES_CONNECTION. Kompletná inštalácia ne Linuxe, môže vyzerať napríklad takto:

```shell
# Stiahnutie projekty
git clone https://github.com/Sibyx/fiit-orm-sqlalchemy-example.git orm_example
cd orm_example

# Vytvorenie virtuálneho prostredia a instalacia zavislosti
python -m venv venv
source venv/bin/activate
poetry install

# Vytvorenie konfiguracie
export POSTGRES_CONNECTION="postgresql://postgres@localhost:5432/orm_example"

# Spustenie príkladov
flask example
```

---
S ❤️ FIIT STU
