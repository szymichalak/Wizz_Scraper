class Flight:
    def __init__(self, data_dict):
        self.arrivalStation: str = ''
        self.departureDate: str = ''
        self.departureStation: str = ''
        self.priceValue: float = 0.0
        self.priceCurrency: str = ''

        for key, value in data_dict.items():
            if key == 'price':
                self.priceValue = value['amount']
                self.priceCurrency = value['currencyCode']
                continue
            if hasattr(self, key):
                if key == 'departureDate':
                    value = value.split('T')[0]
                setattr(self, key, value)

