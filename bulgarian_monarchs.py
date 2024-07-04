# Naming directory of Bulgarian rulers

def add_monarch(monarchs, name, start_year, end_year):
    if (start_year, end_year) in monarchs:
        return f'A monarch {name} already exists for this period.'
    monarchs[(start_year, end_year)] = name
    return f'Monarch {name} added for the period {start_year}-{end_year}.'


def find_monarch_by_year(monarchs, year):
    year = int(year)
    for (start, end), name in monarchs.items():
        if start <= year <= end:
            return f'The monarch in {start} to {end} was {name}.'
    return 'Bulgaria had had no such monarch with this name.'


def find_monarch_by_name(monarchs, name):
    results = [f'In {start} to {end} has governed {monarch_name}' for (start, end), monarch_name in monarchs.items() if
               name in monarch_name]
    if results:
        return '\n'.join(results)
    return 'Bulgaria had had no such monarch with this name.'


def find_kingdom_capital(capitals, year):
    year = int(year)
    for (start, end), capital in capitals.items():
        if start <= year <= end:
            return f'In {start} to {end} Bulgaria was governed in {capital}.'
    return f'There is no capital found for this year.'


def print_menu():
    menu = '''
    Task Manager Menu:
    1. Find the Bulgarian monarch by his year of government.
    2. Find the Bulgarian monarch by his name.
    3. Add a monarch if you found an omit.
    4. FInd the capital of Bulgarian Kingdom by given year.
    5. Exiting...
    '''
    print(menu)


def main():
    while True:
        print_menu()
        choice = input('Enter your choice: ')
        if choice == '1':
            year = input('Type an year from 145 to 1946 to see the Bulgarian monarch : ')
            result = find_monarch_by_year(monarchs, year)
            print(result)
        elif choice == '2':
            name = input('Type a name to search for the Bulgarian monarch : ')
            result = find_monarch_by_name(monarchs, name)
            print(result)
        elif choice == '3':
            name = input('Enter the name of the monarch : ')
            start_year = int(input('Enter the start year of the government : '))
            end_year = int(input('Enter the end year of the government : '))
            result = add_monarch(monarchs, name, start_year, end_year)
            print(result)
        elif choice == '4':
            year = input('Type a year from 145 to 1946 to find the Bulgarian Kingdom capital : ')
            result = find_kingdom_capital(capitals, year)
            print(result)
        elif choice == '5':
            print('Exiting...')
            break
        else:
            print('Invalid choice. Please try again.')


capitals = {
    (145, 642): 'Proto-Bulgarian rulers, There is no exact capital',
    (681, 893): 'First Bulgarian Kingdom - capital Плиска',
    (893, 970): 'First Bulgarian Kingdom - capital Велики Преслав',
    (971, 1018): 'First Bulgarian Kingdom - capital Охрид',
    (1018, 1185): 'a Byzantine dominion. There is no capital at this period',
    (1185, 1371): 'Second Bulgarian kingdom - capital Велико Търново',
    (1371, 1396): 'Second Bulgarian kingdom - capital Видин',
    (1396, 1878): 'a Ottoman Empire. There is no capital at this period',
    (1879, 1946): 'Third Bulgarian kingdom - capital София'
}

monarchs = {
    # Proto-Bulgarian rulers
    (145, 145): 'Кан Авитохол, от рода Дуло',
    (437, 437): 'Кан Ирник, от рода Дуло',
    (440, 440): 'Кан Давид, от рода Дуло',
    (450, 450): 'Кан Астрахан, от рода Дуло',
    (460, 460): 'Кан Монолит, от рода Дуло',
    (558, 558): 'Кан Сандил, от рода Дуло',
    (570, 570): 'Кан Заберган, от рода Дуло',
    (584, 642): 'Хан Ювиги Кубрат, от рода Дуло',

    # First Bulgarian Kingdom - capital Плиска
    (681, 700): 'Велик Хан Аспарух, от рода Дуло, трети син на кан Кубрат',
    (700, 721): 'Велик Хан Тервел, от рода Дуло, син на Аспарух',
    (721, 738): 'Велик Хан Кормисош, от рода Вокил',
    (738, 754): 'Велик Хан Севар, от рода Дуло',
    (754, 760): 'Велик Хан Винех, от рода Укил',
    (760, 763): 'Велик Хан Телец, от рода Угаин',
    (766, 766): 'Велик Хан Умор, от рода Укил',
    (766, 767): 'Велик Хан Токту, от рода Дуло',
    (767, 768): 'Велик Хан Паган, от рода Дуло',
    (768, 777): 'Велик Хан Телериг',
    (777, 802): 'Велик Хан Кардам',
    (802, 814): 'Велик Хан Крум',
    (814, 831): 'Велик Хан Омуртаг, от рода Дуло,син на Крум',
    (831, 836): 'Велик Хан Маламир, от рода Дуло, най-малък син на Омуртаг',
    (836, 852): 'Велик Хан Персиан, племенник на Маламир',
    (852, 889): 'Хан Княз Борис I Михаил, син на Пресиян',
    (889, 893): 'Княз Владимир, първороден син на Борис I',

    # First Bulgarian Kingdom - capital Велики Преслав
    (893, 927): 'Цар Симеон I',
    (927, 970): 'Цар Петър I, син на Симеон',
    (970, 970): 'Цар Борис II, син на цар Петър',

    # First Bulgarian Kingdom  - capital Охрид
    (971, 991): 'Цар Роман, втори син на цар Петър',
    (991, 1014): 'Цар Самуил, най-малък син на комит Никола',
    (1014, 1015): 'Цар Гаврил Радомир, първороден син на Самуил',
    (1015, 1018): 'Цар Иван Владислав, син на Арон',
    (1018, 1185): 'Византийско владичество',

    # Second Bulgarian kingdom - capital Велико Търново
    (1185, 1187): 'Цар Теодор-Петър II (Делян), брат Асен',
    (1187, 1196): 'Цар Асен I',
    (1196, 1197): 'Цар Теодор-Петър II (Делян), брат Асен',
    (1197, 1207): 'Цар Калоян, получава титлата крал от папа Инокентий III',
    (1207, 1218): 'Цар Борил, сестрин син на Асеновци',
    (1218, 1241): 'Цар Иван Асен II, син на цар Асен I',
    (1241, 1246): 'Цар Коломан I Асен, син на Иван Асен II',
    (1246, 1256): 'Цар Михаил II Асен, син на Иван Асен II от брака му с Ирина Комнина',
    (1256, 1256): 'Цар Коломан II',
    (1256, 1257): 'Цар Мицо Асен, зет на Иван Асен II',
    (1257, 1277): 'Цар Константин Асен, болярин от Скопие',
    (1277, 1279): 'Цар Ивайло, завзема престола от цар Константин Тих',
    (1279, 1280): 'Цар Иван Асен III, внук на Иван Асен II',
    (1280, 1292): 'Цар Георги I Тертер, от кумански произход. Стратег на крепостта Червен',
    (1292, 1298): 'Цар Смилец, поставен от хан Ногай',
    (1299, 1299): 'Узурпатор Чака, син на хан Ногай и зет на цар Георги Тертер I',
    (1300, 1321): 'Цар Теодор-Светослав Тертер, син на Георги Тертет I',
    (1321, 1323): 'Цар Георги II Тертер',
    (1323, 1330): 'Цар Михаил III Шишман, видински деспот',
    (1330, 1331): 'Цар Иван Стефан',
    (1331, 1371): 'Цар Иван Александър I, деспот от Ловеч, син на деспот Срацимир',

    # Second Bulgarian kingdom - capital Видин
    (1371, 1393): 'Цар Иван Шишман',
    (1371, 1369): 'Цар Страцимир',
    (1396, 1878): 'Османско владичество',

    # Third Bulgarian kingdom- capital София
    (1879, 1887): 'Княз Александър II Батемберг',
    (1887, 1918): 'Цар Фердинанд I',
    (1918, 1943): 'Цар Борис III',
    (1943, 1946): 'Цар Симеон II',
}

if __name__ == '__main__':
    main()
