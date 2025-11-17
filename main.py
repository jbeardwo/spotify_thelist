# MAKE A BAND CLASS MAKE A CONCERT CLASS
# HANDLE WHEN A BAND IS LISTED TWICE
# Give band class a links attribute to store alt links and handle
import re
import requests

from band import Band
from concert import Concert, concert_sort_key
from spotify_actions import get_followed_artists


def get_followed_bands():
    return [
        "George Lucas Talk Show",
        "Gary Numan",
        "California Honeydrops",
        "Matt Braunger",
        "Thundercat",
        "Karen Less",
        "Jerry's Middle Finger",
        "Sister Nancy",
        "Cactus Blossoms",
    ]


def init_followed_concerts(followed_band_names, list_bands_by_name):
    followed_bands = []
    for followed_band_name in followed_band_names:
        if followed_band_name in list_bands_by_name:
            list_bands_by_name[followed_band_name].init_concerts()
            followed_bands.append(list_bands_by_name[followed_band_name])
    return followed_bands


def get_list_bands():
    main_page = requests.get("http://www.foopee.com/punk/the-list/").text

    list_bands_chunk = re.findall(
        r"Concerts By Band</B><DD>\n(.*?)<P><DT><B>Concerts By Venue", main_page
    )[0]
    list_bands_raw = re.findall(r'<A HREF="([^"]+)">([^<]+)</A>', list_bands_chunk)
    list_bands_by_name = {}
    for link, band_name in list_bands_raw:
        link = "http://www.foopee.com/punk/the-list/" + link
        # We do this because I've seen them have a band listed twice before
        # Although rare it's likely possible for them to spill over into another page.
        # This is why we handle links as a set
        if band_name not in list_bands_by_name:
            band = Band(band_name)
            list_bands_by_name[band_name] = band
        list_bands_by_name[band_name].links.add(link)

    return list_bands_by_name


def main():
    followed_band_names = get_followed_artists()
    list_bands_by_name = get_list_bands()
    followed_bands_in_list = init_followed_concerts(
        followed_band_names, list_bands_by_name
    )
    followed_concerts = []
    for band in followed_bands_in_list:
        for concert in band.concerts:
            followed_concerts.append(concert)
    followed_concerts.sort(key=concert_sort_key)
    print(
        "Symbol Key:\n",
        """   *    recommendable shows			a/a  all ages
    $    will probably sell out			@    pit warning
    ^    under 21 must buy drink tickets	#    no ins/outs\n""",
    )
    print("Shows in the Bay Area for bands you follow on Spotify:")
    for followed_concert in followed_concerts:
        print(followed_concert)


main()
