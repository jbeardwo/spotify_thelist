from datetime import datetime


class Concert:
    def __init__(
        self, followed_band_name, date, venue, ages, price, time, symbols, notes
    ):
        self.followed_band_name = followed_band_name
        self.date = date
        self.venue = venue
        self.ages = ages
        self.price = price
        self.time = time
        self.symbols = symbols
        self.notes = notes

    def __str__(self) -> str:
        return f"\nBand: {self.followed_band_name}\nDate: {self.date}, Venue: {self.venue}, Ages: {self.ages}, Price: {self.price}, Time: {self.time}, Symbols: {self.symbols}, Notes: {self.notes}"

    def __repr__(self) -> str:
        return self.__str__()


def concert_sort_key(concert):
    today = datetime.now()

    # Parse the date with current year
    date_obj = datetime.strptime(f"{concert.date} {today.year}", "%b %d %Y")

    # If the date is in the past, it must be next year
    if date_obj < today:
        date_obj = datetime.strptime(f"{concert.date} {today.year + 1}", "%b %d %Y")

    # Parse time
    if concert.time:
        time_str = concert.time.split("/")[0]
        try:
            time_obj = datetime.strptime(time_str, "%I%p")
            return (date_obj, time_obj.hour, time_obj.minute)
        except:
            return (date_obj, 0, 0)
    else:
        return (date_obj, 0, 0)
