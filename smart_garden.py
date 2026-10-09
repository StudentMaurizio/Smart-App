from datetime import datetime


def plant_toevoegen():
    while True:
        plant = input('Welke plant wil je toevoegen? (Enter om te stoppen): ').strip()

        if plant == '':
            break

        try:
            water = float(input('Hoeveel liter water per dag heeft de plant nodig? '))

            if water < 0:
                print('Voer een positief getal in.')
                continue

        except ValueError:
            print('Ongeldige invoer. Voer een getal in.')
            continue

        while True:
            print('\n1. Dit is een kleine plant')
            print('2. Dit is een middelgrote plant')
            print('3. Dit is een grote plant')
            print('4. Dit is een boom')

            grootte = input('Hoe groot is de plant? ')

            if grootte in ('1', '2', '3', '4'):
                break

            print('Ongeldige keuze.')

        bestand = open('planten.txt', 'a')
        bestand.write(f'\n{plant};{water};{grootte}')
        bestand.close()

        print('Plant toegevoegd!\n')


def water_bekijken():
    bewatering = False

    while True:
        datum = input('Voer een datum in (DD-MM-JJJJ), of druk op Enter om te stoppen: ')

        if datum == '':
            break

        try:
            datetime.strptime(datum, '%d-%m-%Y')
        except ValueError:
            print('Ongeldige datum.')
            continue

        bestand = open('input.txt', 'r')
        regels = bestand.readlines()
        bestand.close()

        gevonden = False

        for regel in regels[1:]:
            gegevens = regel.split()

            if gegevens[0] == datum:
                neerslag = float(gegevens[4])
                gevonden = True
                break

        if not gevonden:
            print('Geen weergegevens voor deze datum.')
            continue

        print(f'\nNeerslag: {neerslag} mm')

        bestand = open('planten.txt', 'r')
        regels = bestand.readlines()
        bestand.close()

        for regel in regels[1:]:
            plant, water, grootte = regel.strip().split(';')

            water = float(water)

            if grootte == '1':
                oppervlakte = 0.1
            elif grootte == '2':
                oppervlakte = 0.25
            elif grootte == '3':
                oppervlakte = 0.75
            else:
                oppervlakte = 2.0

            regenwater = neerslag * oppervlakte
            nodig = max(0, water - regenwater)

            if nodig > 0.0:
                bewatering = True

            print(f'De {plant} heeft nog {nodig:.2f} liter water nodig.')

        if bewatering:
            print('\nAutomatische bewatering: AAN\n')
        else:
            print('Automatische bewatering: UIT')




def smart_garden():
    while True:
        print('1. Plant toevoegen')
        print('2. Hoeveelheid water bekijken')
        print('3. Stoppen')

        keuze = input('Maak een keuze: ')

        if keuze == '1':
            plant_toevoegen()
        elif keuze == '2':
            water_bekijken()
        elif keuze == '3':
            break
        else:
            print('Ongeldige keuze.')
