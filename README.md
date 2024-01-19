# ProjectMGMT
## Aplikacja bazodanowa do zarządzania projektami

### Installation
Pobierz plik ```requirements.txt``` i w wierszu poleceń zainstaluj potrzebne moduły poleceniem:

```
pip install -r requirements.txt
```

Głównym plikiem jest ```main.py```.
Pliki html znajdują się w folderze ```templates```.
Obrazy znajdują się w folderze ```imgs```.

### Przygotowanie połączenia z bazą danych
Aby aplikacja działała poprawnie uzupełnij w pliku ```help.py``` w dwóch miejscach (funkcje  `create_async_connection()` oraz `create_connection()`) dane:

```
dbname = ''
user = ''
password = ''
host = ''
port = ''
```

### Dokumetacja
Dokumentacja i kod SQL do utworzenia bazy danych znajdują się w folderze ```Dokumentacja```.


Autor: Daria Kokot
