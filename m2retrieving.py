from urllib import request, parse


# Module, which is responsible for getting required from user data
class M2Retrieving:
    @staticmethod
    def get_data(input_string):
        """Getting JSON data based on input parameters"""

        # 1. Преобразовать входную строку в лист                                -> get_data
        params = input_string.split(',')

        # 2. Создать мэп списка                                                 -> _list_to_map
        mapper = M2Retrieving._list_to_map(params)

        # 3. Проверить какому из существующих мэпов соответствует данный мэп
        # 4. Получить MDX запрос для мэпа                                       -> _get_mdx_skeleton_for_map

        mdx_skeleton = M2Retrieving._get_mdx_skeleton_for_mapper(mapper)
        if len(mdx_skeleton) == 0:
            return False
        else:
            # 5. Подставить в MDX запрос вместо "*1, *2, *3 и тд" параметры
            # 6. Отправить MDX запрос                                           -> _refactor_mdx_skeleton
            mdx_query = M2Retrieving._refactor_mdx_skeleton(mdx_skeleton, params)
            result = M2Retrieving._send_mdx_request(mdx_query)
            if len(result == 0):
                return False
            return result

    @staticmethod
    def _list_to_map(parameters):
        return

    @staticmethod
    def _get_mdx_skeleton_for_mapper(mapper):
        return

    @staticmethod
    def _refactor_mdx_skeleton(mdx_skeleton, params):
        return

    @staticmethod
    def _send_mdx_request(mdx_query):
        return

    _mappers = {
        # Расходы
        '1.11.1.1.0': None,
        '1.11.1.0.1': None,
        '1.11.1.1.1': None,
        '1.12.1.0.0': None,
        '1.12.1.1.0': None,
        '1.12.1.0.1': None,
        '1.12.1.1.1': None,
        '1.13.0.1.0': None,
        '1.13.0.1.1': None,
        '1.14.0.1.0': None,
        '1.14.0.1.1': None,

        # Доходы
        '2.21.221.1.0': None,
        '2.21.221.1.1': None,

        '2.22.221.1.1': None,
        '2.22.222.1.0': None,
        '2.22.221.0.0': None,
        '2.22.223.0.0': None,
        '2.22.221.1.0': None,
        '2.22.221.0.1': None,
        '2.22.222.0.1': None,

        '2.23.223.0.0': None,
        '2.23.221.0.0': None,
        '2.23.221.0.1': None,
        '2.23.222.0.1': None,

        # Дефицит/Профицит
        '3.341.1.0': None,
        '3.342.0.0': None,
        '3.342.0.1': None,
        '3.343.0.0': None,
        '3.343.0.1': None
    }

    # Внутренние кодовые обозначения для мэпперов
    _theme = {
        'Расходы': 1,
        'Доходы': 2,
        'Дефицит': 3,
        'Профицит': 3
    }
    # Внутренние кодовые обозначения для мэпперов
    _expenditures = {
        'Плановый': 11,
        'Фактические': 12,
        'Текущие': 13,
        'Запланированные': 14
    }

    # Внутренние кодовые обозначения для мэпперов
    _profit1 = {
        '': 21,
        'Плановые': 22,
        'Текущие': 23
    }

    _profit2 = {
        '': 221,
        'Группа доходов': 222,
        'Показатели исполнения бюджета': 223
    }

    # Внутренние кодовые обозначения для мэпперов
    _deficit = {
        '': 341,
        'Плановый': 342,
        'Текущий': 343
    }

    _places = {
        'Российская  Федерация': 2,
        'Крымский федеральный округ': 91128,
        'Республика Крым': 91129,
        'г. Севастополь': 91139,
        'г. Байконур': 93015,
        'Северо-Кавказский федеральный округ': 24604,
        'Ставропольский край': 3086,
        'Республика Ингушетия': 2135,
        'Республика Дагестан': 4,
        'Кабардино-Балкарская Республика': 2374,
        'Республика Северная Осетия - Алания': 2507,
        'Карачаево-Черкесская Республика': 1354,
        'Чеченская республика': 2136,
        'Южный федеральный округ': 3,
        'Краснодарский край': 749,
        'Астраханская область': 1176,
        'Волгоградская область': 1512,
        'Ростовская область': 2622,
        'Республика Адыгея (Адыгея)': 1451,
        'Республика Калмыкия': 2006,
        'Приволжский федеральный округ': 3417,
        'Нижегородская область': 4439,
        'Кировская область': 7726,
        'Самарская область': 5140,
        'Оренбургская область': 5483,
        'Пензенская область': 9475,
        'Пермский край': 24541,
        'Саратовская область': 8860,
        'Ульяновская область': 6097,
        'Республика Башкортостан': 3418,
        'Республика Марий Эл': 9301,
        'Республика Мордовия': 7265,
        'Республика Татарстан (Татарстан)': 6265,
        'Удмуртская республика': 9907,
        'Чувашская Республика - Чувашия': 8208,
        'Северо-Западный федеральный округ': 10249,
        'Архангельская область': 11867,
        'Ненецкий автономный округ': 10575,
        'Вологодская область': 10809,
        'Калининградская область': 10293,
        'г. Санкт-Петербург': 11755,
        'Ленинградская область': 11404,
        'Мурманская область': 10250,
        'Новгородская область': 11182,
        'Псковская область': 10330,
        'Республика Карелия': 11627,
        'Республика Коми': 10597,
        'Сибирский федеральный округ': 12097,
        'Алтайский край': 13781,
        'Красноярский край': 15777,
        'Иркутская область': 12232,
        'Кемеровская область': 14580,
        'Новосибирская область': 14804,
        'Омская область': 13356,
        'Томская область': 15593,
        'Забайкальский край': 24584,
        'Республика Бурятия': 15295,
        'Республика Алтай': 12792,
        'Республика Тыва': 12649,
        'Республика Хакасия': 12130,
        'Уральский федеральный округ': 16333,
        'Курганская область': 16921,
        'Свердловская область': 16827,
        'Тюменская область': 16507,
        'Ханты-Мансийский автономный округ - Югра': 16334,
        'Ямало-Ненецкий автономный округ': 16448,
        'Челябинская область': 17380,
        'Центральный федеральный округ': 19099,
        'Белгородская область': 22729,
        'Брянская область': 22143,
        'Владимирская область': 21258,
        'Воронежская область': 23249,
        'Ивановская область': 23067,
        'Тверская область': 21386,
        'Калужская область': 20350,
        'Костромская область': 20774,
        'Курская область': 19479,
        'Липецкая область': 20018,
        'г. Москва': 23783,
        'Московская область': 19100,
        'Орловская область': 24262,
        'Рязанская область': 22433,
        'Смоленская область': 21792,
        'Тамбовская область': 23909,
        'Тульская область': 21078,
        'Ярославская область': 20670,
        'Дальневосточный федеральный округ': 17698,
        'Приморский край': 18354,
        'Хабаровский край': 18540,
        'Амурская область': 18776,
        'Камчатский край': 24543,
        'Магаданская область': 18239,
        'Сахалинская область': 18294,
        'Чукотский автономный округ': 18184,
        'Республика Саха (Якутия)': 17699,
        'Еврейская автономная область': 18317
    }
