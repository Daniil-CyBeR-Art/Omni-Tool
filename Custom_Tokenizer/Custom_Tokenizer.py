import pymorphy2

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
            print(f"'{Author}' - текст разделен на {len(Extracted_Word_Lists[Author])} слов.")
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
        print(f"В словаре {len(Frequency_Dictionary)} уникальных слов.")
        return Frequency_Dictionary  # Возвращаем результирующий словарь (значения - индексы пар из временного словаря )

    # Функция для индексации
    def Dictionary_Based_Filtering(self, New_Texts, Frequency_Dictionary):
        # Результирующий список списков (слова проиндексированы)
        Indexed_Texts = []
        for Author, Text in New_Texts.items(): # Извлекаем Значение(Список слов) из словаря
            counter = 0
            Indexed_Text = [] # Инициализируем списком новый ключ словаря
            for word in Text: # Извлекаем слово из списка
                if word in Frequency_Dictionary and Frequency_Dictionary[word] < self.Num_Words: # Если слово есть в словаре и значение < Num_Words
                    Indexed_Text.append(Frequency_Dictionary[word]) # добавляем индекс слова в список
                else: # В остальных случаях
                    Indexed_Text.append(0) # добавляем в список 0
                    counter += 1
            Indexed_Texts.append(Indexed_Text) # Добавляем список в список
            print(f"'{Author}' - {counter} слов получили значение: 0")
        return Indexed_Texts # Результирующий список списков (слова проиндексированы)
    
    # Функция для приведения слов к лемме (на основе pymorphy2)
    def Rus_Reduce_to_Lemma(self, Extracted_Word_Lists):
        Lemmatized_Word_Lists = {} # Результирующий словарь (слова лемматизированны)
        m = pymorphy2.MorphAnalyzer() # Объект для морфологического анализа слов
        cache = {} # 'Кэш' для оптимизации процесса
        for author, text in Extracted_Word_Lists.items(): # Извлекаем пары из исходного словаря
            Lemmatized_Word_Lists[author] = [] # Инициализируем списком новый ключ словаря
            error = 0 # Переменная для счетчика ошибок
            for word in text: # Извлекаем слова из текста
                if word in cache: # Если слово есть в 'кэше'
                    lemmatized_word = cache[word] # используйем кэшированное значение
                else: # если нет
                    try: # если при поиске не возникло ошибок
                        lemmatized_word = m.parse(word)[0].normal_form # Извлекаем наиболее вероятный разбор
                        cache[word] = lemmatized_word  # Сохраняем слово в кэш
                    except Exception as e: # если возникла ошибка
                        print(f"Ошибка при лемматизации слова '{word}': {e}") # Информируем пользователя
                        lemmatized_word = word  # Сохраняем оригинальное слово
                        error += 1 # Увеличиваем счетчик для автора
                Lemmatized_Word_Lists[author].append(lemmatized_word) # и добавляем в список автора
            print(f"{author} - {len(Lemmatized_Word_Lists[author]) - error} слов лемматизировано.") # После обработки каждого текста информируем пользователя
        return Lemmatized_Word_Lists # Возвращаем результирующий словарь