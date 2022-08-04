import json

import utility

class Illustrator:
    def __init__(self, name, urls=[], rank=-1, keywords=[], categoryRanks={}, createdAt=None, updatedAt=None, id=None):
        self.id = id
        self.name = name
        self.urls = urls
        self.rank = rank
        self.keywords = keywords
        self.categoryRanks = categoryRanks
        self.createdAt = createdAt
        self.updatedAt = updatedAt

    @staticmethod
    def fromSqlRow(row):
        return Illustrator(
            id = row[0],
            name = row[1],
            urls = json.loads(row[2]),
            rank = row[3],
            keywords = json.loads(row[4]),
            categoryRanks = json.loads(row[5]),
            createdAt = utility.textToDatetime(row[6]),
            updatedAt = utility.textToDatetime(row[7]),
        )
    