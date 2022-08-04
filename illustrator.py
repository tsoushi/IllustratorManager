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
    
    # 新規作成
    @staticmethod
    def new(name, urls=[], rank=-1, keywords=[], categoryRanks={}):
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

    
    
    