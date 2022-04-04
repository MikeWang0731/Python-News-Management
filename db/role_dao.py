from .mysql_db import pool


class RoleDao:

    @staticmethod
    # 打印用户角色选项
    def print_role_list():
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'select id, role from t_role'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()

