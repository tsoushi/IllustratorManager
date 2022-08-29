from illustrator import Illustrator

import logging
logger = logging.getLogger('Log')

# ロガーの初期設定
def initLogger(levelName):
    if levelName == 'debug':
        logLevel = logging.DEBUG
    elif levelName == 'info':
        logLevel = logging.INFO
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logLevel)
    logger.setLevel(logLevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

# イラストレーターの情報を標準出力する
def printIllustrator(illustrator):
    print('''id: {i.id}
name: {i.name}
rank: {i.rank}
urls: {i.urls}
keywords: {i.keywords}
categoryRanks: {i.categoryRanks}
created at: {i.createdAt}
updated at: {i.updatedAt}'''.format(i=illustrator))

def main():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('operation', choices=['add', 'view', 'remove', 'update'])
    parser.add_argument('--id', '-i', help='閲覧、削除、変更の際に使用', type=int, default=None)
    parser.add_argument('--name', '-n')
    parser.add_argument('--urls', '-u', nargs='*')
    parser.add_argument('--add-urls', '-au', nargs='*')
    parser.add_argument('--remove-urls', '-ru', nargs='*')
    parser.add_argument('--rank', '-r', type=int)
    parser.add_argument('--keywords', '-k', nargs='*')
    parser.add_argument('--add-keywords', '-ak', nargs='*')
    parser.add_argument('--remove-keywords', '-rk', nargs='*')
    parser.add_argument('--categoryRanks', '-cr', nargs='*')
    parser.add_argument('--add-category_ranks', '-acr', nargs='*')
    parser.add_argument('--remove-category_ranks', '-rcr', nargs='*')
    parser.add_argument('--debug', '-d', choices=['debug', 'info'], default='info')

    parser.add_argument('--yes', '-y', action='store_true', help='確認をすべてスキップする')

    args = parser.parse_args()

    initLogger(args.debug)

    # イラストレーター情報の新規追加
    if args.operation == 'add':
        name = args.name
        urls = args.urls
        rank = args.rank
        keywords = args.keywords
        categoryRanks = args.categoryRanks

        if args.name is None:
            name = ''
        if args.urls is None:
            urls = []
        if args.rank is None:
            rank = -1
        if args.keywords is None:
            keywords = []
        if args.categoryRanks is None:
            categoryRanks = {}
        else:
            categoryRanks = {i.split('=')[0]: i.split('=')[1] for i in args.categoryRanks},

        illustrator = Illustrator.new(
            name = name,
            urls = urls,
            rank = rank,
            keywords = keywords,
            categoryRanks = categoryRanks
        )
        print('保存中')
        illustrator.save()
        print(f'完了 - id: {illustrator.id}')

    # IDを使用する操作
    elif args.operation in ['view', 'remove', 'update']:
        if args.id is None:
            print('idを指定してください')
            return
        illustrator = Illustrator.fromId(args.id)
        if illustrator is None:
            print('指定したIDのデータは見つかりませんでした')
            return

        # イラストレーター情報表示
        if args.operation == 'view':
            print()
            printIllustrator(illustrator)
            print()
            return

        # イラストレーター情報の削除
        elif args.operation == 'remove':
            if not args.yes:
                print('以下のデータを削除します。よろしいですか？')
                print()
                printIllustrator(illustrator)
                print()
                if input('(y/n)') != 'y':
                    print('キャンセルしました')
                    return
            Illustrator.removeById(illustrator.id)
            print('削除しました')
        elif args.operation == 'update':
            if args.yes:
                print('以下の情報を変更しました')
            else:
                print('以下の情報を変更します。よろしいですか？')
            
            print()
            print(f'id: {illustrator.id}')

            if args.name:
                print(f'name : {illustrator.name} => {args.name}')
                illustrator.name = args.name

            if args.rank:
                print(f'rank : {illustrator.rank} => {args.rank}')
                illustrator.rank = args.rank

            if args.add_urls:
                print(f'urls : {illustrator.urls} => ', end='')
                illustrator.urls.extend(args.add_urls)
                print(illustrator.urls)
            elif args.remove_urls:
                print(f'urls : {illustrator.urls} => ', end='')
                for url in args.remove_urls:
                    try:
                        illustrator.urls.remove(url)
                    except ValueError:
                        pass
                print(illustrator.urls)
            elif args.urls:
                print(f'urls : {illustrator.urls} => {args.urls}')
                illustrator.urls = args.urls

            if args.add_keywords:
                print(f'keywords : {illustrator.keywords} => ', end='')
                illustrator.keywords.extend(args.add_keywords)
                print(illustrator.keywords)
            elif args.remove_keywords:
                print(f'keywords : {illustrator.keywords} => ', end='')
                for keyword in args.remove_keywords:
                    try:
                        illustrator.keywords.remove(keyword)
                    except ValueError:
                        pass
                print(illustrator.keywords)
            elif args.keywords:
                print(f'keywords : {illustrator.keywords} => {args.keywords}')
                illustrator.keywords = args.keywords

            if args.add_category_ranks:
                print(f'keywords : {illustrator.categoryRanks} => ', end='')
                for categoryRank in args.add_category_ranks:
                    category, rank = categoryRank.split('=')
                    illustrator.categoryRanks[category] = int(rank)
                print(illustrator.categoryRanks)
            elif args.remove_category_ranks:
                print(f'categoryRanks : {illustrator.categoryRanks} => ', end='')
                for category in args.remove_category_ranks:
                    try:
                        illustrator.categoryRanks.pop(category)
                    except KeyError:
                        pass
                print(illustrator.categoryRanks)
            elif args.categoryRanks:
                newCategoryRanks = {i.split('=')[0]: int(i.split('=')[1]) for i in args.categoryRanks}
                print(f'categoryRanks : {illustrator.categoryRanks} => {newCategoryRanks}')
                illustrator.categoryRanks = newCategoryRanks

            print()
            if not args.yes:
                if input('(y/n)') != 'y':
                    print('キャンセルしました')
                    return
            illustrator.save()
            print('変更しました')
    return    

if __name__ == '__main__':
    main()
