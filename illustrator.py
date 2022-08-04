import json

import utility
import database

class Illustrator:
    def __init__(self, name, urls, rank, keywords, categoryRanks):
        self.id = None
        self.name = name
        self.urls = urls
        self.rank = rank
        self.keywords = keywords
        self.categoryRanks = categoryRanks

    def save(self):
        pass
    
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
            id = row[0],
            name = row[1],
            urls = json.loads(row[2]),
            rank = row[3],
            keywords = json.loads(row[4]),
            categoryRanks = json.loads(row[5]),
        )
        illustrator.id = row[0]
        illustrator.createdAt = utility.textToDatetime(row[6]),
        illustrator.updatedAt = utility.textToDatetime(row[7]),
        return illustrator

    
    
    