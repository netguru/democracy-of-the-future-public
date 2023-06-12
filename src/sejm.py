import requests
from typing import TypedDict


class Law(TypedDict):
    title: str
    entry_into_force: int
    pdf_url: str
    address: str


def pdf_url(eli: str) -> str:
    return f"http://api.sejm.gov.pl/eli/acts/{eli}/text.pdf"


def fetch_laws(limit: int = 10, offset: int = 0) -> list[Law]:
    # fetch latest 10 laws
    laws = requests.get(
        f"http://api.sejm.gov.pl/eli/acts/search?limit={limit}&offset={offset}&type=Ustawa"
    )
    return [
        {
            "title": x["title"],
            "pdf_url": pdf_url(x["ELI"]),
            "entry_into_force": x["entryIntoForce"],
            "address": x["address"],
        }
        for x in laws.json()["items"]
    ]
