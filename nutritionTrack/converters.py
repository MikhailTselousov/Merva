from datetime import datetime

class YearMonthDayConverter:
    regex = r"\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])" 

    def to_python(self, value):
        return datetime.fromisoformat(value)

    def to_url(self, value):
        return str(value)