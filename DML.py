import mysql.connector
from BotData import *

def insert_user_info(cid, first_name, last_name, username):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor() 
    SQL_Query = """INSERT INTO User (cid, first_name, last_name, username)
    VALUES (%s, %s, %s, %s); """
    cursor.execute(SQL_Query, (cid, first_name, last_name, username))
    print(f'data for {first_name} inserted to table')
    conn.commit()
    cursor.close()
    conn.close()
def insert_product_info(name, description, inventory, price,category,photo_path):
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor() 
        check_query = "SELECT * FROM product WHERE name = %s"
        cursor.execute(check_query, (name,))
        if cursor.fetchone():
            print('Meghdar tekrare ast')
        else:
            SQL_Query = """INSERT IGNORE INTO product (name, description, inventory, price,category,photo_path)
            VALUES (%s, %s, %s, %s,%s,%s); """
            cursor.execute(SQL_Query, (name, description, inventory, price,category,photo_path))
            print(f'data for {name} inserted to product table')
        conn.commit()
        cursor.close()
        conn.close()



def delete_user(cid):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM User WHERE cid=%s;
    """, (cid,))
    print('score updated')
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    """insert_user_info(684464963, 'ali', 'ahmadi', 'ali_ahmadi')
    insert_user_info(541686541, 'akbar', 'asghari', 'akbar_asghari')
    insert_user_info(46861116, 'mamad', 'asghari', 'mamad_asghari')
    update_user_score(684464963, 10)"""
    insert_product_info('Intel Core i7', '12700K Alder Lake 3.6GHz Twelve-Core LGA 1700 Boxed Processor', 5, 29.700,"Processors/CPUs",'Data/images/Intel Core i7.jpg')
    insert_product_info('Intel Core i5', '10400F Desktop Processor 6 Cores up to 4.3 GHz Without Processor Graphics LGA1200r', 3, 11.500,"Processors/CPUs",'Data/images/Intel Core i5.jpg')
    insert_product_info('AMD Ryzen™ 9', '5900X 12-core, 24-Thread Unlocked Desktop Processor', 2, 32.900,"Processors/CPUs",'Data/images/AMD Ryzen™ 9.jpg')
    insert_product_info('AMD Ryzen™ 7','7700X Raphael AM5 4.5GHz 8-Core Boxed Processor',3,34.700,"Processors/CPUs",'Data/images/AMD Ryzen™ 7.jpg')
    insert_product_info('Lenovo ThinkPadE15','E15 i7-1255U -Gen 4 15.6 Laptop Computer - Gray',3,89.300,"Laptops/Notebooks",'Data/images/Lenovo ThinkPadE15.jpg')
    insert_product_info('HP EliteBook','Intel Core i5 12th Gen 1235U 1.3GHz Processor and 16GB DDR4-3200 RAM ',3,64.900,"Laptops/Notebooks",'Data/images/HP EliteBook.jpg')
    insert_product_info('ASUS ZenBookPro14','Intel Core i9 12th Gen 12900H 1.8GHz Processor,RTX 3050 Ti 4GB GDDR6',3,229.900,"Laptops/Notebooks",'Data/images/ASUS ZenBookPro14.jpg')
    insert_product_info('Dell Inspiron16Plus','Intel Core i7 12th Gen 12700H 1.7GHz Processor,16GB DDR5-4800 RAM',2,139.900,"Laptops/Notebooks",'Data/images/Dell Inspiron16Plus.jpg')
    insert_product_info('ASUS VG32AQL1A31.5','2K QHD (2560 x 1440) 170Hz Gaming Monitor',4,34.900,"Computer Monitors",'Data/images/ASUS VG32AQL1A31.5.jpg')
    insert_product_info('LG 32UN650','G8 G85NB 32" 4K Ultra HD (3840 x 2160) 240Hz Curved Screen Monitor',4,42.900,"Computer Monitors",'Data/images/LG 32UN650.jpg')
    insert_product_info('Samsung Odyssey Neo','G8 G85NB 32" 4K Ultra HD (3840 x 2160) 240Hz Curved Screen Monitor',2,139.900,"Computer Monitors",'Data/images/Samsung Odyssey Neo.jpg')
    insert_product_info('iPhone 11',' 64GB, Black - Unlocked (Renewed)',2,290.17,"phone",'Data/images/Apple iPhone 11.jpg')
    insert_product_info('Samsung Galaxy S21',' 5G, US Version, 128GB, Phantom Gray - Unlocked (Renewed)',3,249.99,"phone",'Data/images/Samsung Galaxy S21.jpg')
    insert_product_info('iPhone 15 Pro Max',' (512 GB) - Blue Titanium | [Locked] | Boost Infinite plan required starting at $60/mo. | Unlimited Wireless',2,139.90,"phone",'Data/images/Apple iPhone 15.jpg')
    insert_product_info('Samsung Galaxy S20','FE 5G, 128GB, Cloud Navy - Unlocked (Renewed)',2,189.00,"phone",'Data/images/Samsung Galaxy S20.jpg')
    insert_product_info('Computer Keyboard Wired','Plug Play USB Keyboard, Low Profile Chiclet Keys, Large Number Pad, Caps Indicators, Foldable Stands, Spill-Resistant, Anti-Wear Letters for Windows Mac PC Laptop, Full Size',4,11.5,"other",'Data/images/Computer Keyboard Wired.jpg')
    insert_product_info('Gaming Keyboard','Redragon K551 Mechanical Gaming Keyboard RGB LED Rainbow Backlit Wired Keyboard with Red Switches for Windows Gaming PC (104 Keys, Black)',2,37.5,"other",'Data/images/Gaming Keyboard.jpg')
    insert_product_info('GK-XLI Gaming Mouse','Wired, Lightweight Gaming Mice, Breathing RGB Plug Play High-Precision Adjustable 3200 DPI Ergonomic PC Gaming Mouse for Gamer',4,5.5,"other",'Data/images/GK-XLI Gaming Mouse.jpg')
    insert_product_info('RedragonM913 Gaming Mouse','Redragon M913 Impact Elite Wireless Gaming Mouse, 16000 DPI Wired/Wireless RGB Gamer Mouse with 16 Programmable Buttons, 45 Hr Battery and Pro Optical Sensor, 12 Side Buttons MMO Mouse',2,5.5,"other",'Data/images/RedragonM913 Gaming Mouse.jpg')
    insert_product_info('1TB USB QTDFOQTD','1TB USB Flash Drive USB Drive for Laptop/Computer Gold',3,19.5,"other",'Data/images/1TB USB QTDFOQTD.jpg')
    insert_product_info('Vansuny 128GB USB','Type-C Flash Drive 2-in-1 Dual Flash Drive USB A + USB C OTG Flash Drive for Android Smartphone Tablet Computer Laptop (Blue)',2,11.7,"other",'Data/images/Vansuny 128GB USB.jpg')
    # delete_user(46861116)
