import re

from weatherapp.core import Request
from weatherapp.core import Unit
from weatherapp.core import UnitConverter
from weatherapp.core import Mapper

from bs4 import BeautifulSoup
from bs4 import Tag

from weatherapp.model import Forecast
from weatherapp.model import ForecastType


def _get_additional_info(content):
    data = tuple(item.td.span.get_text()
                 for item in content.table.tbody.children)
    return data[:2]


def _get_data(container, search_items):
    scraped_data = {}

    for key, attr in search_items.items():
        result = container.find(attr[0], attrs=attr[1])
        data = None if result is None else result.contents
        if data is not None:
            scraped_data[key] = data

    return scraped_data


def _parse(container, criteria):
    results = [_get_data(item, criteria)
               for item in container]

    return [result for result in results if result]


def _parse_list_forecast(content, args):
    # criteria by which the querying of DOM will be performed
    criteria = {
        'location': ['span', {'data-testid': re.compile('^PresentationName.*')}],
        'unit': ['span', {'class': re.compile('^LanguageSelector--unitDisplay.*')}],
    }

    aggregate_criteria = {
        'table': ['div', {'data-testid': re.compile('^DetailsSummary.*')}],
    }

    item_criteria = {
        'temperature': ['span', {'data-testid': re.compile('^TemperatureValue.*')}],
        'wind': ['span', {'data-testid': re.compile('^Wind.*')}],
        'phase': ['span', {'class': re.compile('^DetailsSummary--extendedData.*')}],
        'date': ['h2', {'data-testid': re.compile('^daypartName.*')}],
    }

    parsed = BeautifulSoup(content, 'html.parser')

    result = dict()
    for (key, attr) in criteria.items():
        found = parsed.find(attr[0], attrs=attr[1])
        result[key] = found.contents

    table = aggregate_criteria['table']
    forecast_data = parsed.findAll(table[0], attrs=table[1])
    all_days = _parse(forecast_data, item_criteria)

    for day in all_days:
        for key, val in result.items():
            day[key] = val

    return all_days

# all parsers to be used with this app must implement 4 main methods:
# ForecastType.TODAY
# ForecastType.TENDAYS

class WeatherComParser:

    def __init__(self):
        self._forecast = {
            ForecastType.TODAY: self._today_forecast,
            ForecastType.TENDAYS: self._five_and_ten_days_forecast,
        }
        # default forecast type
        self._forecast_type = ForecastType.TODAY

        self._base_url = 'http://weather.com/weather/{forecast}/l/{area}'
        self._request = Request(self._base_url)

        self._temp_regex = re.compile('([0-9]+)d{,2}([0-9]+)')
        self._only_digits_regex = re.compile('[0-9]+')

        self._unit_converter = UnitConverter(Unit.FAHRENHEIT)

    def _clear_str_number(self, str_number):
        result = self._only_digits_regex.match(str_number)
        return '--' if result is None else result.group()

    def _prepare_data(self, results, args):
        global high_temp, low_temp
        forecast_result = []

        self._unit_converter.dest_unit = args.unit

        for item in results:

            day_forecast = Forecast(
                self._unit_converter.convert(item['temperature']),
                item['location'],
                item['unit'],
                item['phase'],
                forecast_type=self._forecast_type)
            forecast_result.append(day_forecast)

        return forecast_result

    def _today_forecast(self, args):
        # criteria by which the querying of DOM will be performed
        criteria = {
            'location': ['h1', {'class': re.compile('^CurrentConditions--location.*')}],
            'unit': ['span', {'class': re.compile('^LanguageSelector--unitDisplay.*')}],
            'temperature': ['span', {'data-testid': re.compile('^TemperatureValue.*')}],
            'phase': ['div', {'data-testid': re.compile('^wxPhrase.*')}],
        }

        content = self._request.fetch_data(args.forecast_option.value,
                                           args.area_code)
        print(f'retrieved raw data {len(content)} bytes')
        parsed = BeautifulSoup(content, 'html.parser')

        result = dict()
        for (key, attr) in criteria.items():
            found = parsed.find(attr[0], attrs=attr[1])

            result[key] = found.contents

        weather_conditions = result

        if len(weather_conditions) < 1:
            raise Exception('Could not parse weather forecast for today.')

        return [weather_conditions]

    def _five_and_ten_days_forecast(self, args):
        content = self._request.fetch_data(args.forecast_option.value, args.area_code)
        results = _parse_list_forecast(content, args)
        return results

    def run(self, args):
        self._forecast_type = args.forecast_option
        forecast_function = self._forecast[args.forecast_option]
        print(f'using sub type: {forecast_function.__name__}')
        return forecast_function(args)
