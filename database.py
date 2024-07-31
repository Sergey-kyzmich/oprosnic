import sqlite3

class database():
    def __init__(self) -> None:
        pass



    def add_data(self, data):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        id = len(list(cursor.execute("SELECT id from opr")))+1
        cursor.execute(f'INSERT INTO opr VALUES (?,?,?,?,?,?,?,?,?,?)', (
                                                             id, 
                                                             data["audio"],
                                                             data["year"],
                                                             data["1"], 
                                                             data["2"], 
                                                             data["3"], 
                                                             data["4"], 
                                                             data["5"], 
                                                             data["6"], 
                                                             data["7"],))
        db.commit()
        db.close()



    def create_db(self):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS opr (
        id INTEGER PRIMARY KEY,
        audio STRING,
        year STRING,
        opr1 STRING,
        opr2 STRING,
        opr3 STRING,
        opr4 STRING,
        opr5 STRING,
        opr6 STRING,
        opr7 STRING
        )
        ''')

        db.close()
    
    def edit(self, id, data):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        # data -> {"name": value}
        for item in data:
            if data[item]==None:
                cursor.execute(f'''UPDATE opr SET {item} = NULL WHERE id = "{id}"''')
            else:
                print(f'''UPDATE opr SET {item if item not in ["1","2","3","4","5","6","7"] else "opr"+item} = '{data[item]}' WHERE id = "{id}"''')
                cursor.execute(f'''UPDATE opr SET {item if item not in ["1","2","3","4","5","6","7"] else "opr"+item} = '{data[item]}' WHERE id = "{id}"''')
            db.commit()
        db.close()
    
    def get_all(self):
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        res = cursor.execute(f"SELECT * FROM opr")
        a = []
        for item in res:
            a.append(item)
        return a

    def get_line(self, id):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        res = cursor.execute(f'SELECT * FROM opr WHERE id = "{id}"')
        for i in res:
            db.close()
            print(f"{i=}")
            return i
        
    def get_column(self, column):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        res = cursor.execute(f"SELECT {column} FROM opr")
        a = []
        for i in res:
            a.append(i[0])
        db.close()
        return a
    

    def len_db(self):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        a = len(list(cursor.execute(f"SELECT id from opr")))
        db.close()
        return a
    
    def delete(self, id):
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute(f'DELETE FROM opr WHERE id = "{id}"');db.commit()
        db.close()
