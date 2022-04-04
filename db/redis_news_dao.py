import redis
from .redis_db import pool


class RedisNewsDao:
    @staticmethod
    def insert(news_id, title, username, news_type, content, is_top, create_time):
        con = redis.Redis(connection_pool=pool)
        try:
            # 将新闻信息储存到Redis的哈希表结构
            con.hmset(news_id, {
                'title': title,
                'author': username,
                'type': news_type,
                'content': content,
                'is_top': is_top,
                'create_time': create_time
            })
            # 如果不是手动置顶，则只缓存24小时
            if is_top == 0:
                con.expire(news_id, 24 * 60 * 60)
        except Exception as e:
            print("Error: ", e)
        finally:
            del con

    @staticmethod
    def delete_cache(news_id):
        con = redis.Redis(connection_pool=pool)
        try:
            # 如果redis中不存在这个key，是不会报异常的，只是这个操作会返回0
            con.delete(news_id)
        except Exception as e:
            print("Error:", e)
        finally:
            del con
