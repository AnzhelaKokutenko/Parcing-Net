import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
import pandas as pd

url = 'https://hh.ru/search/vacancy'
params = {'fromSearchLine': True,
          'text': 'Phyton',
         'page': 0}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30/r4sT761g-47'}
vacancies_list = []
while True:
    response = requests.get(url, params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})
    if response.ok and vacancies:
        for vacancy in vacancies:
            vacancy_data = {}
            sal_min = []
            sal_max = []
            currency = []
            info = vacancy.find('a', {'class': 'bloko-link'})
            name = info.text
            link = info['href']
            hh = 'https://hh.ru'
            salary = vacancy.find ('span', {'data-qa':'vacancy-serp__vacancy-compensation'})
            if salary is not None:
                sal = salary.text.replace(u'\u202f', u'')
                salaries = sal.split()
                if '–' in salaries:
                    sal_min.append(salaries[0])
                    sal_max.append(salaries[2])
                    currency.append(salaries[3])
                elif 'от' in salaries:
                    sal_min.append(salaries[1])
                    sal_max.append(None)
                    currency.append(salaries[2])
                elif 'до' in salaries:
                    sal_min.append(None)
                    sal_max.append(salaries[1])
                    currency.append(salaries[2])
            else:
                sal_min = '-'
                sal_max = '-'
                currency = '-'
            vacancy_data['link'] = link
            vacancy_data['name'] = name
            vacancy_data['min salary'] = sal_min
            vacancy_data['max salary'] = sal_max
            vacancy_data['currency'] = currency
            vacancy_data['site'] = hh
            vacancies_list.append(vacancy_data)
        params['page'] += 1
    else:
        break
pprint(vacancies_list)

df = pd.DataFrame(vacancies_list)
a = df.to_string()
f = open("vacancies.txt", "w",encoding='utf-8')
f.write(a)
f.close()