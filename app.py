from database.DatabaseProvider import DatabaseProvider
from models.flightSearch import FlightSearch
from models.postData import PostData
from scraper.scraper import Scraper
from wizz_request.dataGenerator import DataGenerator
from wizz_request.wizz_request import WizzRequest

postData = PostData()
postData.adultCount = 0
postData.childCount = 0
postData.infantCount = 0
postData.flightList = [
    FlightSearch("ABC", "XYZ", "2020-07-10", "2021-11-20"),
    FlightSearch("XYZ", "ABC", "2020-07-10", "2021-11-20"),
]

data_07 = {
    "flightList":
        [
            {
                "departureStation": "TIA",
                "arrivalStation": "VIE",
                "from": "2021-07-10",
                "to": "2021-07-20"
            },
            {
                "departureStation": "VIE",
                "arrivalStation": "TIA",
                "from": "2021-07-10",
                "to": "2021-07-20"
            }
        ],
    "priceType": "regular",
    "adultCount": 1,
    "childCount": 0,
    "infantCount": 0
}

# wizz_req = WizzRequest()
# wizz_req.make_request(data_07)
# wizz_req.parse_response()

new_scraper = Scraper()
countries, cities = new_scraper.scrap_routes('VIA')


db_prov = DatabaseProvider()
db_prov.drop_table('countries')
db_prov.create_countries_table()
db_prov.fill_countries(countries)
db_prov.select_table('countries')

