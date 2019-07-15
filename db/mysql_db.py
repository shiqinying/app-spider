import pymysql
from config import *


class MySQL:
    def __init__(
        self,
        database,
        host=MYSQL_HOST,
        username=MYSQL_USER,
        password=MYSQL_PWD,
        port=MYSQL_PORT,
    ):
        """
        MySQL初始化
        :param host:
        :param username:
        :param password:
        :param port:
        :param database:
        """
        try:
            self.db = pymysql.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database,
                charset="utf8",
            )
            self.cursor = self.db.cursor()
        except pymysql.MySQLError as e:
            print(e.args)

    def insert(self, table, item):
        """
        插入数据
        :param table:
        :param item:
        :return:
        """
        keys = ",".join(item.keys())
        values = ",".join(["%s"] * len(item))
        sql_query = "insert ignore into {table} ({keys}) values ({values})".format(
            table=table, keys=keys, values=values
        )
        try:
            self.cursor.execute(sql_query, tuple(item.values()))
            self.db.commit()
        except pymysql.MySQLError as e:
            print(e.args)
            self.db.rollback()

    def close(self):
        self.db.close()


if __name__ == "__main__":

    """
    使用方法：
    1 使用前需要创建数据库，表，设计字段
    2 初始化建立连接，程序执行完毕关闭连接
    try:
        mysql = MySQL(database="xxx")
        mysql.insert('table','item')
    finally:
        mysql.close()
    """

    sql = """
    CREATE TABLE IF NOT EXISTS `tiam`(
    `id` int(11) primary key not null AUTO_INCREMENT,
    `actor` varchar (255),
    `title` varchar (255) not null unique , # unique插入时的去重字段，ingnore对其起作用
    `video_url` varchar (255) not null unique , # unique插入时的去重字段，ingnore对其起作用
    `click_times` varchar (255)  ,
    `release_date` varchar (255)  ,
    `category` varchar (255) ,
    `image_url` varchar (255)  ,
    `info` varchar (255)
    );
    """
    mysql = MySQL(database="xxx")
    try:
        mysql.cursor.execute(sql)
        mysql.db.commit()
    except pymysql.MySQLError as e:
        print(e.args)
        mysql.db.rollback()
    finally:
        mysql.close()
