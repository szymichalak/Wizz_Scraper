class FlightSearch:
    def __init__(self, source, destination, from_date, to_date):
        self.departureStation: str = source
        self.arrivalStation: str = destination
        self.from_date: str = from_date
        self.to_date: str = to_date

    def to_dictionary(self):
        return {
                "departureStation": self.departureStation,
                "arrivalStation": self.arrivalStation,
                "from": self.from_date,
                "to": self.to_date
            }
