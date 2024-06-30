# projekt-deployment
W tym repozytorium znajduje się projekt z przedmiotu Wdrażanie Modeli Uczenia Maszynowego
# Część modelowa
Plik 'model_ZMUM' zawiera kod służący do załadowania danych, przetworzenia ich oraz stworzenia modelu uczenia maszynowego, a na koniec zapisanie wyników do plików csv. Dokładniejszy opis tego kodu znajduje się w projekcie z Zaawansowanych Modeli Uczenia Maszynowego.
# Część wdrożeniowa
Plik 'projekt-wdrazanie' zawiera kod służący do wizualizacji danych na wykresie przy pomocy szkieletu Streamlit do języka python. Dzięki niemu jest tworzona aplikacji internetowa.
# Jak uruchomić?
W dowolnym środowisku uruchomić (przynajmniej raz) kod z pliku 'model_ZMUM.py', który spowoduje utworzenie/modyfikację plików 'predictions.csv' i 'real.csv' w folderze 'predictions'. W związku z tym proszę nie zmieniać struktury plików w folderze projektu.
Następnie należy uruchomić wiersz poleceń i w katalogu projektu wydać komendę `steamlit run projekt-wdrazanie.py`. To polecenie poskutkuje uruchomieniem aplikacji internetowej.
