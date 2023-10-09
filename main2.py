import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from DQL import * 
import DML
import logging
logging.basicConfig(filename='shop.log',filemode="a", level=logging.INFO ,format='%(asctime)s %(filename)s - %(message)s')
import mysql.connector

TOKEN = '6251144299:AAEJpQTSgWIkNCCREZ84Ooc-EAuwsQFO880'

knownUsers = []  
userStep = {}  
admins = [1359391742]

commands = {  # command description used in the "help" command
    'start'       : 'شروع مجدد ربات',
    'help'        : 'اطلاعاتی در مورد دستورات موجود به شما می دهد',
    'show_products'   : 'نمایش محصولات فروشگاه',
    'show_order'  :  'نمایش فاکتور',
    'support'     : 'جهت ارتباط با پشتیبانی',
    'home'        : 'باگشت به صفحه اصلی',
    'about us'     : 'جهت اطلاعات بیشتر درباره فروشگاه ما'
} 


admin_commands = {
    'show_users'    : 'get list of users',
}

bot = telebot.TeleBot(TOKEN)

def listener(messages):
    for m in messages:
        
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text + " [" + str(m.message_id) + "]")
bot.set_update_listener(listener)


def forward_message(channel_id, message_id, chat_id):
    try:
        bot.forward_message(chat_id, channel_id, message_id,)
        print("The message has been forwarded!")
    except Exception as e:
        print("Error forwarding message:", str(e))




def gen_markup(number,product_name):
    markup = types.InlineKeyboardMarkup(row_width=3)
    if number > 0:
        markup.add(types.InlineKeyboardButton('-1', callback_data=f"decrease_{product_name}_{number-1}"),
                   types.InlineKeyboardButton(f'تعداد مورد نظر: {str(number)}',  callback_data=f"quantity_{product_name}"),
                   types.InlineKeyboardButton("+1", callback_data=f"increase_{product_name}_{number+1}"))
    else:
        markup.add(types.InlineKeyboardButton(f'تعداد: {str(number)}',  callback_data=f"quantity_{product_name}"),
                   types.InlineKeyboardButton('+1',callback_data=f"increase_{product_name}_{number+1}"))
    markup.add(types.InlineKeyboardButton('افزودن به سبد خرید', callback_data=f'add_{product_name}_{number}'))
    return markup
    
    

@bot.message_handler(commands=['start'])    
def start_command(message: telebot.types.Message):
    logging.info(f'{message.chat.first_name}')
    cid = message.chat.id 
    user_name= message.from_user.first_name 
    knownUsers.append(cid) 
    userStep[cid] = 0  
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton('help', callback_data="help"))
    bot.send_message(cid, f" سلام {user_name} عزیز به فروشگاه تلگرامی ریا سخت افزار خوش امدید 🌟🎉", reply_markup=markup)
    forward_message("@shoppmahdii", 28, 1359391742)
    #mention = "["+user_name+"](tg://user?id="+str(user_id)+")"
    menu(message)

    

def menu(m):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    keyboard.add('نمایش و خرید محصولات','نمایش سبد کالا','نمایش فاکتور','درباره ما','پشتیبانی ')
    bot.send_message(m.chat.id,'"جهت خرید از فروشگاه یا موارد این چنین یکی از موارد زیرا انتخاب کنید 🙏 "',reply_markup=keyboard)

@bot.message_handler(commands=['show_products'])
def show_products(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton('لپ تاپ 💻', callback_data='laptop'),
                InlineKeyboardButton('موبایل 📱', callback_data='phone'),
                  InlineKeyboardButton('پردازنده🏼', callback_data="Processors/CPUs"),
                    InlineKeyboardButton('مانیتور 🖥', callback_data="Computer Monitors"),
                        InlineKeyboardButton('سایر محصولات', callback_data="other products"))
    bot.send_message(message.chat.id, 'محصولات فروشگاه :', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_callback(call: telebot.types.CallbackQuery):
    cid = call.message.chat.id
    help_text = "دستورات زیر در دسترس هستند: \n"
    for key in commands:  
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)

@bot.callback_query_handler(func=lambda call: call.data.startswith(("increase", "decrease", "add")))
def handle_quantity_callback(call):
    action, product_name ,number= call.data.split("_")
    number = int(number)
    rows=select_data(product_name)
    product_id=rows[0]
    product_name = rows[1]
    product_inventory = rows[3]
    product_price=rows[4]
    if rows:
        if action == "increase":
            if number<=product_inventory:
                product_inventory -=1
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=gen_markup(number,product_name))
                bot.answer_callback_query(call.id, 'افزایش محصول ➕')
            else:
                bot.answer_callback_query(call.id, 'تعداد محصول مورد نظر در انبار موجود نمی باشد ❌')

        if action=="decrease":
            product_inventory +=1
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=gen_markup(number,product_name))
            bot.answer_callback_query(call.id, 'کاهش محصول ➖')

        if action=="add":
            if number!=0:
                user_id = call.from_user.id
                add_to_cart(user_id,product_id,product_name,number,product_price)
                bot.answer_callback_query(call.id, "محصول انتخاب شده به سبد کالا اضافه شد✅🛒")
                update_product_inventory(product_inventory,product_id)
                print("The product number has been updated successfully")
                order_button = InlineKeyboardButton("ثبت سفارش", callback_data="order")
                products_button = InlineKeyboardButton("برگشت به منوی محصولات", callback_data="other products")
                keyboard = [[order_button, products_button]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(call.message.chat.id, "برای ثبت سفارش، دکمه زیر را فشار دهید:", reply_markup=reply_markup)
            else:
                bot.answer_callback_query(call.id, f"خطا🚫| تعداد محصول نباید {number} باشد")

@bot.callback_query_handler(func=lambda call: call.data == "order")

def get_firstname(call):
    bot.send_message(call.message.chat.id, "لطفاً نام خود را وارد کنید:")
    bot.register_next_step_handler(call.message, get_lastname)

def get_lastname(message):
    firstname = message.text
    bot.send_message(message.chat.id, "لطفاً نام خانوادگی خود را وارد کنید:")
    bot.register_next_step_handler(message, lambda msg: get_username(msg, firstname))

def get_username(message, firstname):
    lastname = message.text
    username = message.from_user.username
    cid=message.chat.id
    add_score(cid, 1)
    save_user_data(cid, firstname, lastname, username, 1)
    bot.send_message(message.chat.id, "اطلاعات شما با موفقیت ذخیره شد.")


@bot.callback_query_handler(func=lambda call: call.data == 'laptop')
def show_products_callback(call: telebot.types.CallbackQuery):
    try:
        cid = call.message.chat.id 
        userStep[cid] = 1 
        rows = get_laptop_products()
        keyboard = InlineKeyboardMarkup()
        for row in rows:
            product_name = row[0]
            product_button = InlineKeyboardButton(product_name, callback_data=product_name)
            keyboard.add(product_button)
        bot.send_message(call.message.chat.id, 'لیست لپ‌تاپ‌ها💻:', reply_markup=keyboard)
        #forward_message("@shoppmahdii", 23, cid,reply_markup=keyboard)   
    except:
        bot.send_message(call.message.chat.id, f'🚫 | خطا در اجرای فرمان')

@bot.callback_query_handler(func=lambda call: call.data == 'phone')
def show_products_callback(call: telebot.types.CallbackQuery):
    try:
        cid = call.message.chat.id 
        userStep[cid] = 1 
        rows = get_phone_products()
        keyboard = InlineKeyboardMarkup()
        for row in rows:
            product_name = row[0]
            product_button = InlineKeyboardButton(product_name, callback_data=product_name)
            keyboard.add(product_button)
        bot.send_message(call.message.chat.id, 'لیست موبایل‌ها 📱:', reply_markup=keyboard)
            
    except:
        bot.send_message(call.message.chat.id, f'🚫 | خطا در اجرای فرمان')

@bot.callback_query_handler(func=lambda call: call.data == 'Processors/CPUs')
def show_products_callback(call: telebot.types.CallbackQuery):
    try:
        cid = call.message.chat.id 
        userStep[cid] = 1 
        rows = get_Processors_products()
        keyboard = InlineKeyboardMarkup()
        for row in rows:
            product_name = row[0]
            product_button = InlineKeyboardButton(product_name, callback_data=product_name)
            keyboard.add(product_button)
        bot.send_message(call.message.chat.id, 'لیست پردازنده‌ها🏼:', reply_markup=keyboard)   
    except:
        bot.send_message(call.message.chat.id, f'🚫 | خطا در اجرای فرمان')

@bot.callback_query_handler(func=lambda call: call.data == 'Computer Monitors')
def show_products_callback(call: telebot.types.CallbackQuery):
    try:
        cid = call.message.chat.id 
        userStep[cid] = 1 
        rows = get_Monitors_products()
        keyboard = InlineKeyboardMarkup()
        for row in rows:
            product_name = row[0]
            product_button = InlineKeyboardButton(product_name, callback_data=product_name)
            keyboard.add(product_button)
        bot.send_message(call.message.chat.id, 'لیست مانیتور‌ها🖥:', reply_markup=keyboard)   
    except:
        bot.send_message(call.message.chat.id, f'🚫 | خطا در اجرای فرمان')

@bot.callback_query_handler(func=lambda call: call.data == 'other products')
def show_products_callback(call: telebot.types.CallbackQuery):
    try:
        cid = call.message.chat.id 
        userStep[cid] = 1 
        rows = get_others_products()
        keyboard = InlineKeyboardMarkup()
        for row in rows:
            product_name = row[0]
            product_button = InlineKeyboardButton(product_name, callback_data=product_name)
            keyboard.add(product_button)
        bot.send_message(call.message.chat.id, 'سایر محصولات فروشگاه :', reply_markup=keyboard)   
    except:
        bot.send_message(call.message.chat.id, f'🚫 | خطا در اجرای فرمان')



@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    data=call.data
    product_data = select_data(data)
    if product_data:
        product_name = product_data[1]
        product_description = product_data[2]
        product_photo_path = product_data[7]
        product_inventory = product_data[3]
        product_price=product_data[4]
        bot.send_message(call.message.chat.id, f"محصول انتخاب شده: {product_name}")
        bot.send_message(call.message.chat.id, f"تعداد محصول مورد نظر در انبار: {product_inventory}")
        with open(product_photo_path, "rb") as file:
            bot.send_photo(call.message.chat.id, file, caption=f'توضیحات محصول :{product_description}\n قیمت محصول {product_price}',reply_markup=gen_markup(0,product_name))
    if data=="other products":
        show_products(call.message)
    elif data=="empty_cart":
        user_id = call.from_user.id
        empty_cart(user_id)
        bot.send_message(call.message.chat.id, "سبد کالای شما خالی شد ✅🛒")

@bot.message_handler(commands=['support'])
def support_handler(message):
    cid = message.chat.id
    user_id = message.from_user.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('پشتیبانی', url=f'tg://user?id=@fcmahdii'))
#   markup.add(InlineKeyboardButton('پشتیبانی', url=f'tg://user?id={user_id}'))
    bot.send_message(cid, 'لطفا با [پشتیبانی](tg://user?id=1359391742) یا [mahdi-e.m@yahoo.com](https://mail.yahoo.com/) در ارتباط باشید ', parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['show_order'])
def show_order_handler(message):
    user_id = message.from_user.id
    rows = select_from_cart(user_id)
    total_price = 0
    order_details = ""
    for row in rows:
        product_name = row[3]
        quantity = row[4]
        product_price = row[5]
        subtotal = product_price * quantity
        total_price += subtotal
        order_details += f"محصول: {product_name}\nقیمت: {product_price}\nتعداد محصول: {quantity}\n\n"
    insert_into_order(user_id, total_price)
    keyboard = InlineKeyboardMarkup()
    the_payment = InlineKeyboardButton("پرداخت", callback_data="payment")
    keyboard.add(the_payment)
    order_details += f"مجموع قیمت: {total_price}"

    bot.send_message(message.chat.id, order_details, reply_markup=keyboard)

def show_cart(message):
    user_id = message.from_user.id
    result = select_from_cart(user_id)
    if not result:
        bot.send_message(message.chat.id, 'سبد خرید شما خالی است.❌🛒')
        return
    total_price = 0 
    cart_message = 'سبد خرید شما:\n\n'
    for product in result:
        product_name = product[3]
        quantity = product[4]
        product_price = product[5]
        cart_message += f'🛒🛒 {product_name}: {product_price} تومان x {quantity}\n'
        total_price += product_price * quantity
        
    cart_message += f'\nمجموع: {total_price} تومان'
    keyboard = InlineKeyboardMarkup()
    empty_cart = InlineKeyboardButton("خالی کردن سبد کالا🛒", callback_data="empty_cart")
    keyboard.add(empty_cart)
    bot.send_message(message.chat.id, cart_message,reply_markup=keyboard) 
@bot.message_handler(commands=['home'])
def show_home(message):
    menu(message)


@bot.message_handler(func=lambda message: True)
def keyboard_callback(m):
    if m.text=='نمایش و خرید محصولات':
        show_products(m)
    if m.text=='نمایش فاکتور':
        show_order_handler(m)
    if m.text=='نمایش سبد کالا':
        show_cart(m)
    if m.text=='درباره ما':
        forward_message("@shoppmahdii", 10, 1359391742)
    if m.text=='پشتیبانی':
        support_handler(m)




bot.infinity_polling()
