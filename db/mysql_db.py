"""
定义全局的数据库连接池
"""
import mysql.connector.pooling

# 将数据库连接信息定义为私有变量
__config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'wzy980731',
    'database': 'vega'
}

# 创建连接池
try:
    pool = mysql.connector.pooling.MySQLConnectionPool(**__config, pool_size=5)
except Exception as e:
    print("Error: ", e)
