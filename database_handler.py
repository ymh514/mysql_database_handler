import pymysql
import os
import time
import math

EXIST_DEBUG_FLAG = 1

class SqlString:
    class_dict = {
        'Picture': 'picture',
        'Video': 'video',
        'Music': 'music',
        'Document': 'document',
        'Other': 'other'}
    type_dict = {
        'mp3': 'Music',
        'aac': 'Music',
        'flac': 'Music',
        'ogg': 'Music',
        'wma': 'Music',
        'm4a': 'Music',
        'aiff': 'Music',
        'wav': 'Music',
        'amr': 'Music',
        'flv': 'Video',
        'ogv': 'Video',
        'avi': 'Video',
        'mp4': 'Video',
        'mpg': 'Video',
        'mpeg': 'Video',
        '3gp': 'Video',
        'mkv': 'Video',
        'ts': 'Video',
        'webm': 'Video',
        'vob': 'Video',
        'wmv': 'Video',
        'png': 'Picture',
        'jpeg': 'Picture',
        'gif': 'Picture',
        'jpg': 'Picture',
        'bmp': 'Picture',
        'svg': 'Picture',
        'webp': 'Picture',
        'psd': 'Picture',
        'tiff': 'Picture',
        'txt': 'Document',
        'pdf': 'Document',
        'doc': 'Document',
        'docx': 'Document',
        'odf': 'Document',
        'xls': 'Document',
        'xlsv': 'Document',
        'xlsx': 'Document',
        'ppt': 'Document',
        'pptx': 'Document',
        'ppsx': 'Document',
        'odp': 'Document',
        'odt': 'Document',
        'ods': 'Document',
        'md': 'Document',
        'json': 'Document',
        'csv': 'Document'}

    def __init__(self):
        print()

    def convert_size(self,size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def getCreateSummaryTableStr(self):
        sql_str = "CREATE TABLE summary(id INT NOT NULL AUTO_INCREMENT,type VARCHAR(20) NOT NULL,name VARCHAR(100) NOT NULL,mtime DATETIME NOT NULL,size VARCHAR(20) NOT NULL,path VARCHAR(80) NOT NULL,PRIMARY KEY (id))"
        return sql_str

    def getCreateClassTableStr(self, class_name):
        sql_str = "CREATE TABLE "
        sql_str += self.class_dict[class_name]
        sql_str += "(id INT NOT NULL AUTO_INCREMENT,summary_id INT UNSIGNED NOT NULL,PRIMARY KEY (id));"
        return sql_str

    def getInsertSummaryTableStr(self, path, file):
        path += "/"

        filename, file_extension = os.path.splitext(file)

        file_extension = file_extension.strip('.')

        mtime = os.stat(path + file).st_mtime
        mtime2 = time.localtime(mtime)
        mtime2_hr = time.strftime("%m/%d/%Y %H:%M:%S", mtime2)

        ## 5. type 1. name 2. mtime 3. size 4. path
        summary_sql = "INSERT INTO summary(type,name,mtime,size,path) VALUES(\""

        if file_extension in self.type_dict:
            summary_sql += self.type_dict[file_extension]
        else:
            summary_sql += "Other"

        summary_sql += "\",\""
        summary_sql += file
        summary_sql += "\",STR_TO_DATE(\""
        summary_sql += mtime2_hr
        summary_sql += "\",\"%m/%d/%Y %T\"),\""
        summary_sql += self.convert_size(os.stat(path + file).st_size)
        summary_sql += "\", \""
        summary_sql += path
        summary_sql += "\")"

        return summary_sql

    def getInsertTypeTableStr(self, type):  # 傳入大寫了

        class_sql = "INSERT INTO "
        class_sql += self.class_dict[type]
        class_sql += "(summary_id) SELECT id FROM summary WHERE type = \""
        class_sql += type
        class_sql += "\";"
        return class_sql


class DatabaseHandler:
    class_dict = {
        'Picture': 'picture',
        'Video': 'video',
        'Music': 'music',
        'Document': 'document',
        'Other': 'other'}

    def __init__(self):
        self._database = pymysql.connect(
            "localhost", "root", "root", "mydatabase")
        self._cursor = self._database.cursor()
        self._sql = SqlString()

    def createTables(self):

        # summary table
        sql_str = self._sql.getCreateSummaryTableStr()

        try:
            self._cursor.execute(sql_str)
            self._database.commit()
        except BaseException:
            if (EXIST_DEBUG_FLAG == 1):
                print("Summary Table Already Exist")
            self._database.rollback()

        # Create Tables
        for index in self.class_dict:
            # create each table
            class_sql_str = self._sql.getCreateClassTableStr(index)

            try:
                self._cursor.execute(class_sql_str)
                self._database.commit()
            except BaseException:
                if (EXIST_DEBUG_FLAG == 1):
                    print(
                        index +
                        " Table Already Exist")
                self._database.rollback()

    def searchPath(self, path):
        fileList = os.listdir(path)
        for file in fileList:
            fullpath = os.path.join(path, file)
            if os.path.isdir(fullpath):
                self.searchPath(fullpath)
            elif os.path.isfile(fullpath):
                self.insertFileToSummaryTable(path, file)

    def insertFileToSummaryTable(self, path, file):

        insert_summary_sql_str = self._sql.getInsertSummaryTableStr(path, file)
        try:
            self._cursor.execute(insert_summary_sql_str)
            self._database.commit()
        except:
            # if errot occure
            self._database.rollback()

    def insertSummaryIdToTypeTable(self):
        for index in self.class_dict:
            insert_type_sql_str = self._sql.getInsertTypeTableStr(index)
            try:
                self._cursor.execute(insert_type_sql_str)
                self._database.commit()
            except:
                # if errot occure
                self._database.rollback()


    def checkPath(self, path):
        self.createTables()
        self.searchPath(path)
        self.insertSummaryIdToTypeTable()

    def clearAll(self):
        try:
            self._cursor.execute("drop table document;")
            self._cursor.execute("drop table music;")
            self._cursor.execute("drop table other;")
            self._cursor.execute("drop table picture;")
            self._cursor.execute("drop table video;")
            self._cursor.execute("drop table summary;")

            self._database.commit()
        except:
            # if errot occure
            self._database.rollback()


dd = DatabaseHandler()
# dd.clearAll()
dd.checkPath("/home/apteam/Desktop/MySQLTestFiles")