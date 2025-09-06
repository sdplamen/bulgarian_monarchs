from django.core.management.base import BaseCommand
from rulers.models import Monarch, Capital

class Command(BaseCommand):
    def handle(self, *args, **kwargs): 
        capitals_data = [
            {'name': 'Прабългарски владетели, Няма точна столица', 'start_year': 145, 'end_year': 642},
            {'name': 'Първо българско царство - столица Плиска', 'start_year': 681, 'end_year': 893},
            {'name': 'Първо българско царство - столица Велики Преслав', 'start_year': 893, 'end_year': 970},
            {'name': 'Първо българско царство - столица Охрид', 'start_year': 971, 'end_year': 1018},
            {'name': 'Византийско владичество. Няма столица през този период', 'start_year': 1018, 'end_year': 1185},
            {'name': 'Второ българско царство - столица Велико Търново', 'start_year': 1185, 'end_year': 1371},
            {'name': 'Второ българско царство - столица Видин', 'start_year': 1371, 'end_year': 1396},
            {'name': 'Османска империя. Няма столица през този период', 'start_year': 1396, 'end_year': 1878},
            {'name': 'Трето българско царство - столица София', 'start_year': 1879, 'end_year': 1946},
        ]

        monarchs_data = [
            # Proto-Bulgarian rulers
            {'name': 'Кан Авитохол, от рода Дуло', 'start_year': 145, 'end_year': 145},
            {'name': 'Кан Ирник, от рода Дуло', 'start_year': 437, 'end_year': 437},
            {'name': 'Кан Давид, от рода Дуло', 'start_year': 440, 'end_year': 440},
            {'name': 'Кан Астрахан, от рода Дуло', 'start_year': 450, 'end_year': 450},
            {'name': 'Кан Монолит, от рода Дуло', 'start_year': 460, 'end_year': 460},
            {'name': 'Кан Сандил, от рода Дуло', 'start_year': 558, 'end_year': 558},
            {'name': 'Кан Заберган, от рода Дуло', 'start_year': 570, 'end_year': 570},
            {'name': 'Хан Ювиги Кубрат, от рода Дуло', 'start_year': 584, 'end_year': 642},

            # First Bulgarian Kingdom - capital Плиска
            {'name': 'Велик Хан Аспарух, от рода Дуло, трети син на кан Кубрат', 'start_year': 681, 'end_year': 700},
            {'name': 'Велик Хан Тервел, от рода Дуло, син на Аспарух', 'start_year': 700, 'end_year': 721},
            {'name': 'Велик Хан Кормисош, от рода Вокил', 'start_year': 721, 'end_year': 738},
            {'name': 'Велик Хан Севар, от рода Дуло', 'start_year': 738, 'end_year': 754},
            {'name': 'Велик Хан Винех, от рода Укил', 'start_year': 754, 'end_year': 760},
            {'name': 'Велик Хан Телец, от рода Угаин', 'start_year': 760, 'end_year': 763},
            {'name': 'Велик Хан Умор, от рода Укил', 'start_year': 766, 'end_year': 766},
            {'name': 'Велик Хан Токту, от рода Дуло', 'start_year': 766, 'end_year': 767},
            {'name': 'Велик Хан Паган, от рода Дуло', 'start_year': 767, 'end_year': 768},
            {'name': 'Велик Хан Телериг', 'start_year': 768, 'end_year': 777},
            {'name': 'Велик Хан Кардам', 'start_year': 777, 'end_year': 802},
            {'name': 'Велик Хан Крум', 'start_year': 802, 'end_year': 814},
            {'name': 'Велик Хан Омуртаг, от рода Дуло,син на Крум', 'start_year': 814, 'end_year': 831},
            {'name': 'Велик Хан Маламир, от рода Дуло, най-малък син на Омуртаг', 'start_year': 831, 'end_year': 836},
            {'name': 'Велик Хан Персиан, племенник на Маламир', 'start_year': 836, 'end_year': 852},
            {'name': 'Хан Княз Борис I Михаил, син на Пресиян', 'start_year': 852, 'end_year': 889},
            {'name': 'Княз Владимир, първороден син на Борис I', 'start_year': 889, 'end_year': 893},

            # First Bulgarian Kingdom - capital Велики Преслав
            {'name': 'Цар Симеон I', 'start_year': 893, 'end_year': 927},
            {'name': 'Цар Петър I, син на Симеон', 'start_year': 927, 'end_year': 970},
            {'name': 'Цар Борис II, син на цар Петър', 'start_year': 970, 'end_year': 970},

            # First Bulgarian Kingdom - capital Охрид
            {'name': 'Цар Роман, втори син на цар Петър', 'start_year': 971, 'end_year': 991},
            {'name': 'Цар Самуил, най-малък син на комит Никола', 'start_year': 991, 'end_year': 1014},
            {'name': 'Цар Гаврил Радомир, първороден син на Самуил', 'start_year': 1014, 'end_year': 1015},
            {'name': 'Цар Иван Владислав, син на Арон', 'start_year': 1015, 'end_year': 1018},

            # Byzantine dominion
            {'name': 'Византийско владичество', 'start_year': 1018, 'end_year': 1185},

            # Second Bulgarian kingdom - capital Велико Търново
            {'name': 'Цар Теодор-Петър II (Делян)', 'family': 'брат Асен', 'start_year': 1185, 'end_year': 1187},
            {'name': 'Цар Асен I', 'family': '', 'start_year': 1187, 'end_year': 1196},
            {'name': 'Цар Теодор-Петър II (Делян)', 'family': 'брат Асен', 'start_year': 1196, 'end_year': 1197},
            {'name': 'Цар Калоян, получава титлата крал от папа Инокентий III', 'family': '', 'start_year': 1197, 'end_year': 1207},
            {'name': 'Цар Борил', 'family': 'сестрин син на Асеновци', 'start_year': 1207, 'end_year': 1218},
            {'name': 'Цар Иван Асен II', 'family': 'син на цар Асен I', 'start_year': 1218, 'end_year': 1241},
            {'name': 'Цар Коломан I Асен', 'family': 'син на Иван Асен II', 'start_year': 1241, 'end_year': 1246},
            {'name': 'Цар Михаил II Асен', 'family': 'син на Иван Асен II от брака му с Ирина Комнина', 'start_year': 1246, 'end_year': 1256},
            {'name': 'Цар Коломан II', 'family': '', 'start_year': 1256, 'end_year': 1256},
            {'name': 'Цар Мицо Асен', 'family': 'зет на Иван Асен II', 'start_year': 1256, 'end_year': 1257},
            {'name': 'Цар Константин Асен,', 'family': 'болярин от Скопие', 'start_year': 1257, 'end_year': 1277},
            {'name': 'Цар Ивайло', 'family': 'завзема престола от цар Константин Тих', 'start_year': 1277, 'end_year': 1279},
            {'name': 'Цар Иван Асен III', 'family': 'внук на Иван Асен II', 'start_year': 1279, 'end_year': 1280},
            {'name': 'Цар Георги I Тертер', 'family': 'от кумански произход. Стратег на крепостта Червен', 'start_year': 1280, 'end_year': 1292},
            {'name': 'Цар Смилец', 'family': 'поставен от хан Ногай', 'start_year': 1292, 'end_year': 1298},
            {'name': 'Узурпатор Чака', 'family': 'син на хан Ногай и зет на цар Георги Тертер I', 'start_year': 1299, 'end_year': 1299},
            {'name': 'Цар Теодор-Светослав Тертер', 'family': 'син на Георги Тертет I', 'start_year': 1300, 'end_year': 1321},
            {'name': 'Цар Георги II Тертер', 'family': '', 'start_year': 1321, 'end_year': 1323},
            {'name': 'Цар Михаил III Шишман, видински деспот', 'family': '', 'start_year': 1323, 'end_year': 1330},
            {'name': 'Цар Иван Стефан', 'family': '', 'start_year': 1330, 'end_year': 1331},
            {'name': 'Цар Иван Александър I, деспот от Ловеч', 'family': 'син на деспот Срацимир', 'start_year': 1331, 'end_year': 1371},

            # Second Bulgarian kingdom - capital Видин
            {'name': 'Цар Иван Шишман', 'family': '', 'start_year': 1371, 'end_year': 1393},
            {'name': 'Цар Страцимир', 'family': '', 'start_year': 1371, 'end_year': 1396},

            # Ottoman dominion
            {'name': 'Османско владичество', 'family': '', 'start_year': 1396, 'end_year': 1878},

            # Third Bulgarian kingdom - capital София
            {'name': 'Княз Александър I Батемберг', 'family': '', 'start_year': 1879, 'end_year': 1887},
            {'name': 'Цар Фердинанд I', 'family': '', 'start_year': 1887, 'end_year': 1918},
            {'name': 'Цар Борис III', 'family': 'син на Цар Фердинанд I', 'start_year': 1918, 'end_year': 1943},
            {'name': 'Цар Симеон II', 'family': 'син на Цар Борис III', 'start_year': 1943, 'end_year': 1946},
        ]

        # Create capitals first
        for cap_data in capitals_data: 
            Capital.objects.get_or_create(
                name=cap_data['name'],
                start_year=cap_data['start_year'],
                end_year=cap_data['end_year']
            )

        # Create monarchs and assign capitals
        for mon_data in monarchs_data: 
            capital = Capital.objects.filter(start_year__lte=mon_data['start_year'], end_year__gte=mon_data['end_year']).first()
            if capital: 
                Monarch.objects.get_or_create(name=mon_data['name'], start_year=mon_data['start_year'], end_year=mon_data['end_year'], capital=capital)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))