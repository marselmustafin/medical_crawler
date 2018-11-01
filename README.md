# Краулер медицинских отзывов

Краулер для сбора отзывов на клиники и врачей с сайта prodoctorov.ru
Также, краулер собирает данные о врачах.

В файлах `cities.json`, `comments.json`, `doctors.json`, `institutions.json` содержатся примеры собираемых данных.

## Подготовка к краулингу

Склонируйте проект и перейдите в него:
```
  git clone https://github.com/marselmustafin/medical_crawler

  cd medical_crawler
```

Убедитесь что все необходимые библиотеки есть на вашем компьютере.

Для загрузки свежих proxy ip адресов запустите следующий скрипт:
```
  python3 etc/import_proxies.py
```

## Сбор данных о врачах и клиниках

Сбор ссылок на страницы городов (Необязательно, т.к. существующий файл cities.json содержит актуальные города):
```
  scrapy crawl cities -o cities.json
```

Сбор ссылок на страницы клиник:
```
  scrapy crawl institutions -o institutions.json
```

Сбор данных о врачах:
```
  scrapy crawl doctors -o *названиефайла.json*
```

Сбор отзывов на клиники:
```
  scrapy crawl inst_comments -o *названиефайла.json*
```

Статистика по собранным данным
```
  python3 etc/crawled_data_stats.py *файл с комментариями*
```
