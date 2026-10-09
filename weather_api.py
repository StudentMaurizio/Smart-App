import requests
from datetime import date, datetime, timedelta


def zoek_locatie(naam):
    uitzonderingen = {'den haag': (52.0705, 4.3007), 'den bosch': (51.6978, 5.3037)}

    if naam.strip().lower() in uitzonderingen:
        return uitzonderingen[naam.strip().lower()]

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={naam}&count=10&countryCode=NL"

    antwoord = requests.get(url)
    data = antwoord.json()

    if 'results' not in data:
        return

    locatie = data['results'][0]
    latitude = locatie['latitude']
    longitude = locatie['longitude']

    return latitude, longitude



def weergegevens_ophalen(naam, datum):
    gekozen_datum = datetime.strptime(datum, '%Y-%m-%d').date()
    vandaag = date.today()

    if not date(2020, 1, 1) <= gekozen_datum <= vandaag + timedelta(days=10):
        raise ValueError

    if gekozen_datum < vandaag - timedelta(days=5):
        api = "archive-api.open-meteo.com/v1/archive"
        url_extra =''
    else:
        api = "api.open-meteo.com/v1/forecast"
        url_extra = ''

    latitude, longitude = zoek_locatie(naam)

    url = (f'https://{api}?latitude={latitude}&longitude={longitude}'
           f'&daily=temperature_2m_mean,relative_humidity_2m_mean,wind_speed_10m_mean,'
           f'precipitation_sum&start_date={datum}&end_date={datum}&timezone=Europe%2FAmsterdam') + url_extra

    antwoord = requests.get(url)
    data = antwoord.json()

    temperatuur = data['daily']['temperature_2m_mean'][0]
    luchtvochtigheid = data['daily']['relative_humidity_2m_mean'][0]
    windsnelheid = data['daily']['wind_speed_10m_mean'][0]
    neerslag = data['daily']['precipitation_sum'][0]
    windsnelheid = windsnelheid / 3.6

    return temperatuur, luchtvochtigheid, windsnelheid, neerslag
