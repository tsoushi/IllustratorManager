import json

import utility
import database

import logging
logger = logging.getLogger('Log').getChild('Illustrator')

class Illustrator:
    def __init__(self, name, urls, rank, keywords, categoryRanks):
        self.id = None
        self.name = name
        self.urls = urls
        self.rank = rank
        self.keywords = keywords
        self.categoryRanks = categoryRanks

    # 変更を保存する(新規作成、更新問わず)
    def save(self):
        if self.id:
            self._updateDb()
        else:
            self._addToDb()
    
    # データベースから削除する
    def remove(self):
        logger.info(f'remove from database : id = {self.id}')
        if self.id:
            database.removeRowById(self.id)
            logger.info(f'remove from database -> complete')
        else:
            logger.warn('remove from database -> not saved')
            raise Exception('not saved in database')
            
    
    # データベースに新規追加する
    def _addToDb(self):
        id, createdAt, updatedAt = database.addIllustrator(
            name = self.name,
            urls = self.urls,
            rank = self.rank,
            keywords = self.keywords,
            categoryRanks = self.categoryRanks
        )
        self.id = id
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    # 変更内容をデータベースに保存する
    def _updateDb(self):
        updatedAt = database.updateIllustrator(
            id = self.id,
            name = self.name,
            urls = self.urls,
            rank = self.rank,
            keywords = self.keywords,
            categoryRanks = self.categoryRanks
        )
        self.updatedAt = updatedAt
    
    # データベースの初期化
    @staticmethod
    def initDb():
        database.initDb()
    
    # データベースから指定したIDのイラストレータの情報を削除
    @staticmethod
    def removeById(id):
        database.removeRowById(id)

    # 新規作成
    @staticmethod
    def new(name='', urls=None, rank=-1, keywords=None, categoryRanks=None):
        if urls is None:
            urls = []
        if keywords is None:
            keywords = []
        if categoryRanks is None:
            categoryRanks = {}
        illustrator = Illustrator(name, urls, rank, keywords, categoryRanks)
        return illustrator

    # idをもとにデータベースからインスタンスを作成
    @staticmethod
    def fromId(id):
        row = database.getRowFromId(id)
        if row:
            return Illustrator.fromDbRow(row)
        else:
            return None
    
    # データベースのすべてのデータからインスタンスを作成
    @staticmethod
    def getAll(limit=0):
        records = database.getAllIllustrators(limit=limit)
        return [Illustrator.fromDbRow(record) for record in records]
    
    # データベースの行データをもとにインスタンスを作成
    @staticmethod
    def fromDbRow(row):
        illustrator = Illustrator(
            name = row[1],
            urls = json.loads(row[2]),
            rank = row[3],
            keywords = json.loads(row[4]),
            categoryRanks = json.loads(row[5]),
        )
        illustrator.id = row[0]
        illustrator.createdAt = utility.textToDatetime(row[6])
        illustrator.updatedAt = utility.textToDatetime(row[7])
        return illustrator

    # テキストからインスタンスを一括作成
    @staticmethod
    def newFromText(text):
        lines = text.split('\n')
        state = 'ready'
        illustrators = []
        illustrator = None
        for line in lines:
            if state == 'ready':
                try:
                    illustrator = Illustrator.new(rank=int(line))
                    state = 'keywords'
                except ValueError:
                    continue
            elif state == 'keywords':
                if line:
                    illustrator.keywords = line.strip().split('、')
                state = 'name'
            elif state == 'name':
                illustrator.name = line.strip()
                state = 'last'
            elif state == 'last':
                if line.startswith('http'):
                    illustrator.urls.append(line.strip())
                elif line:
                    category, rank = line.replace('：', ':').split(':')
                    illustrator.categoryRanks[category] = int(rank)
                else:
                    illustrators.append(illustrator)
                    illustrator = None
                    state = 'ready'
        if illustrator:
            illustrators.append(illustrator)
        return illustrators