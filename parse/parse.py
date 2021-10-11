# Используем selenium, потому что нужно отрендерить страницу и выполнить AJAX.
from selenium import webdriver
import sqlite3

def get_data(driver, url, search_query, year, page):
    # Переходим по url
    # Устанавливаем таймер максимального ожидания ajax на 7 секунд
    #driver.get(url)
    #driver.find_elements_by_css_selector('li>button')[0].click()
    driver.implicitly_wait(7)
    # Извлекаем по css-слекторам нужные нам блоки
    ul = driver.find_elements_by_css_selector('#search-results')
    titles  = ul[0].find_elements_by_css_selector('li>.title')
    text    = ul[0].find_elements_by_css_selector('li>div')
    topics  = ul[0].find_elements_by_css_selector('li>span:nth-child(2n)')

    # Перебираем все полученные статьи 
    # (предполагается, что кол-во всех блоков одинаково (кроме span-блоков, их в 2 раза больше))
    # Заосим значения в БД
    
    for i in range(len(titles)):
        if ( ((topics[2*i+1].text).split('/')[0]).strip() == year):
            ins = 'INSERT INTO cyberleninka (search_query, year, title, topic, authors, info) VALUES(?, ?, ?, ?, ?, ?)'
            curs.execute(ins, (
                                search_query,
                                ((topics[2*i+1].text).split('/')[0]).strip(), 
                                titles[i].text, 
                                ((topics[2*i+1].text).split('/')[1]).strip(), 
                                topics[2*i].text,
                                text[i].text
                            )
                        )
    
    # Что-то тут не то
    #print(page)
    driver.find_elements_by_css_selector('.paginator>li>a')[page].click()
    # Применяем изменения в БД
    conn.commit()


def get_url(keyword, page):
    return 'https://cyberleninka.ru/search?q='+keyword+'&page='+str(page)


def parse(path, keyword, page_count, year):
    # Инициируем соединение с БД
    global conn
    global curs
    conn = sqlite3.connect(path)
    curs = conn.cursor()
    # Создаем БД, если она еще не создана (раскомментировать)
    #curs.execute('''CREATE TABLE cyberleninka (search_query VARCHAR(50), year VARCHAR(4), title VARCHAR(100), topic VARCHAR(100), authors VARCHAR(100), info TEXT)''')


    # Открываем браузер (драйвер можно скачать с интрнета (потом его следует поместить в каталог с эти файлом))
    driver = webdriver.Chrome("parse/chromedriver.exe")
    
    # Перебираем страницы и записываем значения в БД
    # 0 страницы не сществет, пропускаем ее
    driver.get(get_url(keyword, 1))
    driver.find_elements_by_css_selector('li>button')[0].click()
    for page in range(page_count+1):
        if (page!=0):
            get_data(driver, get_url(keyword, page), keyword, year, page)
    
    # Закрываем браузер
    driver.quit()

    # Достаем значения из БД
    curs.execute("SELECT * FROM cyberleninka WHERE year LIKE '%"+year+"%'")

    # Выводим занченя в консоль
    rows = curs.fetchall()
    print("\n\n------------------------------------------------------------------------------------------------------")
    print("По запросу "+keyword+" Найдено " + str(len(rows))+" результатов:")
    print("------------------------------------------------------------------------------------------------------\n \n")
    for row in rows:
        print(row[3] + " --> " + row[2])
        print("Год: " + row[1])
        print("\n")
        print("Автор: " + row[4])
        print("\n")
        print(row[5])
        print("\n \n")

    conn.close()

#parse('блокчейн', 15, '2021')
#parse('scraping', 5, '2021')
#parse('data-mining', 3, '2021')