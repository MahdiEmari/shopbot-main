import mysql.connector
from BotData import *


def connected_databases():
    try:
        conn = mysql.connector.connect(**{'user': 'root', 'password': '1381.m', 'host': 'localhost'})
        print('Connection successful')
    except mysql.connector.Error as e:
        print(f'Error connecting to the database: {e}')

def create_database(name):
    try:
        conn = mysql.connector.connect(**{'user': 'root', 'password': '1381.m', 'host': 'localhost'})
        cursor = conn.cursor()
        cursor.execute(f'''DROP DATABASE IF EXISTS {name}''')
        conn.commit()
        cursor.execute(f'''CREATE DATABASE IF NOT EXISTS {name}''')
        print('database created')
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print(e)

def create_user_table():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS User (
                    cid          BIGINT         PRIMARY KEY,    
                    first_name   VARCHAR(100),
                    last_name    VARCHAR(255),
                    username     VARCHAR(50),
                    Score       TINYINT    DEFAULT 0,
                    date         TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
                    );
                    '''
                    )
        print('table created')
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print(e)
    
def create_product_table():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS product (
                Product_ID      INT             AUTO_INCREMENT,
                name            VARCHAR(255),
                description     VARCHAR(255),
                inventory       TINYINT         NOT NULL DEFAULT 0,
                price           DECIMAL(10, 2),
                category        VARCHAR(255),
                date            TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
                photo_path      VARCHAR(255),
                PRIMARY KEY (Product_ID)
                );
                '''
                )
    print('table Product created')
    conn.commit()
    cursor.close()
    conn.close()

def create_orders_table():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                order_ID        INT             AUTO_INCREMENT,
                cust_ID         BIGINT,
                total_price     DECIMAL(10, 2),
                date            TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (order_ID),
                FOREIGN KEY (cust_ID) REFERENCES user(cid)
                );
                '''
                )
    print('table orders created')
    conn.commit()
    cursor.close()
    conn.close()
def create_cart_table():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute('''
                CREATE TABLE cart (
                cart_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                product_id INT,
                product_name VARCHAR(255),
                quantity INT,
                price    FLOAT,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES product(Product_ID)
                );
                '''
                )
    print('table orderlines created')
    conn.commit()
    cursor.close()
    conn.close()

def Score(): 
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor() 
    cursor.execute('''CREATE TABLE scores
            (user_id INTEGER PRIMARY KEY, score INTEGER)''')   
    print('table scores created')  
    conn.commit()
    cursor.close()
    conn.close()   


def drop_user_table():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS User""")
    print('table droped')
    conn.commit()
    cursor.close()
    conn.close()
    
def drop_product_table():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS product""")
    print('table droped')
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    connected_databases()
    create_database(database_name)
    drop_user_table()
    create_user_table()
#   drop_product_table()
    create_product_table()
    create_orders_table()
    Score()
    create_cart_table()


