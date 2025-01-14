class Custom_Tokenizer:
    def __init__(self,
                 Allowed_Letters=None,
                 Allowed_Characters=None,
                 Invalid_Characters=None,
                 Stopwords=None,
                 Num_Words=None):

        # Задаем значения по умолчанию, если аргументы не переданы
        if Allowed_Letters is None:
            Allowed_Letters = set(['А','а','Б','б','В','в','Г','г','Д','д',
                                   'Е','е','Ё','ё','Ж','ж','З','з','И','и',
                                   'Й','й','К','к','Л','л','М','м','Н','н',
                                   'О','о','П','п','Р','р','С','с','Т','т',
                                   'У','у','Ф','ф','Х','х','Ц','ц','Ч','ч',
                                   'Ш','ш','Щ','щ','Ъ','ъ','Ы','ы','Ь','ь',
                                   'Э','э','Ю','ю','Я','я'])

        if Allowed_Characters is None:
            Allowed_Characters = set([' ','-',
                                      '/','’'])

        if Invalid_Characters is None:
            Invalid_Characters = set(['.',',','!',
                                      '?',':',';',
                                      '"','(',')'])

        if Stopwords is None:
            Stopwords = set(['и','в','во','не','что','он','на','я','с','со','как','а','то','все','она',
                             'так','его','но','да','ты','к','у','же','вы','за','бы','по','только','ее',
                             'мне','было','вот','от','меня','еще','нет','о','из','ему','теперь','когда',
                             'даже','ну','вдруг','ли','если','уже','или','ни','быть','был','него','до',
                             'вас','нибудь','опять','уж','вам','ведь','там','потом','себя','ничего','ей',
                             'может','они','тут','где','есть','надо','ней','для','мы','тебя','их','чем',
                             'была','сам','чтоб','без','будто','чего','раз','тоже','себе','под','будет',
                             'ж','тогда','кто','этот','того','потому','этого','какой','совсем','ним',
                             'здесь','этом','один','почти','мой','тем','чтобы','нее','сейчас','были',
                             'куда','зачем','всех','никогда','можно','при','наконец','два','об','другой',
                             'хоть','после','над','больше','тот','через','эти','нас','про','всего','них',
                             'какая','много','разве','три','эту','моя','впрочем','хорошо','свою','этой',
                             'перед','иногда','лучше','чуть','том','нельзя','такой','им','более','всегда',
                             'конечно','всю','между'])

        if Num_Words is None:
            Num_Words = 10000

        self.Allowed_Letters = Allowed_Letters
        self.Allowed_Characters = Allowed_Characters
        self.Invalid_Characters = Invalid_Characters
        self.Stopwords = Stopwords
        self.Num_Words = Num_Words

    # Функция для фильтрации и разбиения текстов на слова
    def Filtering_and_Separation(self, All_Texts):

        # Проверка, если входные данные - это строка
        if isinstance(All_Texts, str):
            All_Texts = {'Author': All_Texts}  # Используем фиксированное имя для автора, например 'Author'

        # Результирующий словарь (все тексты отфильтрованы и разбиты на слова)
        Extracted_Word_Lists = {}

        for Author, Text in All_Texts.items(): # Извлекаем Ключ(Автор) и Значение(Текст) из словаря

            Filtered_Text = '' # Инициализируем пустой строкой новый отфильтрованный текст

            for symbol in Text: # Извлекаем символ из текста
                if symbol in self.Allowed_Letters or symbol in self.Allowed_Characters: # Если есть среди разрешенных букв/символов
                    Filtered_Text += symbol.lower() # Приводим к нижнему регистру и добавляем в словарь
                elif symbol in self.Invalid_Characters: # Если есть среди недопустимых символов
                    Filtered_Text += ' ' # Заменяем пробелом
                else: # Если нет ни в одном из списков
                    Filtered_Text += '--' # Заменяем на '--'

            Words = Filtered_Text.split() # Разбиваем отфильтрованный текст на слова

            Extracted_Word_Lists[Author] = [] # Инициализируем списком новый ключ словаря

            for word in Words: # Извлекаем слово из списка
                if '-' in word and word.count("-") == 3: # Если в слове есть '-' и их три:
                    word = word.replace("--", "") # два, идущие подряд, удаляем
                    if word not in self.Stopwords: # и если слово не является 'стоп-словом'
                        Extracted_Word_Lists[Author].append(word) # добавляем слово в список по ключу
                elif '-' in word and word.count("-") == 2 and word != '--': # Если в слове есть '-', их два и это не отдельное слово
                    word = word.replace("--", "") # удаляем оба '-'
                    if word not in self.Stopwords: # и если слово не является 'стоп-словом'
                        Extracted_Word_Lists[Author].append(word) # добавляем слово в список по ключу
                elif '-' in word and word.count("-") == 1 and word != '-': # Если в слове есть один '-' и это не отдельное слово
                    if word not in self.Stopwords: # и если слово не является 'стоп-словом'
                        Extracted_Word_Lists[Author].append(word) # добавляем слово в список по ключу
                elif '-' not in word: # Если в слове нет '-'
                    if word not in self.Stopwords: # и если слово не является 'стоп-словом'
                        Extracted_Word_Lists[Author].append(word) # добавляем слово в список по ключу

        return Extracted_Word_Lists # Возвращаем результирующий словарь (все тексты отфильтрованы и разбиты на слова)

    # Функция для извлечения частотного словаря
    def Extract_Frequency_Dictionary(self, Extracted_Word_Lists):

        # Результирующий словарь (значения - индексы пар из временного словаря)
        Frequency_Dictionary = {}

        # Временный словарь (значение - частота вхождения слова, от большего к меньшему)
        Temp_Frequency_Dictionary = {}

        for Text in Extracted_Word_Lists.values(): # Извлекаем Значение(Список слов) из словаря
            for word in Text: # Извлекаем слово из списка
                if word in Temp_Frequency_Dictionary: # Если ключ есть во временном словаре
                    Temp_Frequency_Dictionary[word] += 1 # Увеличиваем значение на 1
                else: # Если ключа нет
                    Temp_Frequency_Dictionary[word] = 1 # Инициализируем единицей новый ключ словаря

        # Сортировка словаря временной частоты по убыванию значения
        Temp_Frequency_Dictionary = sorted(Temp_Frequency_Dictionary.items(), key=lambda item: item[1], reverse=True)

        for index, (key, value) in enumerate(Temp_Frequency_Dictionary): # Извлекаем пары и их индексы
            Frequency_Dictionary[key] = index + 1  # Добавляем ключ и индекс пары +1 в результирующий словарь

        return Frequency_Dictionary  # Возвращаем результирующий словарь (значения - индексы пар из временного словаря )

    # Функция для фильтрации нового текста, на основе частотного словаря исходного текста
    def Dictionary_Based_Filtering(self, New_Texts, Frequency_Dictionary):

        # Результирующий список списков (слова проиндексированы)
        Indexed_Texts = []

        for Text in New_Texts.values(): # Извлекаем Значение(Список слов) из словаря

            Indexed_Text = [] # Инициализируем списком новый ключ словаря

            for word in Text: # Извлекаем слово из списка
                if word in Frequency_Dictionary and Frequency_Dictionary[word] < self.Num_Words: # Если слово есть в словаре и значение < Num_Words
                    Indexed_Text.append(Frequency_Dictionary[word]) # добавляем индекс слова в список
                else: # В остальных случаях
                    Indexed_Text.append(0) # добавляем в список 0

            Indexed_Texts.append(Indexed_Text) # Добавляем список в список

        return Indexed_Texts # Результирующий список списков (слова проиндексированы)