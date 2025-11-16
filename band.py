import requests
import re
from concert import Concert


class Band:
    def __init__(self, name):
        self.name = name
        self.links = set()
        self.concerts = []

    def __str__(self) -> str:
        return f"Name: {self.name},\nLinks: {self.links},\nConcerts:\n{self.concerts}"

    def __eq__(self, other) -> bool:
        if isinstance(other, Band):
            return self.name == other.name
        return False

    def init_concerts(self):
        for link in self.links:
            concerts_page = requests.get(link).text
            concerts_chunk = re.findall(
                rf"<B>{re.escape(self.name)}</B></A><UL>\n(.*?)\n</UL>",
                concerts_page,
                re.DOTALL,
            )[0]
            concerts_raw = concerts_chunk.split("\n")
            for concert in concerts_raw:
                # go from this array of strings to array of concert objects concert_raw_to_concert(concert string) call Concert() from within.

                self.concerts.append(concert_from_raw(concert, self.name))


def strip_html_tags(text):
    return re.sub(r"<[^>]+>", "", text)


def concert_from_raw(raw_concert, followed_band_name):
    text = strip_html_tags(raw_concert)
    result = {
        "date": None,
        "venue": None,
        "ages": None,
        "price": None,
        "time": None,
        "symbols": "",
        "notes": "",
    }

    date_match = re.match(r"(^\w+ \d+)", text)
    if date_match:
        result["date"] = date_match.group(1)
        text = text[len(result["date"]) :].strip()

    notes_match = re.search(r"\(([^)]+)\)\s*$", text)
    if notes_match:
        result["notes"] = notes_match.group(1)
        text = text[: notes_match.start()].strip()

    symbols_match = re.search(r"([@#$^])+\s*$", text)
    if symbols_match:
        result["symbols"] = symbols_match.group(1)
        text = text[: symbols_match.start()].strip()

    time_patterns = [
        r"\b(\d+(?::\d{2})?[ap]m(?:/\d+(?::\d{2})?[ap]m)?(?:\s+and\s+\d+(?::\d{2})?[ap]m(?:/\d+(?::\d{2})?[ap]m)?)?)\s*$",
        r"\b(\d+(?::\d{2})?[ap]m\s+til\s+\d+(?::\d{2})?[ap]m)\s*$",
        r"\b(noon(?:\s+til\s+\d+(?::\d{2})?[ap]m)?)\s*$",
    ]

    for pattern in time_patterns:
        time_match = re.search(pattern, text)
        if time_match:
            result["time"] = time_match.group(1)
            text = text[: time_match.start()].strip()
            break

    price_patterns = [
        r"\$\d+(?:\.\d+)?(?:\+)?(?:\s*\([^)]+\))?(?:\s*/\s*\$?\d+(?:\.\d+)?)*",  # Require $ sign
        r"\b(free|donation)\b",
        r"\$?\d+(?:\.\d+)?-\d+(?:\.\d+)?\s+sliding\s+scale",
    ]

    for pattern in price_patterns:
        price_match = re.search(pattern, text, re.IGNORECASE)
        if price_match:
            result["price"] = price_match.group(0)
            text = text[: price_match.start()].strip()
            break

    age_patterns = [r"\b(\d+\+(?:\s*\([^)]+\))?)", r"\b(a/a)", r"(\?/\?)"]

    for pattern in age_patterns:
        age_match = re.search(pattern, text)
        if age_match:
            result["ages"] = age_match.group(1)
            text = text[: age_match.start()].strip()
            break

    result["venue"] = text

    return Concert(
        followed_band_name,
        result["date"],
        result["venue"],
        result["ages"],
        result["price"],
        result["time"],
        result["symbols"],
        result["notes"],
    )
