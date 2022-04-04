from .mysql_db import pool


class TypeDao:

    @staticmethod
    # 打印用户角色选项
    def print_type_list():
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = 'select id, type from t_type order by id'
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error: ", e)
        finally:
            if 'con' in dir():
                con.close()
