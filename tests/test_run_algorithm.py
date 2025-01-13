import time
import pytest
import sys
import dotenv
import os
from test_data import TEST_TEXT
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../algorithm")))
dotenv.load_dotenv()

from run_algorithm import run_algorithm


def test_run_algorithm():

    plagiarised_text = """
        'Równocześnie młodzieniec kuszony jest przez zło (uosabiane przez mroczną postać Dartha Sidiousa), które odwołuje się do jego ambicji i podsyca je, aby ostatecznie zawrzeć „szatański pakt” – poddanie się mu za cenę zaspokojenia własnych pragnień i posiadania wszechmocy, która okazuje się złudna.'
        Dobro i Zło są w ''Gwiezdnych wojnach'' przedstawione jednoznacznie, jednak nie oznacza to, że opisywany świat jest czarno-biały: nawet Jedi (w tym Mistrz Yoda) mają swoje słabości.
        Nawet Vader nie jest w istocie złblast(text_embeddings, sentences_from_db, threshold=0.89)y, jest zwyczajnym człowiekiem, który uległ powabom zła.
        ''Gwiezdne wojny'' to opowieść o sile tkwiącej w miłości: to, czego nie mogli dokonać najwięksi i najpotężniejsi Rycerze Jedi – pokonanie Sithów – dokonuje się dzięki miłości syna do ojca oraz ojca do syna.
    """

    plagiarised_text_translated = """
        « En même temps, le jeune homme est tenté par le mal (personnifié par la sombre figure de Dark Sidious), qui fait appel à ses ambitions et les alimente, de sorte qu'il conclut finalement un « pacte satanique » - soumission à lui au prix de satisfaire ses propres désirs et d'avoir la toute-puissance, ce qui s'avère être illusoire.'
        Le bien et le mal sont clairement présentés dans Star Wars, mais cela ne signifie pas que le monde décrit est noir et blanc : même les Jedi (y compris Maître Yoda) ont leurs faiblesses.
        Même Vador n’est pas fondamentalement mauvais, il est juste un homme ordinaire qui est tombé dans les pièges du mal.
        « Star Wars » est une histoire sur le pouvoir de l'amour : ce que les plus grands et les plus puissants chevaliers Jedi n'ont pas pu faire - vaincre les Sith - est accompli grâce à l'amour d'un fils pour son père et d'un père pour son fils.
    """

    original_text = """
        Star Trek” to kultowy fenomen science fiction, który rozpoczął się jako serial telewizyjny, po raz pierwszy wyemitowany w Stanach Zjednoczonych 8 września 1966 roku. W ciągu dekad marka rozwinęła się w ogromny wszechświat pełen seriali, filmów, książek i innych mediów.
        Dotychczas stworzono 8 seriali, w tym jeden animowany. Wśród zamkniętych serii znajduje się 6 seriali, które łącznie obejmują 726 odcinków, podzielonych na 30 sezonów.
    """

    plagiarisms = run_algorithm(plagiarised_text, "pl") # Ten tekst jest w bazie danych, powinien być wykryty jako plagiat
    assert plagiarisms["rating"] > 0.9 and plagiarisms["rating_other_lang"] < 0.2

    plagiarisms_t = run_algorithm(plagiarised_text_translated, "fr") # Ten tekst jest w bazie danych, ale w innym języku
    assert plagiarisms_t["rating"] < 0.2 and plagiarisms_t["rating_other_lang"] > 0.6

    plagiarisms_ot = run_algorithm(original_text, "pl") # tego tekstu nie ma w bazie danych
    assert plagiarisms_ot["rating"] < 0.2 and plagiarisms_ot["rating"] < 0.2
