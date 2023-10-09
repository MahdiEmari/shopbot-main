import mysql.connector
mydict={}

config = {'user': 'root', 'password': '1381.m', 'host': 'localhost', 'database': 'shopping'}

def get_users():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True) 
        SQL_Query = """SELECT * FROM user""" 
        cursor.execute(SQL_Query)
        res = cursor.fetchall()    
        name = res[0]
        print(name)
        conn.close()
    except mysql.connector.Error as error:
        print("Error connecting to the database: {}".format(error))
        return None

def select_from_cart(user_id):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cart where user_id=%s", (user_id,))
        result = cursor.fetchall()
        conn.close()  
        return result
    except mysql.connector.Error as error:
        print("Error connecting to the database: {}".format(error))
        return None

    

def empty_cart(user_id):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print



def select_data(product_name):   
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM product WHERE name = %s", (product_name,))
        rows = cursor.fetchone()
        conn.close()  
        return rows
    except mysql.connector.Error as error:
        print("Error connecting to the database: {}".format(error))
        return None

def get_laptop_products():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor() 
        SQL_Query = """SELECT name FROM shopping.product WHERE category="Laptops/Notebooks";""" 
        cursor.execute(SQL_Query)
        rows = cursor.fetchall() 
        conn.close()
        return rows
    except mysql.connector.Error as error:
        print("Error connecting to the database: {}".format(error))
        return None

def get_phone_products():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor() 
        SQL_Query = """SELECT name FROM shopping.product WHERE category="phone";""" 
        cursor.execute(SQL_Query)
        rows = cursor.fetchall() 
        conn.close()
        return rows
    except mysql.connector.Error as error:
        print("Error connecting to the database: {}".format(error))
        return None



def add_to_cart(user_id,product_id,product_name, quantity,price):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    query = "INSERT INTO cart (user_id,product_id,product_name, quantity,price) VALUES (%s,%s, %s,%s,%s)"
    try:
        cursor.execute(query, (user_id,product_id,product_name, quantity,price))
        conn.commit()
        return True
    except Exception as e:
        print

def update_product_inventory(inventory,product_id):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("UPDATE product SET inventory= %s WHERE Product_ID= %s", (inventory, product_id))
    conn.commit()

def get_Processors_products():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor() 
        SQL_Query = """SELECT name FROM shopping.product WHERE category="Processors/CPUs";""" 
        cursor.execute(SQL_Query)
        rows = cursor.fetchall() 
        conn.close()
        return rows
    except mysql.connector.Error as error:
        print("Error connecting to the database: {}".format(error))
        return None





def save_user_data(cid,first_name,last_name,username,Score ):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor() 
    query = "INSERT INTO user (cid,first_name,last_name,username,Score) VALUES (%s,%s, %s,%s,%s)"
    try:
        cursor.execute(query, (cid,first_name,last_name, username,Score))
        conn.commit()
        return True
    except Exception as e:
        print

def add_score(user_id, score):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM scores WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    if user:
        new_score = user[1] + score
        cursor.execute("UPDATE scores SET score=%s WHERE user_id=%s", (new_score, user_id))
        print('score updated')
    else:
        cursor.execute("INSERT INTO scores (user_id, score) VALUES (%s, %s)", (user_id, score))
    conn.commit()

def get_score(user_id):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM scores WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    if user:
        return user[1]
    else:
        return 0
    
def get_Monitors_products():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor() 
        SQL_Query = """SELECT name FROM shopping.product WHERE category="Computer Monitors";""" 
        cursor.execute(SQL_Query)
        rows = cursor.fetchall() 
        conn.close()
        return rows
    except mysql.connector.Error as error:
        print("Error connecting to the database: {}".format(error))
        return None

def get_others_products():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor() 
        SQL_Query = """SELECT name FROM shopping.product WHERE category="other";""" 
        cursor.execute(SQL_Query)
        rows = cursor.fetchall() 
        conn.close()
        return rows
    except mysql.connector.Error as error:
        print("Error connecting to the database: {}".format(error))
        return None





def insert_into_order(cust_ID, total_pric):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor() 
    query = "INSERT INTO orders (cust_ID,total_price) VALUES (%s, %s)"
    try:
        cursor.execute(query, (cust_ID, total_pric))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    



if __name__ == "__main__":
    pass
