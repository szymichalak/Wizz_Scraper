import requests
import json

from models.flight import Flight


class WizzRequest:
    def __init__(self):
        self.headers: dict = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8,lt;q=0.6,ru;q=0.4",
        }
        self.api_url: str = 'https://be.wizzair.com/10.41.0/Api/search/timetable'
        self.wizz_url: str = 'https://www.wizzair.com/'
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.response_text: str

        self.outboundFlights = []
        self.returnFlights = []

    def make_request(self, data: dict):
        # self.response = self.session.get(self.wizz_url)
        # self.response = self.session.post(self.api_url, json=data)
        self.response_text = '{"outboundFlights":[{"departureStation":"TIA","arrivalStation":"VIE","departureDate":"2021-07-11T00:00:00","price":{"amount":129.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-11T16:05:00"],"classOfService":"H","hasMacFlight":false},{"departureStation":"TIA","arrivalStation":"VIE","departureDate":"2021-07-12T00:00:00","price":{"amount":129.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-12T16:05:00"],"classOfService":"H","hasMacFlight":false},{"departureStation":"TIA","arrivalStation":"VIE","departureDate":"2021-07-14T00:00:00","price":{"amount":129.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-14T16:05:00"],"classOfService":"H","hasMacFlight":false},{"departureStation":"TIA","arrivalStation":"VIE","departureDate":"2021-07-16T00:00:00","price":{"amount":144.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-16T16:05:00"],"classOfService":"GH","hasMacFlight":false},{"departureStation":"TIA","arrivalStation":"VIE","departureDate":"2021-07-18T00:00:00","price":{"amount":204.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-18T16:05:00"],"classOfService":"FE","hasMacFlight":false},{"departureStation":"TIA","arrivalStation":"VIE","departureDate":"2021-07-19T00:00:00","price":{"amount":159.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-19T16:05:00"],"classOfService":"G","hasMacFlight":false}],"returnFlights":[{"departureStation":"VIE","arrivalStation":"TIA","departureDate":"2021-07-11T00:00:00","price":{"amount":174.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-11T13:45:00"],"classOfService":"GF","hasMacFlight":false},{"departureStation":"VIE","arrivalStation":"TIA","departureDate":"2021-07-12T00:00:00","price":{"amount":189.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-12T13:45:00"],"classOfService":"F","hasMacFlight":false},{"departureStation":"VIE","arrivalStation":"TIA","departureDate":"2021-07-14T00:00:00","price":{"amount":174.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-14T13:45:00"],"classOfService":"GF","hasMacFlight":false},{"departureStation":"VIE","arrivalStation":"TIA","departureDate":"2021-07-16T00:00:00","price":{"amount":174.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-16T13:45:00"],"classOfService":"GF","hasMacFlight":false},{"departureStation":"VIE","arrivalStation":"TIA","departureDate":"2021-07-18T00:00:00","price":{"amount":174.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-18T13:45:00"],"classOfService":"GF","hasMacFlight":false},{"departureStation":"VIE","arrivalStation":"TIA","departureDate":"2021-07-19T00:00:00","price":{"amount":174.99,"currencyCode":"EUR"},"priceType":"price","departureDates":["2021-07-19T13:45:00"],"classOfService":"GF","hasMacFlight":false}],"featureTogglesChanged":true}'

    def parse_response(self):
        response_text = self.response_text
        json_acceptable_string = response_text.replace("'", "\"")
        response_dictionary = json.loads(json_acceptable_string)

        for flight in response_dictionary['outboundFlights']:
            self.outboundFlights.append(Flight(flight))
        for flight in response_dictionary['returnFlights']:
            self.returnFlights.append(Flight(flight))

    def request_and_parse(self, data: dict):
        self.make_request(data)
        self.parse_response()
