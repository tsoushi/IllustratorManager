import sqlite3
import json

import utility

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
def addIllustrator(name: str, urls: list, rank: int, keywords: list, categoryRanks: dict):
    logger.debug('add illustrator')
    urls = json.dumps(urls)
    keywords = json.dumps(keywords)
    categoryRanks = json.dumps(categoryRanks)

    with sqlite3.connect(DBPATH) as db:
        logger.debug('committing to database')
        db.execute(
            'INSERT INTO illustrators(name, urls, rank, keywords, category_ranks) VALUES(?, ?, ?, ?, ?)',
            (name, urls, rank, keywords, categoryRanks)
        )
        id, createdAt, updatedAt = db.execute('SELECT id, created_at, updated_at FROM illustrators ORDER BY id DESC LIMIT 1;').fetchone()
        createdAt = utility.textToDatetime(createdAt)
        updatedAt = utility.textToDatetime(updatedAt)
        db.commit()
    logger.debug('add illustrator -> complete')

    return id, createdAt, updatedAt

# イラストレーターの情報を更新する
def updateIllustrator(id: int, name: str, urls: list, rank: int, keywords: list, categoryRanks: dict):
    logger.debug('update illustrator')
    urls = json.dumps(urls)
    keywords = json.dumps(keywords)
    categoryRanks = json.dumps(categoryRanks)
    with sqlite3.connect(DBPATH) as db:
        logger.debug('committing to database')
        db.execute(
            'UPDATE illustrators SET name = ?, urls = ?, rank = ?, keywords = ?, categoryRanks = ?, updated_at = DATETIME(CURRENT_TIMESTAMP, "localtime") WHERE id = ?',
            (name, urls, rank, keywords, categoryRanks, id)
        )
        updatedAt = db.execute('SELECT id FROM illustrators WHERE id = ?', (id,)).fetchone()[0]
        updatedAt = utility.textToDatetime(updatedAt)
        db.commit()
    logger.debug('update illustrator -> complete')

    return updatedAt

# idからイラストレーターを取得する
def getRowFromId(databaseId):
    logger.debug('get row from id')
    with sqlite3.connect(DBPATH) as db:
        data = db.execute('SELECT * FROM illustrators WHERE id = ?;', (databaseId,)).fetchone()
    if data:
        logger.debug('get row from id -> complete')
        return data
    else:
        logger.debug('get row from id -> not found -> complete')
        return None
