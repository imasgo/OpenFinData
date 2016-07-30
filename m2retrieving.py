from datetime import datetime


# Module, which is responsible for getting required from user data
class M2Retrieving:
    @staticmethod
    def get_data(input_string):
        """Getting JSON data based on input parameters"""

        # 1. Преобразовать входную строку в лист
        params = input_string.split(',')
        response = Result(request=input_string)

        # 2. Создать мэп списка
        response = M2Retrieving._list_to_mapper(params, response)
        if response.message != "":
            print(response.message)
            print(response.status)
            print(response.mapper)
            print(response.request)
            return response

        # 3. Проверить какому из существующих мэпов соответствует данный мэп
        # 4. Получить MDX запрос для мэпа
        mdx_skeleton = M2Retrieving._get_mdx_skeleton_for_mapper(response)

        if mdx_skeleton == 0:
            print(response.message)
            return response

        # 5. Подставить в MDX запрос вместо '*1, *2, *3 и тд' параметры
        # 6. Отправить MDX запрос
        mdx_query = M2Retrieving._refactor_mdx_skeleton(mdx_skeleton, params)
        result = M2Retrieving._send_mdx_request(mdx_query)
        if len(result == 0):
            return False
        return result

    @staticmethod
    def _list_to_mapper(parameters, response):
        """Refactoring input parameters in mapper"""

        # Inner codes for refactoring list in mapper
        _codes = (
            {
                'Расходы': 2,
                'Доходы': 3,
                'Дефицит': 4,
                'Профицит': 4
            },

            {
                'Плановый': 2,
                'Фактический': 3,
                'Текущий': 4,
                'Запланированный': 5
            }
        )

        mapper = ''

        if parameters[0] in _codes[0]:
            mapper += str(_codes[0].get(parameters[0])) + '.'
        else:
            response.status = False
            response.message = 'Неверно выбрана предметная область.'
            return response

        if parameters[1] == 'null':
            mapper += '0.'
        elif parameters[1] in _codes[1]:
            mapper += str(_codes[1].get(parameters[1])) + '.'
        else:
            response.status = False
            response.message = 'Неверно выбрана 1я характеристика предметной области'
            return response

        if parameters[2] == 'null':
            mapper += '0.'
        elif parameters[2] in _codes[2]:
            mapper += str(_codes[2].get(parameters[2])) + '.'
        else:
            response.status = False
            message = 'Параметр "' + parameters[2] + '" не верен. ' \
                                                     'Допустимы: отсутствие этого параметра, ' \
                                                     'значение "налоговый" или "неналоговый"'
            response.message = message
            return response

        if parameters[3] == 'null':
            mapper += '0.'
        elif int(parameters[3]) > 2006 and int(parameters[3]) <= datetime.today().year:
            mapper += '1.'
        else:
            response.status = False
            response.message = 'Введите год от 2007 до ' + str(datetime.today().year) + '.'
            return response

        if parameters[4] == 'null':
            mapper += '0.'
        else:
            mapper += '1.'

        if parameters[5] == 'null':
            mapper += '0'
        else:
            mapper += '1'

        response.mapper = mapper
        return response

    @staticmethod
    def _mapper_to_words(mapper):
        """Refactoring mapper in word constructions"""
        # Inner codes for refactoring mapper in list
        _codes = (
            {
                2: 'Расходы',
                3: 'Доходы',
                4: 'Дефицит/Профицит'
            },
            {
                0: 'Тип(пустой параметр)',
                2: 'Плановый',
                3: 'Фактический',
                4: 'Текущий',
                5: 'Запланированный'
            },
            {
                1: 'Налоговый/Неналоговый',
                0: 'Группа расходов(пустой параметр)'
            },
            {
                1: 'Год',
                0: 'Год(пустой параметр)'
            },
            {
                1: 'Сфера',
                0: 'Сфера(пустой параметр)'
            },
            {
                1: 'Территория',
                0: 'Территория (пустой параметр)'
            }
        )

        words = '/'
        items = mapper.split('.')
        index = 0
        for i in items:
            words += _codes[index].get(int(i)) + '/'
            index += 1
        return words

    @staticmethod
    def _get_mdx_skeleton_for_mapper(response):
        mdx_skeleton = M2Retrieving._mappers.get(response.mapper, 0)
        if mdx_skeleton == 0:
            close_mappers = []
            message2 = "Возможные варианты: "
            for i in list(M2Retrieving._mappers.keys()):
                if M2Retrieving._distance(i, response.mapper) == 1:
                    close_mappers.append(i)
                    message2 += M2Retrieving._mapper_to_words(i) + '\r\n'

            message1 = "Введенные параметры: " + M2Retrieving._mapper_to_words(response.mapper)
            response.message = message1 + '\r\nДанный запрос некорректен:(\r\n' + message2[:-3]
        return mdx_skeleton

    @staticmethod
    def _refactor_mdx_skeleton(mdx_skeleton, params):
        return

    @staticmethod
    def _send_mdx_request(mdx_query):
        return

    @staticmethod
    def _distance(a, b):
        """Levenshtein algorithm for finding the nearest mapper for requested one"""
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)  # Keep current and previous row, not entire matrix
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    _mappers = {
        # Expenditures' mappers
        '2.3.0.1.0.0': None,
        '2.2.0.1.1.0': None,
        '2.3.0.1.1.0': None,
        '2.5.0.1.1.0': None,
        '2.4.0.0.1.0': None,
        '2.3.0.1.0.1': None,
        '2.2.0.1.1.1': None,
        '2.3.0.1.1.1': None,
        '2.5.0.0.1.1': None,
        '2.4.0.0.1.1': None,

        # Profits' mappers
        '3.0.0.1.0.0': None,
        '3.2.0.1.0.0': None,
        '3.0.1.1.0.0': None,  # гд
        '3.2.1.1.0.0': None,  # гд
        '3.2.0.0.0.0': None,
        '3.2.1.0.0.0': None,  # гд-показатели исполнения бюджета
        '3.4.0.0.0.0': None,
        '3.4.1.0.0.0': None,  # гд-показатели исполнения бюджета
        '3.0.0.1.0.1': None,
        '3.2.0.1.0.1': None,
        '3.2.0.0.0.1': None,
        '3.2.1.0.0.1': None,  # гд
        '3.4.0.0.0.1': None,
        '3.4.1.0.0.1': None,  # гд

        # Deficit/surplus's mappers
        '4.2.0.0.0.0': None,
        '4.4.0.0.0.0': None,
        '4.0.0.1.0.0': None,
        '4.0.0.1.0.1': None,
        '4.2.0.1.0.1': None,
        '4.4.0.0.0.1': None
    }

    # Outer codes for substitution in MDX-query
    _places = {
        'г. Байконур': 93015,
        'Амурская область': 67708,
        'Еврейская автономная область': 67705,
        'Камчатский край': 67728,
        'Магаданская область': 67703,
        'Приморский край': 67706,
        'Республика Саха (Якутия)': 67642,
        'Сахалинская область': 67704,
        'Хабаровский край': 67707,
        'Чукотский автономный округ': 67640,
        'Дальневосточный федеральный округ': 17698,
        'г. Севастополь': 93011,
        'Республика Крым': 93010,
        'Крымский федеральный округ': 91128,
        'Кировская область': 67663,
        'Нижегородская область': 67656,
        'Оренбургская область': 67659,
        'Пензенская область': 67667,
        'Пермский край': 67727,
        'Республика Башкортостан': 67655,
        'Республика Марий Эл': 67666,
        'Республика Мордовия': 67662,
        'Республика Татарстан (Татарстан)': 67661,
        'Самарская область': 67658,
        'Саратовская область': 67665,
        'Удмуртская республика': 67668,
        'Ульяновская область': 67660,
        'Чувашская Республика - Чувашия': 67664,
        'Приволжский федеральный округ': 3417,
        'Архангельская область': 67678,
        'Вологодская область': 67674,
        'г. Санкт-Петербург': 67639,
        'Калининградская область': 67670,
        'Ленинградская область': 67676,
        'Мурманская область': 67669,
        'Ненецкий автономный округ': 67672,
        'Новгородская область':67675,
        'Псковская область': 67671,
        'Республика Карелия': 67677,
        'Республика Коми': 67673,
        'Северо-Западный федеральный округ': 10249,
        'Кабардино-Балкарская Республика': 67651,
        'Карачаево-Черкесская Республика': 67638,
        'Республика Дагестан': 67643,
        'Республика Ингушетия': 67649,
        'Республика Северная Осетия - Алания': 67652,
        'Ставропольский край': 67654,
        'Чеченская республика': 67650,
        'Северо-Кавказский федеральный округ': 24604,
        'Алтайский край': 67688,
        'Забайкальский край': 67729,
        'Иркутская область': 67682,
        'Кемеровская область': 67689,
        'Красноярский край': 67694,
        'Новосибирская область': 67690,
        'Омская область': 67687,
        'Республика Алтай': 67684,
        'Республика Бурятия': 67691,
        'Республика Тыва': 67683,
        'Республика Хакасия': 67681,
        'Томская область': 67692,
        'Сибирский федеральный округ': 12097,
        'Курганская область': 67699,
        'Свердловская область': 67698,
        'Тюменская область': 67697,
        'Ханты-Мансийский автономный округ - Югра': 67695,
        'Челябинская область': 67700,
        'Ямало-Ненецкий автономный округ': 67696,
        'Уральский федеральный округ': 16333,
        'Белгородская область': 67721,
        'Брянская область': 67719,
        'Владимирская область': 67716,
        'Воронежская область': 67723,
        'г. Москва': 67724,
        'Ивановская область': 67722,
        'Калужская область': 67712,
        'Костромская область': 67714,
        'Курская область': 67710,
        'Липецкая область': 67711,
        'Московская область': 67709,
        'Орловская область': 67726,
        'Рязанская область': 67720,
        'Смоленская область': 67718,
        'Тамбовская область': 67725,
        'Тверская область': 67717,
        'Тульская область': 67715,
        'Ярославская область': 67713,
        'Центральный федеральный округ': 19099,
        'Астраханская область': 67645,
        'Волгоградская область': 67647,
        'Краснодарский край': 67644,
        'Республика Адыгея (Адыгея)': 67646,
        'Республика Калмыкия': 67648,
        'Ростовская область': 67653,
        'Южный федеральный округ': 3,
        'Российская Федерация': 2,
    }

class Result:
    def __init__(self, request='', status=False, message='', mapper='', response=''):
        self.request = request
        self.status = status
        self.message = message
        self.mapper = mapper
        self.response = response


M2Retrieving.get_data('Доходы,null,null,2010,jjj,jjj')
