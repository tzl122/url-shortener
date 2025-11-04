import sqlite3
import string,random

class db:
    def __init__(self):
        conn=self.get_db
        cursor=conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id TEXT,
            url TEXT             
                       )
""")
        conn.commit()
        conn.close()

    @property
    def get_db(self):
       return sqlite3.connect("data/data.db")

    @staticmethod
    def get_id(length=6):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))
    
    
    def add_url(self,urll):
        conn=self.get_db
        cursor=conn.cursor()
        idd=self.get_id()
        cursor.execute("SELECT id FROM links")
        ids=cursor.fetchall()
        while (idd, ) in ids:
            idd=self.get_id()
        cursor.execute("INSERT INTO links (id,url) VALUES (?,?)",(str(idd),urll))
        conn.commit()
        conn.close()
        return str(idd)
    

    def delete_url(self,idd):
        conn=self.get_db
        cursor=conn.cursor()
        cursor.execute("SELECT id FROM links")
        ids=cursor.fetchall()
        if (idd, ) in ids:
            cursor.execute("DELETE FROM links WHERE id = ?", (idd, ))
            conn.commit()
            conn.close()
        else:
            conn.close()    
    @property
    def get_data(self):
        conn=self.get_db
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM links")
        data=cursor.fetchall()
        conn.close()
        return data
    
    def get_url(self,id):
        conn=self.get_db
        cursor=conn.cursor()
        cursor.execute("SELECT url FROM links WHERE id = ?", (id, ))
        url=cursor.fetchone()
        conn.close()
        if url:
            return url[0]
        else:
            return None