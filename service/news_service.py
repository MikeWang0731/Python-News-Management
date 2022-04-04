from db.news_dao import NewsDao
from db.redis_news_dao import RedisNewsDao
from db.mongo_news_dao import MongoNewsDao


class NewsService:
    __news_dao = NewsDao()
    __redis_news_dao = RedisNewsDao()
    __mongo_news_dao = MongoNewsDao()

    # 调用查看待审核新闻的接口
    def search_un_review_list(self, page):
        result = self.__news_dao.search_un_review_list(page)
        return result

    # 调用查看页数的接口
    def search_un_review_count_page(self):
        result = self.__news_dao.search_un_review_count_page()
        return result

    # 调用更新新闻审批状态的接口
    def update_un_review_news(self, news_id):
        self.__news_dao.update_un_review_news(news_id)

    # 调用打印所有新闻状态的接口
    def print_all_news(self, page):
        result = self.__news_dao.print_all_news(page)
        return result

    # 调用计算所有新闻的页数的接口
    def count_news_pages(self):
        result = self.__news_dao.count_news_pages()
        return result

    # 调用删除新闻的接口
    def delete_news_by_id(self, news_id):
        content_id = self.__news_dao.search_content_id(news_id)
        self.__news_dao.delete_news_by_id(news_id)
        self.__mongo_news_dao.delete_news_by_id(content_id)

    # 调用添加一条新闻的接口
    # 将新闻内容插入到mongoDB，将新闻的记录插入mySQL
    def insert(self, title, editor_id, type_id, content, is_top):
        self.__mongo_news_dao.insert(title, content)
        content_id = self.__mongo_news_dao.search_id(title)
        self.__news_dao.insert(title, editor_id, type_id, content_id, is_top)

    # 调用找到需要被缓存的新闻的接口
    def search_target_cache(self, news_id):
        result = self.__news_dao.search_target_cache(news_id)
        return result

    # 调用向redis中缓存新闻数据的接口
    def cache_news(self, news_id, title, username, news_type, content, is_top, create_time):
        self.__redis_news_dao.insert(news_id, title, username, news_type, content, is_top, create_time)

    # 调用删除缓存的新闻的接口
    def delete_cache(self, news_id):
        self.__redis_news_dao.delete_cache(news_id)

    # 调用根据id查找新闻的接口
    def search_news_by_id(self, news_id):
        result = self.__news_dao.search_news_by_id(news_id)
        return result

    # 调用更新新闻信息的接口：既要更新MySQL内部的信息，也要删除Redis中已有的缓存，更新mongo中的新闻内容
    def update_news(self, news_id, title, type_id, content, is_top):
        content_id = self.__news_dao.search_content_id(news_id)
        self.__mongo_news_dao.update(content_id, title, content)
        self.__news_dao.update_news(news_id, title, type_id, content_id, is_top)
        self.delete_cache(news_id)

    # 调用按照id在mongo数据库中查找新闻的方法
    def search_content_by_id(self, content_id):
        content = self.__mongo_news_dao.search_content_by_id(content_id)
        return content
