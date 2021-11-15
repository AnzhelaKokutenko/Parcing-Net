from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['Parsing']

    def process_item(self, item, spider):
        if spider.name == 'hh':
            list = []
            for i in item['salary']:
                l = i.replace(" ", "").replace("\xa0", "")
                list.append(l)
            item['salary'] = list
            if item['salary'][0] == 'от':
                item['min_salary'] = int(item['salary'][1])
                if item['salary'][2] == 'до':
                    item['max_salary'] = int(item['salary'][3])
                    item['currency'] = item['salary'][5]
                else:
                    item['max_salary'] = None
                    item['currency'] = item['salary'][3]
            elif item['salary'][0] == 'до':
                item['min_salary'] = None
                item['max_salary'] = item['salary'][1]
                item['currency'] = item['salary'][3]
            else:
                item['min_salary'] = None
                item['max_salary'] = None
            del item['salary']
            item['site'] = 'https://hh.ru'

        if spider.name == 'sj':
            list = []
            for i in item['salary']:
                l = i.replace(" ", "").replace("\xa0", "")
                list.append(l)
            item['salary'] = list

            if item['salary'][0] == 'Подоговорённости':
                item['min_salary'] = None
                item['max_salary'] = None

            elif item['salary'][2] == '—':
                item['min_salary'] = int(item['salary'][0])
                item['max_salary'] = int(item['salary'][4])
                item['currency'] = item['salary'][6]

            elif item['salary'][0] == 'от':
                pos = item['salary'][2].find('руб.')
                item['min_salary'] = item['salary'][2][:pos]
                item['currency'] = item['salary'][2][pos:]

            elif item['salary'][0] == 'до':
                pos = item['salary'][2].find('руб.')
                item['max_salary'] = item['salary'][2][:pos]
                item['currency'] = item['salary'][2][pos:]

            elif item['salary'][2] == 'руб.':
                item['min_salary'] = item['salary'][0]
                item['max_salary'] = item['salary'][0]
                item['currency'] = item['salary'][2]
            else:
                item['min_salary'] = None
                item['max_salary'] = None
            del item['salary']
            item['site'] = 'https://superjob.ru'

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
