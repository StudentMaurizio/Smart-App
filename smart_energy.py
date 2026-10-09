import matplotlib.pyplot as plt
from datetime import datetime


def bereken_energie():
    energieprijs = 0.30

    bestand = open('output.txt', 'r')
    uitvoer = open('energie.txt', 'w')
    uitvoer.write('date CV_energie ventilatie_energie watering_energie totale_energie kosten\n')

    for regel in bestand:
        datum, cv, ventilatie, bewatering = regel.strip().split(';')

        cv_energie = int(cv) / 100 * 10
        ventilatie_energie = int(ventilatie) * 0.5
        bewatering_energie = 1 if bewatering == 'True' else 0

        totaal = round(cv_energie + ventilatie_energie + bewatering_energie, 2)
        kosten = round(totaal * energieprijs, 2)

        uitvoer.write(f'{datum} {cv_energie} {ventilatie_energie} {bewatering_energie} {totaal} {kosten}\n')

    bestand.close()
    uitvoer.close()


def kosten_per_dag():
    while True:
        datum = input('Voer een datum in (DD-MM-JJJJ), of druk op Enter om te stoppen: ')

        if datum == '':
            break

        try:
            datetime.strptime(datum, '%d-%m-%Y')
        except ValueError:
            print('Ongeldige datum.')
            continue

        bestand = open('energie.txt', 'r')
        regels = bestand.readlines()
        bestand.close()
        gevonden = False

        for regel in regels [1:]:
            dag, cv, ventilatie, bewatering, totaal, kosten = regel.split()

            if dag == datum:
                print(f'\n1. Energieverbruik per onderdeel:')
                print(f'CV-ketel: {cv} kWh')
                print(f'Ventilatie: {ventilatie} kWh')
                print(f'Bewatering: {bewatering} kWh')
                print(f'\n2. Totaal energieverbruik: {totaal} kWh')
                print(f'3. Totale kosten: €{kosten}\n')

                if float(totaal) > 15:
                    print('WAARSCHUWING: Hoog energieverbruik!')

                gevonden = True
                break

        bestand.close()

        if not gevonden:
            print('Geen gegevens voor deze datum.')


def toon_grafiek():
    datums = []
    verbruik = []
    kosten = []

    bestand = open('energie.txt', 'r')
    regels = bestand.readlines()
    bestand.close()

    for regel in regels[1:]:
        datum, cv, ventilatie, bewatering, totaal, prijs = regel.split()
        datums.append(datum)
        verbruik.append(float(totaal))
        kosten.append(float(prijs))

    bestand.close()

    plt.plot(datums, verbruik, marker='o', label='Verbruik (kWh)')
    plt.plot(datums, kosten, marker='o', label='Kosten (€)')
    plt.xlabel('Datum')
    plt.ylabel('Waarde')
    plt.title('Smart Energy')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()


def smart_energy():
    bereken_energie()

    while True:
        print('1. Energieverbruik en kosten per datum')
        print('2. Grafiek bekijken')
        print('3. Stoppen')

        keuze = input('Maak een keuze: ')

        if keuze == '1':
            kosten_per_dag()
        elif keuze == '2':
            toon_grafiek()
        elif keuze == '3':
            break
        else:
            print('Ongeldige keuze.')