import sqlite3

class DataBaseManager:
    def __init__(self,dbname):
        self.conn = None
        self.cursor = None
        self.dbname=dbname
    def open(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
    def close(self):
        self.cursor.close()
        self.conn.close()
    
    def get_all_todos(self,user_id):
        self.open()
        self.cursor.execute('''SELECT * FROM Todo WHERE user=?''',[user_id])
        data = self.cursor.fetchall()
        self.close()
        return data
    
        
    def get_all_completed_todos(self,user_id,datecompleted):
        self.open()
        self.cursor.execute('''SELECT * FROM Todo WHERE (user=? AND datecompleted IS NOT NULL)''',[user_id,datecompleted])
        data = self.cursor.fetchall()
        self.close()
        return data


    def add_article(self,title,memo,user,important):
        self.open()
        self.cursor.execute('''INSERT INTO Todo (title,memo,user,important) VALUES(?,?,?,?)''',[title,memo,user,important])
        self.conn.commit()
        self.close()
    def save_article(self,title,memo,id):
        self.open()
        self.cursor.execute('''UPDATE Todo SET title=?,memo=? WHERE ID=? ''',[title,memo,id])
        self.conn.commit()
        self.close()

    def get_article(self,id):
        self.open()
        self.cursor.execute('''SELECT * FROM Todo WHERE ID=? ''' ,[id]) 
        data = self.cursor.fetchone()
        self.close()
        return data

    def complete_todo(self,completed,datecompleted,id):
        self.open()
        self.cursor.execute('''UPDATE Todo SET completed=? WHERE ID=? ''',[completed,id])
        self.cursor.execute('''UPDATE Todo SET datecompleted=? WHERE ID=? ''',[datecompleted,id])
        self.conn.commit()
        self.close()
    
    def delete_todo(self,id):
        self.open()
        self.cursor.execute('''DELETE FROM Todo WHERE ID=? ''',[id])
        self.conn.commit()
        self.close()
    
    def createuser(self,login,password):
        self.open()
        self.cursor.execute('''SELECT * FROM Users WHERE login=?''',[login])
        user = self.cursor.fetchone()
        if user:
            self.close()
            return False
        else:
            self.cursor.execute('''INSERT INTO Users (login,password) VALUES(?,?)''',[login,password])
            self.conn.commit()
            self.close()
            return True


    
    def get_user(self,id):
        self.open()
        self.cursor.execute('''SELECT * FROM Users WHERE id=? ''' ,[id]) 
        data = self.cursor.fetchone()
        self.close()
        return data
    
    def check_user(self,login,password):
        self.open()
        self.cursor.execute('''SELECT * FROM Users WHERE (login=? AND password=?)''',[login,password])
        data = self.cursor.fetchone()
        self.close()
        return data