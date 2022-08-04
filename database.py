import sqlite3
import json

from .illustrator import Illustrator

import logging
logger = logging.getLogger(__name__)

DBPATH = 'data.db'
SCHEMA_PATH = 'schema.sql'

# データベースの初期化
def initDb():
    logger.info('initialize database')
    with sqlite3.connect(DBPATH) as db:
        db.executescript(open(SCHEMA_PATH, 'r', encoding='utf-8').read())
        db.commit()
        logger.info('initialize database -> complete')

# 新しいイラストレーターを追加する
def addIllustrator(illustrator: Illustrator):
    logger.debug('add illustrator')
    name = illustrator.name
    urls = json.dumps(illustrator.urls)
    rank = illustrator.rank
    keywords = json.dumps(illustrator.keywords)
    categoryRanks = json.dumps(illustrator.categoryRanks)

    with sqlite3.connect(DBPATH) as db:
        logger.debug('committing to database')
        db.execute(
            'INSERT INTO illustrators(name, urls, rank, keywords, category_ranks) VALUES(?, ?, ?, ?, ?)',
            (name, urls, rank, keywords, categoryRanks)
        )
    logger.debug('add illustrator -> complete')

# idからイラストレーターを取得する
def getIllustratorFromId(databaseId):
    logger.debug('get illustrator from id')
    with sqlite3.connect(DBPATH) as db:
        data = db.execute('SELECT * FROM illustrators WHERE id = ?;', (databaseId,)).fetchone()
    if data:
        logger.debug('get illustrator from id -> complete')
        return Illustrator.fromSqlRow(data)
    else:
        logger.debug('get illustrator from id -> not found -> complete')
        return None
