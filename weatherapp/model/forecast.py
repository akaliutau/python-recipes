from datetime import date
from .forecast_type import ForecastType

class Forecast:
    def __init__(
            self,
            current_temp,
            location,
            unit,
            description,
            forecast_date=None,
            forecast_type=ForecastType.TODAY):
        self._current_temp = current_temp
        self._location = location
        self._unit = unit
        self._description = description
        self._forecast_type = forecast_type

        if forecast_date is None:
            self.forecast_date = date.today()
        else:
            self._forecast_date = forecast_date

    @property
    def forecast_date(self):
        return self._forecast_date

    @forecast_date.setter
    def forecast_date(self, forecast_date):
        self._forecast_date = forecast_date.strftime("%a %b %d")

    @property
    def current_temp(self):
        return self._current_temp

    @property
    def description(self):
        return self._description

    def __str__(self):
        temperature = None
        offset = ' ' * 4

        return (f'>> {self.forecast_date}\n'
                f'{temperature}'
                f'({self._description})\n')