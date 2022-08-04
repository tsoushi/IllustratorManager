import datetime

def textToDatetime(text):
    return datetime.datetime.strptime(text, '%Y-%m-%d %H:%M:%S')

def datetimeToText(dttm):
    return dttm.stfptime('%Y-%m-%d %H:%M:%S')