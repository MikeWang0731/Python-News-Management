from .mongo_db import client
from bson.objectid import ObjectId


class MongoNewsDao:

    @staticmethod
    # 添加新闻记录
    def insert(title, content):
        try:
            client.vega.news.insert_one({'title': title, 'content': content})
        except Exception as e:
            print("Error: ", e)

    @staticmethod
    # 通过新闻标题找到其id
    def search_id(title):
        try:
            news_id = client.vega.news.find_one({'title': title})
            return str(news_id['_id'])
        except Exception as e:
            print("Error: ", e)

    @staticmethod
    # 通过新闻的主键值修改这个新闻
    def update(news_id, title, content):
        try:
            client.vega.news.update_one({'_id': ObjectId(news_id)}, {'$set': {'title': title, 'content': content}})
        except Exception as e:
            print('Error: ', e)

    @staticmethod
    # 根据id查找正文
    def search_content_by_id(content_id):
        try:
            return client.vega.news.find_one({'_id': ObjectId(content_id)})['content']
        except Exception as e:
            print("Error:", e)

    @staticmethod
    # 根据id删除新闻
    def delete_news_by_id(content_id):
        try:
            client.vega.news.delete_one({'_id': ObjectId(content_id)})
        except Exception as e:
            print("Error:", e)
