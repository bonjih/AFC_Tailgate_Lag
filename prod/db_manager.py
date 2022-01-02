__author__ = ""
__email__ = ""
__phone__ = ""
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = ""
__status__ = "Dev"

import pymysql as pymysql  # db connection module, change to suite db type
from sqlalchemy import create_engine
import pandas as pd


class SQL:
    def __init__(self, user, pwd, host, db):
        self.user = user
        self.pwd = pwd
        self.host = host
        self.db = db
        self.engine = create_engine('mysql+pymysql://' + user + ':' + pwd + '@' + host + '/' + db + '?charset=utf8')
        self.conn = pymysql.connect(user=self.user, passwd=self.pwd, host=self.host, database=self.db)

    def check_entry_exist(self, img_date):
        cur = self.conn.cursor()
        cur.execute('SELECT file_name FROM TailgateImageAnalysis WHERE file_name = %s', img_date)
        exits = cur.fetchone()
        if exits is None:
            return False
        if img_date == exits[0]:
            return True
        if img_date != exits[0]:
            return False

    def image_data(self, img_data, db_fields):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO TailgateImageAnalysis (date_time) VALUES (CURRENT_TIMESTAMP)", )
        df = pd.DataFrame(img_data)
        df = df.transpose()
        df.columns = db_fields
        df.to_sql('TailgateImageAnalysis', con=self.engine, if_exists='append', index=False)

        print("'{}', with ID '{}' has been added to the database".format(img_data[8], img_data[11]))

