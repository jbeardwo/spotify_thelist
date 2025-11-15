# MAKE A BAND CLASS MAKE A CONCERT CLASS
# HANDLE WHEN A BAND IS LISTED TWICE
# Give band class a links attribute to store alt links and handle
import urllib.request
import re


def get_followed_bands():
    return [
        "Matt Braunger",
        "Thundercat",
        "Karen Less",
        "Jerry's Middle Finger",
        "Sister Nancy",
        "Cactus Blossoms",
    ]


def get_followed_concerts(followed_bands):
    list_bands_to_links = get_list_bands()

    for band in followed_bands:
        if band in list_bands_to_links:
            band_concerts = get_band_concerts(band, list_bands_to_links)


def get_list_bands():
    with urllib.request.urlopen("http://www.foopee.com/punk/the-list/") as response:
        main_page = response.read().decode("utf-8")
        # THINK about this: sometimes the same band is listed twice, and you'll get multiple responses from this:
        # you need to take into account both of them since they may have different concerts
        # could even be on a different page!
    list_bands_chunk = re.findall(
        r"Concerts By Band</B><DD>\n(.*?)<P><DT><B>Concerts By Venue", main_page
    )[0]
    list_bands = re.findall(r'<A HREF="([^"]+)">([^<]+)</A>', list_bands_chunk)
    band_to_link = {}
    for link, band in list_bands:
        band_to_link[band] = "http://www.foopee.com/punk/the-list/" + link
    return band_to_link


def get_band_concerts(band, band_to_link):
    with urllib.request.urlopen(band_to_link[band]) as response:
        concerts_page = response.read().decode("utf-8")

    concerts_chunk = re.findall(
        rf"<B>{re.escape(band)}</B></A><UL>\n(.*?)\n</UL>", concerts_page, re.DOTALL
    )[0]

    concerts_raw = concerts_chunk.split("\n")
    concerts = []
    for concert in concerts_raw:
        concerts.push(process_concert(concert))


def process_concert(concert):
    pass


def main():
    followed_bands = get_followed_bands()
    followed_concerts = get_followed_concerts(followed_bands)


main()
