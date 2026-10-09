import weather_api


def Fahrenheit(temperatuur):
    Fahrenheit = 32 + 1.8 * temperatuur
    return Fahrenheit

def gevoelstemperatuur(temperatuur, windsnelheid, luchtvochtigheid):
    gevoelstemperatuur = temperatuur - luchtvochtigheid / 100 * windsnelheid
    return gevoelstemperatuur

def weerrapport(temperatuur, windsnelheid, luchtvochtigheid):
    gevoel = gevoelstemperatuur(temperatuur, windsnelheid, luchtvochtigheid)

    if gevoel < 0 and windsnelheid > 10:
        return "Het is heel koud en het stormt! Verwarming helemaal aan!"

    elif gevoel < 0 and windsnelheid <= 10:
        return "Het is behoorlijk koud! Verwarming aan op de benedenverdieping!"

    elif 0 <= gevoel < 10 and windsnelheid > 12:
        return "Het is best koud en het waait; verwarming aan en roosters dicht!"

    elif 0 <= gevoel < 10 and windsnelheid <= 12:
        return "Het is een beetje koud, elektrische kachel op de benedenverdieping aan!"

    elif 10 <= gevoel < 22:
        return "Heerlijk weer, niet te koud of te warm."

    else:
        return "Warm! Airco aan!"


def weerstation():
    totaal_temp = 0
    aantal_dagen = 0

    while True:
        locatie = input('Voer een stad of dorp in: ')

        if weather_api.zoek_locatie(locatie) is not None:
            break

        print('Ongeldige stad of dorp')

    while True:
        datum = input('Voer een datum in (DD-MM-JJJJ), of druk op Enter om te stoppen: ')

        if datum == "":
            print('Weerstation gestopt.')
            break

        try:
            jaar, maand, dag = datum.split('-')
            datum_api = f'{dag}-{maand}-{jaar}'

            temperatuur, luchtvochtigheid, windsnelheid, neerslag = weather_api.weergegevens_ophalen(locatie, datum_api)

            if None in (temperatuur, luchtvochtigheid, windsnelheid, neerslag):
                print('Niet alle weergegevens zijn bschikbaar.')
                continue

            while True:
                try:
                    aantal_mensen = int(input('Hoeveel mensen zijn er thuis? '))
                    if aantal_mensen <0:
                        print('Voer een positied geheel getal of 0 in.')
                        continue
                    break

                except ValueError:
                    print('Ongeldige invoer. Voer een geheel getal in.')

            while True:
                    try:
                        temp_setpoint = float(input('Gewenste binnentemperatuur: '))
                        break

                    except ValueError:
                        print('Ongeldige invoer. Voer een geheel getal in.')


            print(f"\nWeerrapport voor {locatie} op {datum}")
            print(f"Temperatuur: {temperatuur:.1f} °C")
            print(f"Windsnelheid: {windsnelheid:.2f} m/s")
            print(f"Luchtvochtigheid: {luchtvochtigheid}%")
            print(f"Neerslag: {neerslag} mm")

            gevoel = gevoelstemperatuur(temperatuur, windsnelheid, luchtvochtigheid)

            print(f"Geschatte gevoelstemperatuur: {gevoel:.1f} °C")

            rapport = weerrapport(temperatuur, windsnelheid, luchtvochtigheid)

            if rapport is not None:
                print(rapport)

            aantal_dagen = aantal_dagen + 1
            totaal_temp = totaal_temp + temperatuur
            gemiddelde = round(totaal_temp / aantal_dagen, 2)

            print(f'Gem. temperatuur tot nu toe is {gemiddelde} °C')

            jaar, maand, dag = datum.split('-')
            datum_opslaan = f'{dag}-{maand}-{jaar}'

            with open("input.txt", "a") as bestand:
                bestand.write(f"\n{datum} {aantal_mensen} {temp_setpoint} {temperatuur} {neerslag}")

            print("Weergegevens toegevoegd aan input.txt.")
            print("=======================================\n")

        except (ValueError, KeyError, IndexError, TypeError):
            print('Datum is ongeldig of er zijn geen weergegevens beschikbaar.')
