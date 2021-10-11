# Python web-parser with GUI

### Особенности:
1. Библиотека eel.js требует установленного браузера chrome.
2. Для работы selenium требуется chrome webdriver, который нужно поместить в каталог (parse)
3. На windows может возникнуть проблема с установкой пакета wordcloud

Ссылка для загрузки пакета wordcloud .whl формата и драйвера chromedriver.exe:
https://disk.yandex.ru/d/EIpiXA7LWODBtA

### Устанока библиотек:
```shell
		pip3 install selenium
		pip3 install nltk
		pip3 install collections
		pip3 install eel
		pip3 install wordcloud
```


### Проблемы с Wordcloud
На windows может возникнуть проблема с установкой пакета wordcloud. Поэтому эту бибиотеку нужно установить вручную. Для этого стоит перейти в каталог с пакетом .whl и выполнить pip команду.

Установка локальных пакетов: 

```shell
		pip install pakage-name.whl
```

Пример:
```shell
		pip install wordcloud-1.8.1-cp39-cp39-win_amd64.whl
```