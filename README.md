# Fumetsu

Strona dla grup fansubberskich, z możliwością dodawania serii, odcinków i odtwarzaczy, ogłoszeń, podpisów pod seriami oraz napisów.

## O stronie

Stronę, początkowo używaną właśnie w grupie subberskiej, postanowiłem otworzyć i zrobić z niej łatwy w instalacji template dla potencjalnie innych grup.
Serie i odcinki dodaje się najlepiej przez Rest API podpięte pod stronę, które podane dane, uzupełnione anilistem, dodaje do bazy danych.
Strona posiada również system rejestracji i logowania, co umożliwia użytkownikom zostawianie komentarzy pod odcinkami/seriami jak i customizowanie profilu.
Stronę można, a nawet zaleca się, pozmieniać pod własne potrzeby, co oznacza np. zmianę logo lub ztweakowanie domyślnego motywu. 

## Setup strony na Dockerze

### Wymagania

Strona jest przygotowana pod Dockera, więc pójdzie na każdym systemie, na którym będzie pobrany.
Polecam pobrać [Docker Desktop](https://docs.docker.com/compose/install/) z oficjalnej strony, wtedy też łatwiej będzie odpalać później stronę.
Oczywiście można też normalnie z command line pobrać dockera i docker-compose i też będzie git.

### Instalacja

1. Sklonuj i pobierz repo.

```bash
git clone https://github.com/ccandour/fumetsu-website.git
cd fumetsu-website
```

2. Podmień placeholdery.

- część pliku `./django_site/.env`, oprócz konfiguracji postgressa
- configi http i https w folderze `./nginx`, tam gdzie jest `example.com`
- w `docker-compose.yml` w komendzie certbota trzeba zamienić `example.com` na swoją domenę, dla której certbot zrobi certyfikat
- (opcjonalnie) w reszcie plików strony są linki do facebooka, patronite itd., można tam podlinkować swoje, te placeholdery mają zawsze 'example' w linkach

3. Zbuduj docker image strony (to powinno chwilę potrwać).

```bash
docker compose build
```

4. Uruchom containery (to -d na końcu detatchuje proces).

```bash
docker compose up -d
```

## Setup lokalnej strony poza Dockerem

1. Sklonuj i pobierz repo.

```bash
git clone https://github.com/ccandour/fumetsu-website.git
cd fumetsu-website
```
2. Zainstaluj Postgresql i najnowszego Pythona.
Jest na ten temat pełno tutoriali w internecie, każdy będzie git,
ważne by nazwa stworzonej bazy danych, użytkownik i hasło do postgresa zgadzały się później z tymi w .env.

   
2. Podmień placeholdery.

- w pliku `./django_site/.env` zamień `DB_HOST` na 'localhost' i resztę ustawień bazy danych tak by pasowały do twoich z lokalnego serwera.
- w pliku `./django_site/.env` zmień `DEBUG` na True
- reszta podmian placeholderów (example) jest opcjonalna, strona lokalnie z nimi też się odpali, ale można popodmieniać

3. Stwórz i aktywuj środowisko wirtualne.

```bash
python3 -m venv .venv
# na windowsie python zamiast python3
```
```bash
source .venv/bin/activate
# na windowsie .venv\Scripts\activate
```

4. Zaktualizuj package manager pythona

```bash
python3 -m pip install --upgrade pip
python3 -m pip --version
# na windowsie python zamiast python3
```

5. Pobierz dependencies

```bash
python3 -m pip install -r requirements.txt
# na windowsie python zamiast python3
```

6. Przygotuj bazę danych

```bash
cd django_site
```
```bash
python3 manage.py makemigrations
# na windowsie python zamiast python3
```
Powinny zrobić się migracje, jeśli wyskoczy 'no changes detected' albo coś to spróbuj tym:
```bash
python3 manage.py makemigrations core
python3 manage.py makemigrations users
# na windowsie python zamiast python3
```

Na koniec importujemy defaultowe tagi do serii:
```bash
python3 manage.py loaddata initial_data.json
# na windowsie python zamiast python3
```

7. Uruchomienie strony
Bedąc nadal w naszym środowisku (.venv) i w directory ./django_site uruchamiamy:
```bash
python3 manage.py runserver
# na windowsie python zamiast python3
```

## Problemy

Jeśli są jakieś problemy z instalacją czy czymś to śmiało pisać na Discordzie - @ccandour i to ogarniemy.
Btw pod /admin na stronie jest panel admina w Django, gdzie można edytować w razie czego odcinki, serie itd.
Żeby się tam dostać trzeba stworzyć superusera w Django, który jeż też potrzebny do API requestów:
```bash
python3 manage.py createsuperuser
# na windowsie python zamiast python3
```
Jeśli używasz Dockera to (chyba):
```bash
docker exec -it django-website python3 manage.py createsuperuser
```

## Contributowanie

Jeśli z dobrego serca postanowisz dodać/usprawnić coś na stronie, 
otwórz pull requesta ze swojego forka i tam się wszystko ogarnie.
A i jeśli są jakieś problemy czy coś, Issues czekają na zapełnienie :)
Co do commitów, fajnie jakby były podobnie nazywane co [Convencional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

## Licencja

Projekt jest licencjowany pod licencją AGPL, więcej w LICENCE.md.

## Podziękowania

Shout out dla Kuro i Kacperka za oryginalną stronę, która zainspirowała ten rewrite.
