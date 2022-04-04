from .mysql_db import pool


# 上面引用文件 - 使用相对引用
class UserDao:

    # 新闻管理员登陆
    @staticmethod
    def login(username, password):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            # 如果能在user表里查询到这个用户和对应的密码，那就是登陆成功，即返回的记录等于1条
            sql = "select count(*) from t_user where username=%s and aes_decrypt(unhex(password),'HelloWorld')=%s"
            cursor.execute(sql, [username, password])
            result = cursor.fetchone()[0]
            return True if result == 1 else False
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                # 归还连接
                con.close()

    # 查询用户角色
    @staticmethod
    def search_user_role(username):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            # 查询某个user的职位
            sql = "select r.role from t_user u join t_role r on u.role_id=r.id " \
                  "where u.username = %s"
            cursor.execute(sql, [username])
            result = cursor.fetchone()[0]
            return result
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                # 归还连接
                con.close()

    @staticmethod
    def add_user(username, password, email, role_id):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            # 添加一个用户
            sql = "insert into t_user(username,password,email,role_id) " \
                  "value (%s,hex(aes_encrypt(%s,'HelloWorld')),%s,%s)"
            cursor.execute(sql, [username, password, email, role_id])
            con.commit()
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                # 归还连接
                con.close()

    @staticmethod
    # 获取用户列表的总页数（10个/页）
    def user_count_page():
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'select ceil(count(*)/10) from t_user'
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    # 打印所有用户
    def print_all_user(page):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'select u.id,username,r.role from t_user u join t_role r on u.role_id=r.id ' \
                  'order by u.id limit %s,%s'
            cursor.execute(sql, [(page - 1) * 10, 10])
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    # 更新用户信息
    def update_user_information(user_id, username, password, email, role_id):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            con.start_transaction()
            sql = "update t_user set username=%s, password=hex(aes_encrypt(%s,'HelloWorld')), email=%s, role_id=%s " \
                  "where id=%s"
            cursor.execute(sql, [username, password, email, role_id, user_id])
            con.commit()
        except Exception as e:
            if 'con' in dir():
                con.rollback()
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    # 删除用户信息
    def delete_user(user_id):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            con.start_transaction()
            sql = "delete from t_user where id=%s"
            cursor.execute(sql, [user_id])
            con.commit()
        except Exception as e:
            if 'con' in dir():
                con.rollback()
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

    @staticmethod
    # 查询用户id
    def search_user_id(username):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'select id from t_user where username=%s'
            cursor.execute(sql, [username])
            result = cursor.fetchone()[0]
            return result
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()
