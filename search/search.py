import sqlite3
import nltk
from collections import Counter
from wordcloud import WordCloud

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
stopwords = nltk.corpus.stopwords.words('russian')
stemmer = nltk.SnowballStemmer("russian")

# Массив исключений
manual_stopwords = ['|',"'",',','.',')',',','(','m',"'m","n't",'e.g',"'ve",'s',
										'#','/','``',"'s","''",'!','r',']','=','[','s','&','%','*','...',
										'1','2','3','4','5','6','7','8','9','10','--',"''",';','-',':',

										'of', 'and', 'or', 'there', 'the', 'в', '«', '»']

# Инициируем соединение с БД
conn = sqlite3.connect('storage/data.db')
curs = conn.cursor()

# Объект выходных значений
data = {"authors": {}, "therms": {}}


# Приведем слова к унифицированнй форме, чтобы не было множественных форм...
def word_stemmer(wordrow):
    stemmed = [stemmer.stem(word) for word in wordrow]
    return stemmed

# Фильтр ненужных вхождений
def word_filter(excluded, wordrow):
		filtered = [word for word in wordrow if word not in excluded]
		return filtered

# Первоначальная обработка данных
def data_processing(text):
    output = nltk.word_tokenize(text) # токенизируем слова
    output = word_filter(manual_stopwords, output) # Удаляем ненужные вхождения
    output = word_filter(stopwords, output) # Выделяем основы слов (без множесвенных форм)
    output = word_stemmer(output) # Выделяем основы слов (без множесвенных форм)
    return output


# Выбираем наиболее часто встречающиеся слова из описания 
def top_five(input_text):
		output = {}
		tagged = data_processing(input_text)
		parts = Counter(word for word in tagged)
		parts = {k: parts[k] for k in sorted(parts, key=parts.get, reverse=True)}
		#print(parts, nltk.FreqDist(parts).most_common(5))
		i = 0
		mx = 5
		for part in parts:
		    #print(translation[part] + " " + str(parts[part]))
		    output[part] = parts[part] 
		    i = i + 1
		    if (mx <= i):
		    		break
		return output


def bind_therms(elements):
		for element in elements:
				if element in data['therms']:
						data['therms'][element] = data['therms'][element] + elements[element]
				else:
						data['therms'][element] = elements[element]


def bind_authors(authors):
		for author in authors:
				if author in data['authors']:
						data['authors'][author] += 1
				else:
						data['authors'][author] = 1


# Функция извлечения данных из БД
def get_data(path, query):
		global conn
		global curs

		conn = sqlite3.connect(path)
		curs = conn.cursor()
		# Достаем значени из БД
		# (Предполагается, что они уже собраны)
		curs.execute("SELECT * FROM cyberleninka WHERE search_query='"+query+"'")
		
		manual_stopwords.append(query) # Добавляем поисковой запрос в словам исключениям

		rows = curs.fetchall()
		for row in rows:
				bind_authors(row[4].split(',')) # Подсчет авторов
				bind_therms(top_five(row[5]))   # Подсчет слов
		
		return data


# очень много авторов, у которых 1 публикация, 
# такое количество публикаций ля модели - выброс - гепакс
# очищаем их
def clear_hepaxes_authors():
		output = {'authors': {}}
		hepaxes = nltk.FreqDist(data['authors']).hapaxes()
		data['authors'] = {k: data['authors'][k] for k in sorted(data['authors'], key=data['authors'].get, reverse=True)}
		for author in data['authors']:
				if (data['authors'][author] > 1):
						output['authors'][author] = data['authors'][author]
				else:
						break
		data['authors'] = output
				
def get_data_from_database(path, query):
		# Заполняем объект data данными
		global data
		data = {"authors": {}, "therms": {}}
		get_data(path, query)
		data['authors'] = nltk.FreqDist(data['authors']).most_common(10)
		# Проводим очистку от гепаксов
		#clear_hepaxes_authors()

		# Выводим топ самых частовстречающихся авторов/слов
		print("Топ авторов:")
		print(nltk.FreqDist(data['authors']).most_common(5))

		print("Топ слов:")
		print(nltk.FreqDist(data['therms']).most_common(20))
		return data


# !!! ВНИМАНИЕ !!!
# Скорее всего вы не установите эту бибиотеку через pip,
# Поэтому требуеся Установить библиотеку вручную:
# Переходим в каталог с whl файлом, запускаем команду:
# python -m pip install wordcloud-1.8.1-cp39-cp39-win_amd64.whl

# Импортируем инструменты для облака слов
def create_picture():
		# Создаем текст из полученных слов (этого требует библиотека отрисовки)
		text = ''
		elems = [(word+' ')*val for word, val in nltk.FreqDist(data['therms']).most_common(20)]
		for elem in elems:
				text += elem

		# Генерируем облако слов
		wordcloud = WordCloud(width = 2000, 
		                      height = 1500, 
		                      random_state=1, 
		                      background_color='Black', 
		                      margin=20, 
		                      colormap='Pastel1', 
		                      collocations=False).generate(text)
		# Сохраняем
		wordcloud.to_file('./web/words_cloud.png')

if __name__ == "__main__":
		do()