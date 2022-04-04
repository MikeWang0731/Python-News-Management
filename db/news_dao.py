from .mysql_db import pool


class NewsDao:

    @staticmethod
    # 查询待审批的新闻列表
    # page: 查看的页数，如page=1，那就是第一页
    def search_un_review_list(page):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            # 返回待审批的新闻信息，包含新闻标题，新闻类型，编辑者
            # 并且要限制每一屏展示的信息数量
            sql = "select n.id, n.title,t.type,u.username from t_news n " \
                  "join t_type t on n.type_id=t.id join t_user u on n.editor_id=u.id " \
                  "where n.state=%s order by n.create_time desc limit %s,%s"
            # 偏移量的计算方式，每页10个，那第一页就是从第一条开始，偏移量就是0，所以要page-1
            cursor.execute(sql, ['待审批', (page - 1) * 10, 10])
            result = cursor.fetchall()
            return result  # Result -> [(1, '新闻标题1', '要闻', 'scott')]
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                # 归还连接
                con.close()

    @staticmethod
    # 计算我们的结果一共需要几页来展示（10条/页）
    def search_un_review_count_page():
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            # 结果除以10且向上进位，例如21条就是21/10=2.1也就是3页
            sql = 'select ceil(count(*)/10) from t_news where state=%s'
            cursor.execute(sql, ['待审批'])
            page = cursor.fetchone()[0]
            return page
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    # 更新新闻的审批状态
    def update_un_review_news(news_id):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = 'update t_news set state=%s where id=%s'
            cursor.execute(sql, ['已审批', news_id])
            con.commit()
        except Exception as e:
            if 'con' in dir():
                con.rollback()
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    # 打印所有的新闻信息
    def print_all_news(page):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            # 返回所有的新闻信息，包含新闻标题，新闻类型，编辑者
            # 并且要限制每一屏展示的信息数量
            sql = "select n.id, n.title,t.type,u.username from t_news n " \
                  "join t_type t on n.type_id=t.id join t_user u on n.editor_id=u.id " \
                  " order by n.create_time desc limit %s,%s"
            # 偏移量的计算方式，每页10个，那第一页就是从第一条开始，偏移量就是0，所以要page-1
            cursor.execute(sql, [(page - 1) * 10, 10])
            result = cursor.fetchall()
            return result  # Result -> [(1, '新闻标题1', '要闻', 'scott')]
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                # 归还连接
                con.close()

    @staticmethod
    # 计算所有新闻的总页数
    def count_news_pages():
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            # 结果除以10且向上进位，例如21条就是21/10=2.1也就是3页
            sql = 'select ceil(count(*)/10) from t_news'
            cursor.execute(sql)
            page = cursor.fetchone()[0]
            return page
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    # 按照id删除新闻
    def delete_news_by_id(news_id):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = 'delete from t_news where id=%s'
            cursor.execute(sql, [news_id])
            con.commit()
        except Exception as e:
            if 'con' in dir():
                con.rollback()
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    # 添加一条新闻
    def insert(title, editor_id, type_id, content_id, is_top):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = 'insert into t_news(title, editor_id, type_id, content_id, is_top, state)' \
                  'values (%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, [title, editor_id, type_id, content_id, is_top, '待审批'])
            con.commit()
        except Exception as e:
            if 'con' in dir():
                con.rollback()
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    # 找到要被缓存的新闻/记录 -> 新闻信息，类型信息，创建者信息（三表联查）
    def search_target_cache(news_id):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'select n.title,u.username,t.type,n.content_id,n.is_top,n.create_time from t_news n ' \
                  'join t_type t on n.type_id = t.id join t_user u on n.editor_id=u.id where n.id=%s'
            cursor.execute(sql, [news_id])
            result = cursor.fetchone()
            return result
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    # 根据id查找新闻
    def search_news_by_id(news_id):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'select n.title,t.type,n.is_top from t_news n ' \
                  'join t_type t on n.type_id = t.id where n.id=%s'
            cursor.execute(sql, [news_id])
            result = cursor.fetchone()
            return result
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    def update_news(news_id, title, type_id, content_id, is_top):
        try:
            con = pool.get_connection()
            con.start_transaction()
            cursor = con.cursor()
            sql = "update t_news set title=%s,type_id=%s,content_id=%s,is_top=%s,state=%s," \
                  "update_time=NOW() where id=%s"
            cursor.execute(sql, [title, type_id, content_id, is_top, '待审批', news_id])
            con.commit()
        except Exception as e:
            if 'con' in dir():
                con.rollback()
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    def search_content_id(news_id):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'select content_id from t_news where id=%s'
            cursor.execute(sql, [news_id])
            result = cursor.fetchone()[0]
            return result
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()
