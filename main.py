import smart_garden
import weerstation
import smart_home
import weather_api
import smart_energy

print('Smart App gestart')

while True:

    print('\n===== SMART APP =====')
    print('1. Weerstation')
    print('2. Smart Home controller')
    print('3. smart energy')
    print('4. Smart Garden')
    print('5. Stoppen')

    keuze = input('Maak een keuze: ')

    if keuze == '1':
        print('\n----- WEERSTATION -----')
        weerstation.weerstation()

    elif keuze == '2':
        print('\n----- SMART HOME CONTROLLER -----')
        smart_home.smart_app_controller('input.txt', 'output.txt')

    elif keuze == '3':
        print('\n----- SMART ENERGY -----')
        smart_energy.smart_energy()

    elif keuze == '4':
        print('\n----- SMART GARDEN -----')
        smart_garden.smart_garden()

    elif keuze == '5':
        print('Programma gestopt')
        break

    else:
        print('Ongeldige keuze')