def aantal_dagen(inputFile):
    try:
        aantal_dagen = open(inputFile, 'r')

    except FileNotFoundError:
        print('Fout: het bestand bestaat niet.')
        return -1

    bestand = aantal_dagen.readlines()
    aantal_regels = 0

    for regels in bestand:
        aantal_regels = aantal_regels + 1

    aantal_regels = aantal_regels - 1
    aantal_dagen.close()
    return aantal_regels


def auto_bereken(inputFile, outputFile):
    try:
        lezen = open(inputFile, 'r')

    except FileNotFoundError:
        print('Fout: het bestand bestaat niet.')
        return
    regels = lezen.readlines()
    lezen.close()

    toevoegen = open(outputFile, 'w')

    for regel in regels[1:]:
        datum, personen, temperatuur_binnen, temperatuur_buiten, neerslag = regel.strip().split(' ')

        temperatuur_verschil = float(temperatuur_binnen) - float(temperatuur_buiten)

        if temperatuur_verschil < 10:
            CV_ketel = 0

        elif 10 <= temperatuur_verschil < 20:
            CV_ketel = 50

        else:
            CV_ketel = 100

        ventilatiestand = int(personen) + 1
        if ventilatiestand > 4:
            ventilatiestand = 4

        if float(neerslag) >= 3:
            bewatering = False
        else:
            bewatering = True

        toevoegen.write(f'{datum};{CV_ketel};{ventilatiestand};{bewatering}\n')

    toevoegen.close()
    print('De actuatoren zijn automatisch berekend en opgeslagen.')


def overwrite_settings(outputFile):

    try:
        lezen = open(outputFile, 'r')

    except FileNotFoundError:
        print('Fout: het uitvoerbestand bestaat nog niet. bereken eerst de actuatoren.')
        return

    regels = lezen.readlines()
    lezen.close()
    datum_invoer = input('Welke datum wil je aanpassen? ')
    datum_gevonden = False

    for index, regel in enumerate(regels):
        datum, CV_ketel, ventilatiestand, bewatering = regel.strip().split(';')

        if datum_invoer == datum:
            datum_gevonden = True
            print('1. CV-ketel\n2. Ventilatie\n3. Bewatering')

            try:
                invoer_systeem = int(input('Welk systeem wil je aanpassen? '))

            except ValueError:
                return -3

            if invoer_systeem == 1:

                try:
                    invoer_CV_ketel = int(input('Voer de nieuwe waarde voor de CV-ketel in (0 t/m 100): '))

                except ValueError:
                    return -3

                if 0 <= invoer_CV_ketel <= 100:
                    CV_ketel = invoer_CV_ketel

                else:
                    print('Ongeldige waarde. De CV-ketel moet tussen 0 en 100 liggen.')
                    return None

            elif invoer_systeem == 2:

                try:
                    invoer_ventilatiestand = int(input('Voer de nieuwe ventilatiestand in (0 t/m 4): '))

                except ValueError:
                    return -3

                if 0 <= invoer_ventilatiestand <= 4:
                    ventilatiestand = invoer_ventilatiestand

                else:
                    print('Ongeldige waarde. De ventilatiestand moet tussen 0 en 4 liggen.')
                    return None

            elif invoer_systeem == 3:

                try:
                    invoer_bewatering = int(input('Voer 0 (uit) of 1 (aan) in voor de bewatering: '))

                except ValueError:
                    return -3

                if invoer_bewatering == 0:
                    bewatering = False

                elif invoer_bewatering == 1:
                    bewatering = True

                else:
                    print('ongeldige waarde. kies 0 voor uit of 1 voor aan.')
                    return None

            else:
                print ('Ongeldig systeem. Kies 1, 2 of 3.')
                return None

            nieuwe_regel = (f'{datum};{CV_ketel};{ventilatiestand};{bewatering}\n')
            regels[index] = nieuwe_regel
            break

    if datum_gevonden == False:
        return -1

    schrijven = open(outputFile, 'w')
    schrijven.writelines(regels)
    schrijven.close()
    return 0


def smart_app_controller(inputFile, outputFile):
    while True:
        print('1. Aantal dagen weergeven')
        print('2. Actuatoren automatisch berekenen')
        print('3. Een waarde overschrijven')
        print('4. Stoppen')

        keuze = input('Maak een keuze: ')

        if keuze == '1':
            aantal = aantal_dagen(inputFile)

            if aantal != -1:
                print(f'Er zijn {aantal} dagen aanwezig.')

        elif keuze == '2':
            auto_bereken(inputFile, outputFile)

        elif keuze == '3':
            resultaat = overwrite_settings(outputFile)

            if resultaat == 0:
                print('De waarde is succesvol aangepast.')
            elif resultaat == -1:
                print('De datum kon niet worden gevonden.')
            elif resultaat == -3:
                print('De ingevoerde keuze of waarde is ongeldig.')

        elif keuze == '4':
            print('Programma gestopt.')
            break

        else:
            print('Ongeldige keuze. Kies 1, 2, 3 of 4.')
