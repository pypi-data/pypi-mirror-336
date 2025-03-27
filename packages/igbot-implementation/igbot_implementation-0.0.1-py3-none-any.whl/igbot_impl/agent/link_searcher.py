from igbot_impl.igbot_impl.agent import Agent
import json

from igbot_base.igbot_base.agent_response import AgentResponse
from igbot_impl.igbot_impl.llm import Model
from igbot_impl.igbot_impl.llm.one_use_llm import OneUseLlm
from igbot_impl.igbot_impl.llm import ResponseFormat
from igbot_base.igbot_base.prompt_template import Prompt

category_system_prompt = """
Jesteś najlepszym asystentem do spraw przypisywania zgodnej kategorii do zadanego pytania. 
Otrzymasz zapytanie od klienta który odwiedza naszą stonę i rozmawia z asystentem AI.
Twoim zadaniem jest dowiedzenie się, czy do danego pytania klienta warto wysłać link do strony internetowej.
Skategoryzuj każde zapytanie do kategorii linku. Podaj wynik w formacie JSON z kluczem: category.

Jeśli pytanie jest zbyt ogólne, nie pasuje do żadnej kategorii, 
lub jest to pytanie dla którego wysłanie linku nie przyniesie żadnej korzyści dla klienta, zwróć wynik w formacie JSON z kluczem category i pustą tablicą.
przykład:

Użytkownik: Dzień dobry!
Asystent: {"category": []}

Jeśli pytanie pasuje do jednej kategorii zwróć wynik w formacie JSON z kluczem category i z tablicą string z jedną wartością.
przykład

Użytkownik: Czy prowadzicie serwis maszyn?
Asystent: {"category": ["serwis"]}

Jeśli pytanie pasuje do wielu kategorii zwróć wynik w formacie JSON z kluczem category i z tablicą string z wieloma wartościami, maksymalnie dwoma.
przykład

Użytkownik: Czy prowadzicie serwis maszyn albo szkolenia?
Asystent: {"category": ["serwis", "szkolenia"]}

Pamiętaj, zwracaj tylko kategorie z podanej listy!

Oto dostępne kategorie:

{{categories}}

Pamiętaj! Wybierz tylko kategorię z podanej listy!

Pytanie klienta jest następujące:
"""

find_link_system_prompt = """
Jesteś najlepszym asystentem do spraw wyszukiwania linku który najbardziej pasuje do zadanego pytania przez klienta.
Na podstawie pytania klienta oraz podanej listy linków wybierz i zwróć link który najbardziej pasuje do zadanego pytania.
JSON o kluczu "links" i wartości w postaci tablicy stringów.

Jeśli z podanej listy linków nie ma linku który pasuje do danego pytania zwróć obiekt JSON o kluczu "links" i pustą tablicę.
przykład: 

Linki: ["google.pl", "innylink.pl"]
Kategorie: ["serwis maszyn", "kontakt"]
Użytkownik: Dzień dobry!
Asystent: {"links": []}

Jeśli w podanej liście jest link który pasuje do jednej kategorii zwróć wynik w formacie JSON z kluczem "links" i z tablicą string z jedną wartością.
przykład:

Linki: ["serwis.pl", "innylink.pl"]
Kategorie: ["serwis maszyn", "kontakt"]
Użytkownik: Czy prowadzicie serwis maszyn?
Asystent: {"links": ["serwis.pl"]}

Jeśli pytanie pasuje do wielu kategorii zwróć wynik w formacie JSON z kluczem links i z tablicą string z wieloma wartościami, maksymalnie dwoma.
przykład:

Linki: ["serwis.pl", "innylink.pl", "kontakt.pl"]
Kategorie: ["serwis maszyn", "kontakt"]
Użytkownik: Czy prowadzicie serwis maszyn jeśli tak to mogę prosić o kontakt?
Asystent: {"links": ["serwis.pl", "kontakt.pl"]}

Pamiętaj: 
- zwracaj tylko linki z podanej listy!
- zwracaj tylko jeśli link pasuje do kategorii i pytania!
- zwracaj maksymalnie po jednym linku do każdej kategorii!

Oto dostępna lista linków:
{{links}}

Pamiętaj! Wybierz tylko link z podanej listy!

Pytanie klienta jest następujące:
"""

get_links_answer_system_prompt = """
Jesteś najlepszym asystentem do spraw zachęcania klienta do odwiedzenia strony za pomocą podanych linków.

Na podstawie pytania klienta oraz podanej listy linków stwórz wiadomość zachęcającą do ich odwiedzenia, gdzie klient
będzie mógł dowiedzieć się więcej informacji.
Przykład:

Linki: ["serwis.pl", "kontakt.pl"]
Użytkownik: Czy prowadzicie serwis maszyn? jeśli tak to proszę o kontakt
Asystent: Strona z kontaktem do firmy znajduje się tutaj: https://kontakt.pl. A jeśli chcesz dowiedzieć się wiecej o naszym serwisie, odwiedź https://serwis.pl

Oto dostępna lista linków:
{{links}}

Nie odpowiadaj na zadane pytanie. Po prostu zaproś klienta do odwiedzenia strony do której prowadzi link.
Pamiętaj! Wybierz tylko link z podanej listy!

Pytanie klienta jest następujące:
"""

find_category_prompt = Prompt(category_system_prompt, ["categories"])
find_link_prompt = Prompt(find_link_system_prompt, ["links"])
get_link_answer_prompt = Prompt(get_links_answer_system_prompt, ["links"])


class CategoryLinkSearcherAgent(Agent):

    def __init__(self,
                 agent_id,
                 llm_model: Model,
                 categories: list,
                 links_for_category_fn):
        self.__id = agent_id
        self.__llm_find_categories = OneUseLlm("find_categories", llm_model, 0.0,
                                               find_category_prompt, ResponseFormat.JSON_OBJECT.value)
        self.__llm_find_links = OneUseLlm("find_links", llm_model, 0.0,
                                          find_link_prompt, ResponseFormat.JSON_OBJECT.value)
        self.__llm_get_answer = OneUseLlm("get_links_answer", llm_model, 0.7,
                                          get_link_answer_prompt, None)
        self.__categories = categories
        self.__links_for_category_fn = links_for_category_fn

    def invoke(self, query) -> AgentResponse:
        categories = self._find_category(query)
        print(" ".join(categories))
        links_arr = self.__links_for_category_fn(categories)
        links = self._find_links(query, links_arr)
        if len(links) == 0:
            return AgentResponse.no_content()
        print(' '.join(links))
        answer = self.__llm_get_answer.call(query, {"links": links})
        if not answer.__contains__("https://") or answer.__contains__("serwis.pl") or answer.__contains__("kontakt.pl"):
            return AgentResponse.no_content()

        return AgentResponse.success(answer)

    def _find_category(self, query):
        categories = "\n".join(f"- {category}" for category in self.__categories)
        categories_json = self.__llm_find_categories.call(query, {"categories": categories})
        return json.loads(categories_json)["category"]

    def _find_links(self, query, links_arr):
        links = "\n".join(f"- {link}" for link in links_arr)
        links_json = self.__llm_find_links.call(query, {"links": links})
        return json.loads(links_json)["links"]
