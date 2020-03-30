from datetime import datetime


class TimeConverter:
    def __init__(self):
        self.short_format = "%Y-%m-%d"
        self.long_format = "%Y-%m-%d_%H-%M"

    def date_to_str(self, date_in, length):
        if length == "short":
            return datetime.strftime(date_in, self.short_format)
        elif length == "long":
            return datetime.strftime(date_in, self.long_format)
        else:
            return None

    def str_to_date(self, str_in, length):
        if length == "short":
            return datetime.strptime(str_in, self.short_format)
        elif length == "long":
            return datetime.strptime(str_in, self.long_format)
        else:
            return None
