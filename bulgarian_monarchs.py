# Именник на българските владетели

def add_king(kings, name, start_year, end_year):
    if name not in kings:
        kings[name] = (start_year, end_year)
        return 'Monarch added successfully.'
    return 'Monarch already exists.'

def find_king_by_year(kings, year):
    for name, (start_year, end_year) in kings.values():
        if start_year <= int(year) <= end_year:
            return f'{name} has governed in {year}'
    return 'Bulgaria had had no such monarch in this period.'

def find_king_by_name(kings, name):
    if name in kings.keys():
        start_year, end_year = kings[name]
        return f'{name} has governed from {start_year} to {end_year}'
    return 'Bulgaria had had no such monarch with this name.'

def print_menu():
    menu = '''
    Task Manager Menu:
    1. Find the Bulgarian monarch by his year of government.
    2. Find the Bulgarian monarch by his name.
    3. Add a monarch if you found an omit.
    4. Exiting...
    '''
    print(menu)

def main():
    while True:
        print_menu()
        choice = input('Enter your choice: ')
        if choice == '1':
            year = input('Type an year from 145 to 1946 to see the Bulgarian monarch : ')
            result = find_king_by_year(kings, year)
            print(result)
        elif choice == '2':
            name = input('Type a name to search for the Bulgarian monarch : ')
            result = find_king_by_name(kings, name)
            print(result)
        elif choice == '3':
            name = input("Enter the name of the monarch: ")
            start_year = int(input("Enter the start year of the reign: "))
            end_year = int(input("Enter the end year of the reign: "))
            result = add_king(kings, name, start_year, end_year)
            print(result)
        elif choice == '4':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please try again.')


kings = {
    # Прабългарски владетели
    'Кан Авитохол, от рода Дуло': (145, 145),
    'Кан Ирник, от рода Дуло': (437, 437),
    'Кан Давид, от рода Дуло': (440, 440),
    'Кан Астрахан, от рода Дуло': (450, 450),
    'Кан Монолит, от рода Дуло': (460, 460 ),
    'Кан Сандил, от рода Дуло': (558, 558),
    'Кан Заберган, от рода Дуло': (570, 570),
    'Хан Ювиги Кубрат, от рода Дуло': (584, 642),

    # Първо българско царство - Столица Плиска
    'Велик Хан Аспарух, от рода Дуло, трети син на кан Кубрат': (681, 700),
    'Велик Хан Тервел, от рода Дуло, син на Аспарух': (700, 721),
    'Велик Хан Кормисош, от рода Вокил': (721, 738),
    'Велик Хан Севар, от рода Дуло': (738, 754),
    'Велик Хан Винех, от рода Укил': (754, 760),
    'Велик Хан Телец, от рода Угаин': (760, 763),
    'Велик Хан Умор, от рода Укил': (766, 766),
    'Велик Хан Токту, от рода Дуло': (766, 767),
    'Велик Хан Паган, от рода Дуло': (767, 768),
    'Велик Хан Телериг': (768, 777),
    'Велик Хан Кардам': (777, 802),
    'Велик Хан Крум': (802, 814),
    'Велик Хан Омуртаг, от рода Дуло,син на Крум': (814, 831),
    'Велик Хан Маламир, от рода Дуло, най-малък син на Омуртаг': (831, 836),
    'Велик Хан Персиан, племенник на Маламир': (836, 852),
    'Хан Княз Борис I Михаил, син на Пресиян': (852, 889),
    'Княз Владимир, първороден син на Борис I': (889, 893),

    # Първо българско царство - Столица Велики Преслав
    'Цар Симеон I': (893, 927),
    'Цар Петър I, син на Симеон': (927, 970),
    'Цар Борис II, син на цар Петър': (970, 970),

    # Първо българско царство - Столица Охрид
    'Цар Роман, втори син на цар Петър': (971, 991),
    'Цар Самуил, най-малък син на комит Никола': (991, 1014),
    'Цар Гаврил Радомир, първороден син на Самуил': (1014, 1015),
    'Цар Иван Владислав, син на Арон': (1015, 1018),
    'Византийско владичество': (1018, 1185),

    # Второ българско царство - Велико Търново
    'Цар Теодор-Петър II (Делян), брат Асен': (1185, 1187),
    'Цар Асен I': (1187, 1196),
    'Цар Теодор-Петър II (Делян), брат Асен': (1196, 1197),
    'Цар Калоян, получава титлата крал от папа Инокентий III': (1197, 1207),
    'Цар Борил, сестрин син на Асеновци': (1207, 1218),
    'Цар Иван Асен II, син на цар Асен I': (1218, 1241),
    'Цар Коломан I Асен, син на Иван Асен II': (1241, 1246),
    'Цар Михаил II Асен, син на Иван Асен II от брака му с Ирина Комнина': (1246, 1256),
    'Цар Коломан II': (1256, 1256 + 1),
    'Цар Мицо Асен, зет на Иван Асен II': (1256, 1257),
    'Цар Константин Асен, болярин от Скопие': (1257, 1277),
    'Цар Ивайло, завзема престола от цар Константин Тих': (1277, 1279),
    'Цар Иван Асен III, внук на Иван Асен II': (1279, 1280),
    'Цар Георги I Тертер, от кумански произход. Стратег на крепостта Червен': (1280, 1292),
    'Цар Смилец, поставен от хан Ногай': (1292, 1298),
    'Узурпатор Чака, син на хан Ногай и зет на цар Георги Тертер I': (1299, 1299),
    'Цар Теодор-Светослав Тертер, син на Георги Тертет I': (1300, 1321),
    'Цар Георги II Тертер': (1321, 1323),
    'Цар Михаил III Шишман, видински деспот': (1323, 1330),
    'Цар Иван Стефан': (1330, 1331),
    'Цар Иван Александър I, деспот от Ловеч, син на деспот Срацимир': (1331, 1371),

    # Второ българско царство - Столица Видин
    'Цар Иван Шишман': (1371, 1393),
    'Цар Страцимир': (1371, 1369),
    'Османско владичество': (1396, 1878),

    # Трето българско царство - Столица София
    'Княз Александър II Батемберг': (1879, 1887),
    'Цар Фердинанд I': (1887, 1918),
    'Цар Борис III': (1918, 1943),
    'Цар Симеон II': (1943, 1946),
}

if __name__ == '__main__':
    main()