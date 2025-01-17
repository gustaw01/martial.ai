
# Martial.AI

Projekt ma na celu wykonanie systemu do oceny plagiatu w tekscie zadanym przez użytkownika. 
Na podstawie tekstu obliczane są liczbowe reprezentacje zdań które są następnie porównywane z reprezentacjami zawartymi w bazie danych.
Zaletą zastosowanego podejścia jest możliwość oceny plagiatu poprzez tłumaczenie tekstu w innym języku.
Liczbowe reprezentacje zdań zawierają informacje o znaczeniu tekstu bez względu na język tekstu.
Wyniki oceny plagiatu są wyświetlane w interfejsie użytkownika napisanym w języku JavaScript z użyciem framework React.
Komunikacja między interfejsem użytkownika z 

## Backend

### Algorytm

#### Reprezentacje zdań
**Reprezentacje liczbowe słów** - znane również jako osadzanie słów, to technika stosowana w przetwarzaniu języka naturalnego, szczególnie w dużych modelach językowych. 
Polega ona na przedstawianiu słów za pomocą wektorów liczbowych, w których słowa o zbliżonym znaczeniu są odwzorowywane jako wektory znajdujące się blisko siebie w wielowymiarowej przestrzeni wektorowej.
Dzięki temu możliwe jest przestwienie różnic semantycznych między wyrazami w sposób zrozumiały dla modeli komputerowych. <br><br>
W tym projekcie korzystamy z reprezentacji całych zdań w tekscie przekazanym przez użytkownika. 
Zdanie jest osadzane za pomocą komercyjnego API oferowanego przez OpenAI, odpowiedzią z tego API jest wektor o dlugości 1536 liczb zmiennoprzecinkowych z zakresu pomiędzy -1 a 1. 

#### Schemat i zasada działania

![Schemat działania martial.AI](proces.drawio.png "Schemat działania martial.AI")

1. Użytkownik umiesza dokument w formie pdf, docx lub tekst poprze interfejs
2. Tekst jest dzielony na zdania i obliczane są reprezentacje zdań za pomocą API OpenAI
3. Otrzymane reprezentacje są porównywane z reprezentacjami zawartymi w bazie danych
4. Baza danych zwraca k najbliższych zdań dla każdego zdania
5. Na podstawie zwróconych zdań obliczane jest podobieństwo między dokumentami z bazy danych a reprezentacjami tekstu użytkownika
6. Wynik jest przekazywany do interfesu użytkownika

### Użyte technologie
![Schemat działania martial.AI](rozwiazanie.png "Schemat działania martial.AI")
* Python
    * fastapi - biblioteka używana do stworzenia interfesu API w serwerze webowym 
    * nltk - Natual Language Toolkit; paczka umożliwiająca obróbkę języka naturalnego
    * psycopg2 - biblioteka umożliwiająca połączenie się z bazą danych
* Postgresql
    * pgvector - rozszerzenie umożliwiające przechowywanie 
* API OpenAI
    * Używany do uzyskania liczbowych reprezentacji słów

#### Funkcje zawarte w kodzie
* **find_k_nearest** <br>
Funkcja find_k_nearest wyszukuje K najbliższych wektorów w bazie danych względem podanego wektora, wykorzystując metrykę kosinusową.
Sprawdza poprawność długości i typu wektora, a opcjonalnie umożliwia wykluczenie wyników w określonym języku. Zapytanie SQL sortuje wyniki według odległości kosinusowej, zwracając informacje o tytułach dokumentów, językach, zdaniach, indeksach oraz odległościach kosinusowych od zadanego wektora. 

* **create_embeddings** <br>
Funkcja przyjmuje tekst, język, nazwę modelu oraz klienta OpenAI.
Dzieli tekst na zdania za pomocą nltk.sent_tokenize, dopasowując tokenizację do podanego języka.
Wywołuje API OpenAI do wygenerowania reprezentacji dla każdego zdania.
W przypadku błędu zwraca None, natomiast przy sukcesie zwraca listę wektorów (reprezentacji).
Zaimplementowana również z obsługą wielowątkowości pozwalając na równoległe przetwarzanie partii zdań.
Tekst jest dzielony na partie (batch) po 8 zdań, a każda partia przetwarzana jest w osobnym wątku.Wyniki są zbierane i sortowane według kolejności oryginalnych zdań, aby zachować poprawność kolejności wektorów.
* **blast** <br>
Funkcja służy do analizy podobieństwa zdań w dokumentach za pomocą reprezentacji (embeddings), metryki kosinusowej i danych przechowywanych w bazie PostgreSQL.
Porównuje osadzenia zdań dokumentu docelowego (target_embeddings) z osadzeniami zdań pobranymi z bazy danych (document_data).
Dla zdań o podobieństwie powyżej zadanego progu (threshold) wyszukuje sekwencje dopasowanych zdań w określonych granicach (parametry max_forward i max_backward).
Funkcja zwraca listę sekwencji zawierających szczegóły dopasowania: identyfikatory zdań, ich treść, indeks w dokumencie oraz wartość podobieństwa.
Umożliwia ro porównanie zawartości różnych dokumentów na podstawie ich podobieństwa semantycznego.

* **run_algorithm**

### Serwer webowy

* Endpoint /embeddings_assessment

## Frontend

## Testy