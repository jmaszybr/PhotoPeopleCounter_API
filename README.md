# PhotoPeopleCounter_API - Aplikacja do Detekcji Twarzy i Zliczania Osób
 Projekt został opracowany w ramach modułu "Technologie chmurowe" na studiach podyplomowych "Uczenie Maszynowe i Data Science". W repozytorium dostępna jest wersja API. W drugim repozytorium (PhotoPeopleCounter) dostępna jest wersja projektu oparta na frameworku Flask.
 
#### Autor: Joanna Maszybrocka

## Opis
Aplikacja, napisana jest w języku Python, wykorzystuje klasyfikator kaskadowy Haar z biblioteki OpenCV do identyfikacji twarzy i zliczania osób na zdjęciach. Użytkownik ma możliwość przesyłania zdjęć na trzy różne sposoby:

### 1. Analiza Obrazu Testowego
Endpoint: `/analyze_test`

- Użytkownicy mogą wypróbować działanie aplikacji bez konieczności przesyłania własnych zdjęć.
- Aplikacja używa zdefiniowanego obrazu testowego,
- Aplikacja przeprowadza analizę, identyfikuje twarze i zwraca zliczoną liczbę osób.
- Zapewnia również obraz z zaznaczonymi twarzami i obraz oryginalny.

### 2. Przesyłanie Obrazów
Endpoint: `/analyze_upload`

- Użytkownicy mogą przesyłać własne zdjęcia bezpośrednio przez stronę.
- Po przesłaniu zdjęcia, aplikacja przeprowadza analizę, identyfikuje twarze i zwraca zliczoną liczbę osób.
- Zapewnia również obraz z zaznaczonymi twarzami i obraz oryginalny.

### 3. Analiza Obrazów z URL
Endpoint: `/analyze_url`

- Umożliwia podanie URL obrazu do analizy.
- Po przesłaniu zdjęcia, aplikacja przeprowadza analizę, identyfikuje twarze i zwraca zliczoną liczbę osób.
- Zapewnia również obraz z zaznaczonymi twarzami i obraz oryginalny.

## Wymagania
- Python 3.x
- OpenCV


