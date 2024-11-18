import requests
import re


def list_wikipedia_titles(search_query: str, n: int = 20, language: str = "en") -> list[str]:
    base_url = f"https://{language}.wikipedia.org/w/api.php"  # language arg to control what language is used
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_query,
        "format": "json",
        "srlimit": n,
    }

    response = requests.get(base_url, params=params)

    data = response.json()
    titles = [item["title"] for item in data.get("query", {}).get("search", [])]
    return titles


def fetch_wikipedia_text(page_title: str, language: str = "en") -> str | None:
    url = f"https://{language}.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": page_title,
        "rvprop": "content",
        "rvslots": "main",
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for _, page_content in pages.items():
            if "revisions" in page_content:
                text = page_content["revisions"][0]["slots"]["main"]["*"]

                # TEXT CLEANING
                text = re.sub(r"\{\{.*?\}\}", "", text, flags=re.DOTALL)  # double braces
                text = re.sub(r"\{.*?\}", "", text, flags=re.DOTALL)  # remove single braces
                text = re.sub(r"\[\[.*?\|(.*?)\]\]", r"\1", text)  # Keep text
                text = re.sub(r"\[\[.*?\]\]", "", text)  # Remove if no text
                text = re.sub(r"\[http[^\]]+\]", "", text)  # external links
                text = re.sub(r"<.*?>", "", text, flags=re.DOTALL)  # html tags
                text = re.sub(r"File:[^\s]+\s?", "", text, flags=re.IGNORECASE)  # more cleaning
                text = re.sub(r"\s{2,}", " ", text).strip()  # Whitespace

                return text

        return None
    else:
        return None


# Choosing 4 langauges that I like
# titles_pl = list_wikipedia_titles("Gwiezdne Wojny", 50, "pl")
# titles_en = list_wikipedia_titles("Star Wars", 50, "en")
# titles_fr = list_wikipedia_titles("La Guerre des étoiles", 50, "fr")
# titles_ge = list_wikipedia_titles("Star Wars", 50, "ka")
