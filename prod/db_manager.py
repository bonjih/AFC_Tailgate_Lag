__author__ = "Ben Hamilton - Titan ICT Consultants"
__email__ = "ben.hamilton@titanict.com.au"
__phone__ = "+61 7 3360 4900"
__license__ = "xxx"
__version__ = "1.0.0"
__maintainer__ = "Anglo American"
__status__ = "Dev"

import pymysql as pymysql  # db connection module, change to suite db type
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd


# import MySQLdb
# db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)

def db_creds_json(j_configs):
    global user, passwd, host, database
    user = j_configs[2]
    passwd = j_configs[3]
    host = j_configs[4]
    database = j_configs[5]


#engine = create_engine('mysql+pymysql://debian-sys-maint:SoLcxvfgbzqU0ixI@10.6.66.160/anglo?charset=utf8')




# strips for tuple for if/than statement in check_entry_exist()
def remove_extra_char_in_values(res_value):
    res_value = str(res_value)[1:-1]
    res_value = res_value.replace("'", "")
    res_value = res_value.replace(",", "")
    return res_value


try:
    def db_connect():
        global conn, cursor, engine
        engine = create_engine('mysql+pymysql://' + user + ':' + passwd + '@' + host + '/' + database + '?charset=utf8')
        conn = pymysql.connect(user=user, passwd=passwd, host=host, database=database)
        cursor = conn.cursor()

    # check if file name entry exists in db, if so skip
    def check_entry_exist(img_configs):
        print(img_configs)
        cursor.execute('SELECT file_name FROM TailgateImageAnalysis WHERE file_name = %s', img_configs[1])
        exits = cursor.fetchone()
        exits = remove_extra_char_in_values(exits)

        if img_configs[1] == exits:
            return True
        if img_configs[1] != exits:
            return False

    # meta_data and cv_data are tuples
    def image_data(img_data, db_fields):

        df = pd.DataFrame(img_data)
        df = df.transpose()
        df.columns = db_fields
        df.to_sql('TailgateImageAnalysis', con=engine, if_exists='append', index=False)

        # create image ID
        # image ID is created from file name + SQL auto increment id
        # cursor.execute('SELECT id FROM TailgateImageAnalysis WHERE file_name = %s', file_name)
        # id_tup = cursor.fetchone()
        # print(id_tup)
        # ids = remove_extra_char_in_values(id_tup)
        # name = file_name[:-4]
        # image_id = '{}{}'.format(str(name), str(ids))
        # cursor.execute('UPDATE TailgateImageAnalysis SET image_id = %s WHERE file_name = %s', (image_id, file_name))
        #
        # conn.commit()
        print("'{}', with ID '{}' has been added to the database".format(img_data[8], img_data[11]))


except TypeError as e:
    print("Database empty:{}".format(e))

except Exception as e:
    print("Exception: database connection error occurred, please check connection credentials:{}".format(e))
