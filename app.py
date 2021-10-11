### Визуализация
import eel
# ЭТО ДОЛЖНО БЫТЬ ВНАЧАЛЕ, ИНАЧЕ ОН НЕ ИНИЦИАЛИЗИРУЕТ ВСЕ ФУНКЦИИ
eel.init('web')

from search import search as search_lib
from parse import parse as parse_lib

# Функция вывода сожержимого в html
# Эта функция вызывает функцию JS (output)
# и передает ей данные для вывода (value)
@eel.expose
def output_to_html_PY(value):
		eel.output_to_html_JS(value)


@eel.expose
def get_content_PY(query_obj):
		print(query_obj['action'], query_obj['value'])

		if query_obj['action'] == 'parse':
				parse(query_obj['value'])
		elif query_obj['action'] == 'search':
				search_db(query_obj['value'])


@eel.expose
def output_authors_to_html_PY(data, query):
		eel.output_authors_to_html_JS(data, query)


@eel.expose
def output_answers_results_to_html_PY(result):
		eel.output_answers_results_to_html_JS(result)


def parse(query):
		parse_lib.parse("storage/data.db", query, 10, '2021')
		output_to_html_PY('Done')


def search_db(query):
		info = search_lib.get_data_from_database("storage/data.db", query)
		search_lib.create_picture()
		output_authors_to_html_PY(info['authors'], query)

#####

# ЭТО ДОЛЖНО БЫТЬ В КОНЦЕ, ИНАЧЕ ОН НЕ ИНИЦИАЛИЗИРУЕТ ВСЕ ФУНКЦИИ
eel.start('main.html')

####
