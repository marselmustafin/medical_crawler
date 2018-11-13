# Краулер https://protabletky.ru/

прокси отключен, чтобы включить нужно просто расскоментировать строчки в scrapy.cfg

## Подготовка к краулингу

Склонируйте проект и перейдите в него:
```
  git clone https://github.com/marselmustafin/medical_crawler

  cd medical_crawler/drugs_crawler
```

Убедитесь что все необходимые библиотеки есть на вашем компьютере.

Для загрузки свежих proxy ip адресов запустите следующий скрипт:
```
  python3 ../etc/import_proxies.py
```

## Сбор данных

Сбор ссылок подгруппы таблеток
```
  scrapy crawl drugs_groups -o drugs_groups.json
```

Сбор ссылок на таблетки и их оценки:
```
  scrapy crawl drugs -o drugs.json
```

Сбор ссылок на таблетки и их оценки:
```
  scrapy crawl consumers_drugs_reviews -o consumers_drugs_reviews.json
  scrapy crawl doctors_drugs_reviews -o doctors_drugs_reviews.json
``
