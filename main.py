import telebot
import requests
import threading
import time
import os
import random
import string
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- ⚠️ إعدادات الهوية والبوت الأساسية (SpiderSmsX_1) ---
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8891688659:AAFEsRsfQYvm_6NhNwugIBZB84gz5j_O9tQ")
ADMIN_ID = 8672817508                # الـ ID بتاعك كمدير للبوت 👑

# 🔑 بيانات الحسابات لموقع Durian 
DURIAN_ACCOUNTS = [
    ["Abdelhadi2005", "OXgwaDJnNXIraDByNEVxRXFsNWVEUT09"],
    ["Abdelhadi2005", "OXgwaDJnNXIraDByNEVxRXFsNWVEUT09"]
]

# 📢 المعرفات والروابط الرسمية المثبتة للمشروع
CHANNEL_USER = "@Spider_Sms_Channels"
CHANNEL_URL = "https://t.me/Spider_Sms_Channels"
SUPPORT_URL = "https://t.me/SpiderSmsX_1"
# -----------------------------------------------------------------

# تعريف المتغيرات أولاً لمنع الـ NameError
user_hunting_targets = {}
hunting_active = False
active_hunted_numbers = {}
admin_state = {}
USER_PURCHASE_COOLDOWN = {}

BALANCES_FILE = "balances.txt"
PROMOS_FILE = "promos.txt"
ORDERS_FILE = "orders.txt"
PRICES_FILE = "prices.txt"
BANNED_FILE = "banned.txt"
REFERRALS_FILE = "referrals.txt"

USER_BALANCES = {}
SETTINGS = {
    "rate": 50.0, 
    "wallet": "01028520360", # رقم الكاش الفريش الخاص بك 📱
    "binance_id": "123456789", 
    "pid": "0257", 
    "ref_reward": 0.01 
}
PROMO_CODES = {}
USER_ORDERS = {}
BANNED_USERS = set()
USED_REFERRALS = set()

SYSTEM_STATS = {"total_sales": 0.0, "successful_orders": 0, "failed_orders": 0}

ALL_COUNTRIES = {
    "مصر": {"code": "eg", "price": 0.25, "flag": "🇪🇬"}, "روسيا": {"code": "ru", "price": 0.25, "flag": "🇷🇺"},
    "أمريكا": {"code": "us", "price": 0.25, "flag": "🇺🇸"}, "الهند": {"code": "in", "price": 0.25, "flag": "🇮🇳"},
    "تونس": {"code": "tn", "price": 0.25, "flag": "🇹🇳"}, "الأرجنتين": {"code": "ar", "price": 0.25, "flag": "🇦🇷"},
    "الجزائر": {"code": "dz", "price": 0.25, "flag": "🇩🇿"}, "ليبيا": {"code": "ly", "price": 0.25, "flag": "🇱🇾"},
    "سوريا": {"code": "sy", "price": 0.25, "flag": "🇸🇾"}, "الأردن": {"code": "jo", "price": 0.25, "flag": "🇯🇴"},
    "الإمارات": {"code": "ae", "price": 0.25, "flag": "🇦🇪"}, "جنوب إفريقيا": {"code": "tz", "price": 0.25, "flag": "🇿🇦"},
    "نيجيريا": {"code": "ng", "price": 0.25, "flag": "🇳🇬"}, "تايلاند": {"code": "th", "price": 0.25, "flag": "🇹🇭"},
    "المكسيك": {"code": "mx", "price": 0.25, "flag": "🇲🇽"}, "باكستان": {"code": "pk", "price": 0.25, "flag": "🇵🇰"},
    "موريتانيا": {"code": "mr", "price": 0.25, "flag": "🇲🇷"}, "الكونغو الديمقراطية": {"code": "cd", "price": 0.25, "flag": "🇨🇩"},
    "أنغولا": {"code": "ao", "price": 0.25, "flag": "🇦🇴"}, "أفغانستان": {"code": "af", "price": 0.25, "flag": "🇦🇫"},
    "تنزانيا": {"code": "tz", "price": 0.25, "flag": "🇹🇿"}, "جمهورية الدومينيكان": {"code": "do", "price": 0.25, "flag": "🇩🇴"},
    "موزمبيق": {"code": "mz", "price": 0.25, "flag": "🇲🇿"}, "الكاميرون": {"code": "cm", "price": 0.25, "flag": "🇨🇲"},
    "السنغال": {"code": "sn", "price": 0.25, "flag": "🇸🇳"}, "كينيا": {"code": "ke", "price": 0.25, "flag": "🇰🇪"},
    "الكونغو": {"code": "cg", "price": 0.25, "flag": "🇨🇬"}, "الفلبين": {"code": "ph", "price": 0.25, "flag": "🇵🇭"},
    "أوغندا": {"code": "ug", "price": 0.25, "flag": "🇺🇬"}, "زامبيا": {"code": "zm", "price": 0.25, "flag": "🇿🇲"},
    "توغو": {"code": "tg", "price": 0.25, "flag": "🇹🇬"}, "كمبوديا": {"code": "kh", "price": 0.25, "flag": "🇰🇭"},
    "بوركينا فاسو": {"code": "bf", "price": 0.25, "flag": "🇧🇫"}, "هايتي": {"code": "ht", "price": 0.25, "flag": "🇭🇹"},
    "مالاوي": {"code": "mw", "price": 0.25, "flag": "🇲🇼"}, "إثيوبيا": {"code": "et", "price": 0.25, "flag": "🇪🇹"},
    "فرنسا": {"code": "fr", "price": 0.25, "flag": "🇫🇷"}, "بورتوريكو": {"code": "pr", "price": 0.25, "flag": "🇵🇷"},
    "فيجي": {"code": "fj", "price": 0.25, "flag": "🇫🇯"}, "أستراليا": {"code": "au", "price": 0.25, "flag": "🇦🇺"},
    "سلوفاكيا": {"code": "sk", "price": 0.25, "flag": "🇸🇰"}, "إسبانيا": {"code": "es", "price": 0.25, "flag": "🇪🇸"},
    "ألمانيا": {"code": "de", "price": 0.25, "flag": "🇩🇪"}
}

bot = telebot.TeleBot(BOT_TOKEN, num_threads=4)

# --- 🌐 إعداد خادم الويب ومنظومة الحماية من النوم الإجباري ---
app = Flask(__name__)

@app.route('/')
def home():
    return "🟢 SPIDER SMS BOT IS LIVE AND RUNNING ULTRA 24/7 SUCCESSFULLY!"

def run_flask_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive_ping():
    time.sleep(30)
    port = os.environ.get("PORT", "8080")
    local_url = f"http://127.0.0.1:{port}/"
    while True:
        try:
            requests.get(local_url, timeout=5)
            print("⚡ [Keep-Alive] تم إرسال نبضة الإيقاظ بنجاح، السيرفر مستيقظ!")
        except:
            pass
        time.sleep(180)

# --- وظائف السيستم والبيانات ---
def load_all_data():
    global USER_BALANCES, SETTINGS, PROMO_CODES, USER_ORDERS, ALL_COUNTRIES, BANNED_USERS, SYSTEM_STATS, USED_REFERRALS
    if os.path.exists(BALANCES_FILE):
        try:
            with open(BALANCES_FILE, "r") as f:
                for line in f:
                    if ":" in line: u_id, bal = line.strip().split(":"); USER_BALANCES[int(u_id)] = float(bal)
        except: pass
    if os.path.exists(PROMOS_FILE):
        try:
            with open(PROMOS_FILE, "r") as f:
                for line in f:
                    if ":" in line: code, val = line.strip().split(":"); PROMO_CODES[code] = float(val)
        except: pass
    if os.path.exists(BANNED_FILE):
        try:
            with open(BANNED_FILE, "r") as f:
                for line in f: BANNED_USERS.add(int(line.strip()))
        except: pass
    if os.path.exists(REFERRALS_FILE):
        try:
            with open(REFERRALS_FILE, "r") as f:
                for line in f: USED_REFERRALS.add(int(line.strip()))
        except: pass
    if os.path.exists(PRICES_FILE):
        try:
            with open(PRICES_FILE, "r") as f:
                for line in f:
                    if ":" in line: c_name, pr = line.strip().split(":"); 
                    if c_name in ALL_COUNTRIES: ALL_COUNTRIES[c_name]["price"] = float(pr)
        except: pass
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r") as f:
                for line in f:
                    if "||" in line:
                        u_id, text = line.strip().split("||", 1); u_id = int(u_id);
                        if u_id not in USER_ORDERS: USER_ORDERS[u_id] = []
                        USER_ORDERS[u_id].append(text)
                        SYSTEM_STATS["successful_orders"] += 1
                        try:
                            price_part = text.split("سعر: ")[1].replace("$", "")
                            SYSTEM_STATS["total_sales"] += float(price_part)
                        except: pass
        except: pass

def save_data(mode):
    try:
        if mode == "balances":
            with open(BALANCES_FILE, "w") as f:
                for u_id, bal in USER_BALANCES.items(): f.write(f"{u_id}:{bal}\n")
        elif mode == "promos":
            with open(PROMO_CODES, "w") as f:
                for code, val in PROMO_CODES.items(): f.write(f"{code}:{val}\n")
        elif mode == "banned":
            with open(BANNED_FILE, "w") as f:
                for u_id in BANNED_USERS: f.write(f"{u_id}\n")
        elif mode == "referrals":
            with open(REFERRALS_FILE, "w") as f:
                for u_id in USED_REFERRALS: f.write(f"{u_id}\n")
        elif mode == "prices":
            with open(PRICES_FILE, "w") as f:
                for c_name, info in ALL_COUNTRIES.items(): f.write(f"{c_name}:{info['price']}\n")
    except: pass

def log_order(user_id, order_text):
    if user_id not in USER_ORDERS: USER_ORDERS[user_id] = []
    USER_ORDERS[user_id].append(order_text)
    try:
        with open(ORDERS_FILE, "a") as f: f.write(f"{user_id}||{order_text}\n")
    except: pass

def get_user_balance(user_id):
    if user_id not in USER_BALANCES: 
        USER_BALANCES[user_id] = 0.00
        save_data("balances")
    return USER_BALANCES[user_id]

def get_country_info_by_code(code):
    for name, info in ALL_COUNTRIES.items():
        if info["code"] == code: return name, info["price"], info["flag"]
    return f"دولة ({code})", 0.25, "🌍"

def check_user_joined_channel(user_id):
    if user_id == ADMIN_ID: return True
    try:
        member = bot.get_chat_member(CHANNEL_USER, user_id)
        if member.status in ['member', 'creator', 'administrator']: return True
    except: pass
    return False

def get_force_join_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📢 اشترك في القناة من هنا أولاً 📢", url=CHANNEL_URL),
        InlineKeyboardButton("🔄 ✅ تحقق من الاشتراك الحين", callback_data="check_join_btn")
    )
    return markup

def get_admin_dashboard_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("💰 شحن رصيد لزبون", callback_data="admin_add_balance"), InlineKeyboardButton("➖ سحب رصيد", callback_data="admin_sub_balance"))
    markup.add(InlineKeyboardButton("⚙️ إعدادات الأسعار والكاش", callback_data="admin_set_vars"), InlineKeyboardButton("🎫 توليد كود شحن", callback_data="admin_gen_promo"))
    markup.add(InlineKeyboardButton("🌍 تعديل سعر دولة", callback_data="admin_set_country_price"), InlineKeyboardButton("📊 تعديل جماعي للأسعار", callback_data="admin_mass_price"))
    markup.add(InlineKeyboardButton("👥 إدارة حظر زبون", callback_data="admin_manage_user"), InlineKeyboardButton("📢 إذاعة رسالة برودكاست", callback_data="admin_broadcast"))
    markup.add(InlineKeyboardButton("🔄 تنظيف الذاكرة والتعليق", callback_data="admin_clear_cache"), InlineKeyboardButton("🔄 تحديث لوحة التحكم", callback_data="admin_refresh_stats"))
    return markup

def get_admin_vars_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(f"📱 رقم الكاش الحالي ({SETTINGS['wallet']})", callback_data="none"),
        InlineKeyboardButton(f"💵 سعر الدولار الحالي ({SETTINGS['rate']} ج.م)", callback_data="edit_rate"),
        InlineKeyboardButton(f"🎯 كود المشروع الحالى ({SETTINGS['pid']})", callback_data="edit_pid"),
        InlineKeyboardButton("🔙 عودة للوحة الإدارة", callback_data="admin_back_main")
    )
    return markup

def get_user_manage_keyboard(target_id):
    markup = InlineKeyboardMarkup(row_width=2)
    ban_status = "🔴 حظر الزبون" if target_id not in BANNED_USERS else "🟢 فك الحظر عنه"
    markup.add(InlineKeyboardButton(ban_status, callback_data=f"banuser_{target_id}"))
    markup.add(InlineKeyboardButton("🔄 تصفير محفظته", callback_data=f"clearbal_{target_id}"))
    markup.add(InlineKeyboardButton("🔙 عودة", callback_data="admin_back_main"))
    return markup

def get_main_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("🎯 تفعيل الصيد التلقائي", callback_data="manage_hunting"))
    markup.add(InlineKeyboardButton("💰 إيداع / شحن", callback_data="deposit"), InlineKeyboardButton("📋 أرقامي المشتراة", callback_data="user_orders"))
    markup.add(InlineKeyboardButton("👥 رابط الإحالة والربح", callback_data="user_referral"), InlineKeyboardButton("🎫 شحن كود هدية", callback_data="user_redeem_promo"))
    markup.add(InlineKeyboardButton("👨‍💻 التواصل مع الدعم", url=SUPPORT_URL))
    return markup

def get_countries_keyboard(user_id, page=0):
    markup = InlineKeyboardMarkup(row_width=2)
    user_targets = user_hunting_targets.get(user_id, [])
    items = list(ALL_COUNTRIES.items())
    per_page = 10  
    start = page * per_page
    end = start + per_page
    
    for name, info in items[start:end]:
        code = info["code"]
        status = " 🎯 [جاري]" if code in user_targets else ""
        markup.add(InlineKeyboardButton(f"{info['flag']} {name}{status}", callback_data=f"hunt_{code}_{page}"))
        
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️ السابق", callback_data=f"hpage_{page-1}"))
    if end < len(items): nav.append(InlineKeyboardButton("التالي ➡️", callback_data=f"hpage_{page+1}"))
    if nav: markup.row(*nav)
    markup.add(InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_main"))
    return markup

def get_deposit_methods_keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📱 شحن عبر فودافون كاش (مصر)", callback_data="dep_vodafone"),
        InlineKeyboardButton("🪙 شحن عبر Binance Pay (عالمي)", callback_data="dep_binance"),
        InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_main")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in BANNED_USERS:
        bot.send_message(message.chat.id, "❌ **عذراً، لقد تم حظرك من استخدام البوت من قبل الإدارة.**")
        return

    start_args = message.text.split()
    if len(start_args) > 1 and user_id != ADMIN_ID:
        try:
            inviter_id = int(start_args[1].strip())
            if inviter_id != user_id and user_id not in USER_BALANCES and user_id not in USED_REFERRALS:
                reward = SETTINGS["ref_reward"]
                if reward > 0:
                    if inviter_id not in USER_BALANCES: USER_BALANCES[inviter_id] = 0.00
                    USER_BALANCES[inviter_id] += reward
                    save_data("balances")
                    USED_REFERRALS.add(user_id)
                    save_data("referrals")
                    try: bot.send_message(inviter_id, f"🎉 <b>دخل زبون جديد عبر رابط إحالتك!</b>\n💰 المكافأة: <b>+{reward}$</b>")
                    except: pass
        except: pass

    if not check_user_joined_channel(user_id):
        bot.send_message(message.chat.id, f"⚠️ <b>يجب الاشتراك في قناة البوت الرسمية أولاً لتفعيل الحساب!</b>", reply_markup=get_force_join_keyboard(), parse_mode="HTML")
        return
        
    if user_id == ADMIN_ID:
        admin_text = (
            f"👑 <b>مرحباً بك يا مدير في لوحة التحكم الإدارية الفائقة</b>\n\n"
            f"📊 <b>إحصائيات السيستم التراكمية والحية:</b>\n"
            f"• إجمالي الزبائن: <code>{len(USER_BALANCES)}</code>\n"
            f"• إجمالي أرصدة الزبائن: <code>{sum(USER_BALANCES.values()):.2f} $</code>\n"
            f"• مبيعات البوت الناجحة: <code>{SYSTEM_STATS['total_sales']:.2f} $</code>\n"
            f"• عدد الأرقام المباعة: <code>{SYSTEM_STATS['successful_orders']} رقم</code>\n"
            f"• محاولات حجز ملغية/فاشلة: <code>{SYSTEM_STATS['failed_orders']} محاولة</code>"
        )
        bot.send_message(message.chat.id, admin_text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")
    else:
        welcome_text = f"• <u><b>🕸️ 𝕾𝕻𝕴𝕯𝕰𝕽 𝕾𝕸𝕾 🕷️ - Auto Hunting Bot</b></u> •\n\n💰 <b>رصيدك الحالي:</b> {get_user_balance(user_id):.2f} $\n\n🆔 الـ ID الخاص بك: <code>{user_id}</code>"
        bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    user_id = call.from_user.id
    if user_id in BANNED_USERS and user_id != ADMIN_ID: return

    try: bot.answer_callback_query(call.id)
    except: pass

    if call.data == "check_join_btn":
        if check_user_joined_channel(user_id):
            welcome_text = f"• <u><b>🕸️ 𝕾𝕻𝕴𝕯𝕰𝕽 𝕾𝕸𝕾 🕷️ - Auto Hunting Bot</b></u> •\n\n💰 <b>رصيدك الحالي:</b> {get_user_balance(user_id):.2f} $\n\n🆔 الـ ID الخاص بك: <code>{user_id}</code>"
            bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")
        else:
            try: bot.send_message(user_id, "❌ لسه مشركتش في القناة يا غالي! اشترك أولاً.")
            except: pass
        return

    if not check_user_joined_channel(user_id) and user_id != ADMIN_ID: return

    if user_id == ADMIN_ID:
        if call.data == "admin_back_main":
            admin_text = (
                f"👑 <b>مرحباً بك يا مدير في لوحة التحكم الإدارية الفائقة</b>\n\n"
                f"📊 <b>إحصائيات حية:</b>\n"
                f"• إجمالي الزبائن: <code>{len(USER_BALANCES)}</code>\n"
                f"• إجمالي الأرصدة: <code>{sum(USER_BALANCES.values()):.2f} $</code>\n"
                f"• مبيعات البوت: <code>{SYSTEM_STATS['total_sales']:.2f} $</code>"
            )
            bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=admin_text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")
            return
        elif call.data == "admin_clear_cache":
            global active_hunted_numbers
            active_hunted_numbers.clear()
            bot.send_message(user_id, "🔄 تم تنظيف الذاكرة التخزينية بنجاح!")
            return
        elif call.data == "admin_set_vars":
            bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text="⚙️ **إعدادات ومغيرات السيستم من التليجرام:**", reply_markup=get_admin_vars_keyboard(), parse_mode="Markdown")
            return
        elif call.data in ["edit_rate", "edit_pid"]:
            admin_state[user_id] = {"mode": "edit_var", "var": call.data.replace("edit_", "")}
            bot.send_message(user_id, "✍️ أرسل القيمة الجديدة الآن:")
            return
        elif call.data == "admin_add_balance":
            msg = bot.send_message(user_id, "✍️ أرسل **ID حساب الزبون** للشحن:")
            bot.register_next_step_handler(msg, process_admin_target_id, "add")
            return
        elif call.data == "admin_sub_balance":
            msg = bot.send_message(user_id, "✍️ أرسل **ID حساب الزبون** للخصم:")
            bot.register_next_step_handler(msg, process_admin_target_id, "sub")
            return
        elif call.data == "admin_gen_promo":
            admin_state[user_id] = {"mode": "gen_promo"}
            bot.send_message(user_id, "✍️ أدخل قيمة كود الشحن بالدولار:")
            return
        elif call.data == "admin_mass_price":
            admin_state[user_id] = {"mode": "mass_price"}
            bot.send_message(user_id, "✍️ أدخل السعر الموحد الجديد لجميع الدول:")
            return
        elif call.data == "admin_manage_user":
            admin_state[user_id] = {"mode": "query_user"}
            bot.send_message(user_id, "✍️ أرسل الـ ID الخاص بالزبون:")
            return
        elif call.data.startswith("banuser_"):
            t_id = int(call.data.split("_")[1])
            if t_id in BANNED_USERS: BANNED_USERS.remove(t_id); bot.send_message(user_id, "🟢 تم فك الحظر")
            else: BANNED_USERS.add(t_id); bot.send_message(user_id, "🔴 تم حظر الزبون")
            save_data("banned")
            return
        elif call.data.startswith("clearbal_"):
            t_id = int(call.data.split("_")[1])
            USER_BALANCES[t_id] = 0.00
            save_data("balances")
            bot.send_message(user_id, "🔄 تم تصفير المحفظة بنجاح")
            return
        elif call.data == "admin_set_country_price":
            admin_state[user_id] = {"mode": "set_country_select"}
            bot.send_message(user_id, "✍️ اكتب اسم الدولة بالظبط:")
            return
        elif call.data == "admin_broadcast":
            msg = bot.send_message(user_id, "📢 اكتب رسالة البرودكاست لإذاعتها:")
            bot.register_next_step_handler(msg, process_admin_broadcast)
            return
        elif call.data == "admin_refresh_stats":
            admin_text = (
                f"👑 <b>لوحة التحكم المحدثة الفائقة</b>\n\n"
                f"📊 <b>إحصائيات حية:</b>\n"
                f"• إجمالي الزبائن: <code>{len(USER_BALANCES)}</code>\n"
                f"• إجمالي الأرصدة: <code>{sum(USER_BALANCES.values()):.2f} $</code>"
            )
            bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=admin_text, reply_markup=get_admin_dashboard_keyboard(), parse_mode="HTML")
            return

    if call.data == "manage_hunting":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🌍 **قسم الصيد التلقائي لأرقام التليجرام:**", reply_markup=get_countries_keyboard(user_id, page=0), parse_mode="Markdown")
        return
    elif call.data.startswith("hpage_"):
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=get_countries_keyboard(user_id, page=int(call.data.split("_")[1])))
        return
    elif call.data.startswith("hunt_"):
        parts = call.data.split("_")
        code, page = parts[1], int(parts[2])
        if user_id not in user_hunting_targets: user_hunting_targets[user_id] = []
        name, price, _ = get_country_info_by_code(code)
        
        if code not in user_hunting_targets[user_id] and get_user_balance(user_id) <= 0:
            bot.send_message(user_id, "❌ محفظتك فارغة! يرجى الشحن أولاً.")
            return
        if code in user_hunting_targets[user_id]:
            user_hunting_targets[user_id].remove(code)
        else:
            user_hunting_targets[user_id].append(code)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=get_countries_keyboard(user_id, page=page))
        return

    elif call.data == "user_referral":
        bot_info = bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
        ref_text = f"👥 <b>برنامج إحالة وربح رصيد مجاني</b>\n\n🔗 <code>{ref_link}</code>\n\n💰 ستحصل على <b>{SETTINGS['ref_reward']:.2f}$</b> لكل صديق جديد يشترك!"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="back_to_main"))
        bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=ref_text, reply_markup=markup, parse_mode="HTML")
        return

    elif call.data == "deposit":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="💳 **الرجاء اختيار طريقة الإيداع المناسبة لك للشحن:**", reply_markup=get_deposit_methods_keyboard(), parse_mode="Markdown")
        return

    elif call.data == "dep_vodafone":
        deposit_text = f"📱 <b>شحن الرصيد عبر فودافون كاش</b>\n\n📱 رقم الكاش: <code>{SETTINGS['wallet']}</code>\n💵 الحسبة: 1$ = {SETTINGS['rate']} جنيه."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="deposit"))
        bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=deposit_text, reply_markup=markup, parse_mode="HTML")
        return

    elif call.data == "dep_binance":
        binance_text = f"🪙 <b>شحن الرصيد عبر Binance Pay</b>\n\n🆔 معرف بايننس: <code>{SETTINGS['binance_id']}</code>"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="deposit"))
        bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=binance_text, reply_markup=markup, parse_mode="HTML")
        return

    elif call.data == "user_redeem_promo":
        admin_state[user_id] = {"mode": "redeem_promo"}
        bot.send_message(user_id, "🎫 أدخل كود الهدية الخاص بك هنا:")
        return

    elif call.data == "user_orders":
        orders = USER_ORDERS.get(user_id, [])
        if not orders: bot.send_message(user_id, "📋 ليس لديك أرقام مشتراة.")
        else:
            text = "📋 **سجل أرقامك المشتراة السابقة:**\n\n" + "\n\n".join(orders[-10:])
            bot.send_message(user_id, text)
        return

    elif call.data == "back_to_main":
        welcome_text = f"• <u><b>🕸️ 𝕾𝕻𝕴𝕯𝕰𝕽 𝕾𝕸𝕾 🕷️ - Auto Hunting Bot</b></u> •\n\n💰 <b>رصيدك الحالي:</b> {get_user_balance(user_id):.2f} $\n\n🆔 الـ ID الخاص بك: <code>{user_id}</code>"
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")
        return
    
    elif call.data.startswith("claim_"):
        current_time = time.time()
        last_purchase_time = USER_PURCHASE_COOLDOWN.get(user_id, 0)
        
        if current_time - last_purchase_time < 5:
            bot.send_message(user_id, "⚠️ يرجى الانتظار 5 ثوانٍ بين محاولات الشراء.")
            return

        parts = call.data.split("_")
        phone = parts[1]
        acc_index = int(parts[2])
        
        if phone in active_hunted_numbers:
            target_info = active_hunted_numbers[phone]
            price = float(target_info['price'])
            
            if get_user_balance(user_id) >= price:
                USER_PURCHASE_COOLDOWN[user_id] = current_time
                del active_hunted_numbers[phone]
                
                loading_markup = InlineKeyboardMarkup()
                loading_markup.add(InlineKeyboardButton("10%", callback_data="none"))
                bot.edit_message_text(
                    chat_id=user_id, 
                    message_id=call.message.id, 
                    text=f"🔄 <b>جاري فحص وحجز الرقم من السيرفر الصيني...</b>\n📱 الرقم: <code>[ جاري التأمين... * * * * * * * * * ]</code>", 
                    reply_markup=loading_markup, 
                    parse_mode="HTML"
                )
                
                threading.Thread(target=wait_for_sms, args=(user_id, phone, price, acc_index, call.message.id, target_info['country'], target_info['flag']), daemon=True).start()
            else:
                bot.send_message(user_id, "❌ رصيدك غير كافٍ للشراء!")
        else:
            bot.send_message(user_id, "❌ الرقم تم بيعه أو انتهت صلاحيته!")

# --- ⚙️ معالجة الرسائل النصية للإدارة ---
@bot.message_handler(func=lambda msg: msg.from_user.id in admin_state)
def handle_states(message):
    user_id = message.from_user.id
    state = admin_state[user_id]
    text = message.text.strip()
    
    if state.get("mode") == "edit_var":
        var = state["var"]
        if var == "rate": SETTINGS["rate"] = float(text)
        elif var == "pid": SETTINGS["pid"] = text
        bot.send_message(user_id, f"✅ تم تحديث {var} بنجاح الحين!")
        del admin_state[user_id]
        
    elif state.get("mode") == "gen_promo":
        try:
            val = float(text)
            code = "PULSE-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            PROMO_CODES[code] = val
            bot.send_message(user_id, f"🎫 **تم توليد كود الشحن بنجاح:**\n\n`{code}`\n\n💰 قيمته: **{val}$**")
        except: bot.send_message(user_id, "❌ قيمة غير صحيحة.")
        del admin_state[user_id]
        
    elif state.get("mode") == "mass_price":
        try:
            new_pr = float(text)
            for c_name in ALL_COUNTRIES: ALL_COUNTRIES[c_name]["price"] = new_pr
            save_data("prices")
            bot.send_message(user_id, f"✅ تم تحديث أسعار الدول لتكون موحدة: **{new_pr}$**!")
        except: bot.send_message(user_id, "❌ القيمة غير صحيحة.")
        del admin_state[user_id]
        
    elif state.get("mode") == "query_user":
        try:
            t_id = int(text)
            t_bal = get_user_balance(t_id)
            ban_text = "⚠️ محظور" if t_id in BANNED_USERS else "🟢 نشط"
            info_msg = f"👤 **بيانات حساب الزبون:**\n\n• رصيده الحالى: **{t_bal:.2f} $**\n• حالة الحساب: **{ban_text}**"
            bot.send_message(user_id, info_msg, reply_markup=get_user_manage_keyboard(t_id))
        except: bot.send_message(user_id, "❌ الـ ID غير صحيح.")
        del admin_state[user_id]
        
    elif state.get("mode") == "set_country_select":
        if text in ALL_COUNTRIES:
            admin_state[user_id] = {"mode": "set_country_price_val", "c_name": text}
            bot.send_message(user_id, f"💰 أدخل السعر الجديد لدولة {text} بالدولار:")
        else:
            bot.send_message(user_id, "❌ اسم الدولة غير موجود.")
            del admin_state[user_id]
            
    elif state.get("mode") == "set_country_price_val":
        try:
            pr = float(text)
            c_name = state["c_name"]
            ALL_COUNTRIES[c_name]["price"] = pr
            save_data("prices")
            bot.send_message(user_id, f"✅ تم تغيير سعر دولة **{c_name}** بنجاح إلى **{pr}$**!")
        except: bot.send_message(user_id, "❌ قيمة السعر غير صحيحة.")
        del admin_state[user_id]
        
    elif state.get("mode") == "redeem_promo":
        if text in PROMO_CODES:
            val = PROMO_CODES[text]
            if user_id not in USER_BALANCES: USER_BALANCES[user_id] = 0.00
            USER_BALANCES[user_id] += val
            del PROMO_CODES[text]
            save_data("balances")
            bot.send_message(user_id, f"🎉 **تم شحن الكود بنجاح!**\n💰 أُضيف إلى محفظتك: **+{val}$**")
        else: bot.send_message(user_id, "❌ كود غير صحيح أو مستخدم.")
        del admin_state[user_id]

def release_bad_number(phone_number, acc_index):
    acc = DURIAN_ACCOUNTS[acc_index]
    try:
        url = f"https://api.durianrcs.com/out/ext_api/cancelMobile?name={acc[0]}&ApiKey={acc[1]}&pn={phone_number}&pid={str(SETTINGS['pid'])}&serial=2"
        requests.get(url, timeout=5)
    except: pass

def is_number_banned_on_telegram(phone_number, acc_index):
    acc = DURIAN_ACCOUNTS[acc_index]
    try:
        check_url = f"https://api.durianrcs.com/out/ext_api/getMsg?name={acc[0]}&ApiKey={acc[1]}&pn={phone_number}&pid={str(SETTINGS['pid'])}&serial=2"
        res = requests.get(check_url, timeout=4).json()
        res_str = str(res).lower()
        if res.get("code") == 905 or "block" in res_str or "ban" in res_str or "password" in res_str or "verify" in res_str or "email" in res_str:
            return True
    except: pass
    return False

def global_auto_buyer():
    global hunting_active
    hunting_active = True
    while hunting_active:
        for u_id, targets_list in list(user_hunting_targets.items()):
            if get_user_balance(u_id) <= 0 and len(targets_list) > 0:
                user_hunting_targets[u_id] = []
                try: bot.send_message(u_id, f"🛑 **تم إيقاف الصيد التلقائي لجميع الدول لأن رصيدك انتهى!**")
                except: pass

        active_codes = set()
        for targets_list in user_hunting_targets.values():
            for target_code in targets_list: active_codes.add(target_code)
                
        if not active_codes:
            time.sleep(1)
            continue

        for c_name, c_info in list(ALL_COUNTRIES.items()):
            country_code = c_info["code"]
            if country_code not in active_codes: continue
            
            for idx, acc in enumerate(DURIAN_ACCOUNTS):
                if "اسم_الحساب" in acc[0] or "مفتاح_API" in acc[1]: continue
                try:
                    url = f"https://api.durianrcs.com/out/ext_api/getMobile?name={acc[0]}&ApiKey={acc[1]}&cuy={country_code}&pid={str(SETTINGS['pid'])}&num=1&noblack=1&serial=2"
                    response = requests.get(url, timeout=4)
                    
                    if response.status_code == 200:
                        res_json = response.json()
                        if res_json.get("code") == 200:
                            phone_number = res_json.get("data")
                            
                            if is_number_banned_on_telegram(phone_number, idx):
                                release_bad_number(phone_number, idx)
                                continue
                                
                            price = c_info["price"]
                            flag = c_info["flag"]
                            active_hunted_numbers[phone_number] = {"country": c_name, "flag": flag, "price": price}
                            
                            for u_id, targets_list in list(user_hunting_targets.items()):
                                if u_id not in BANNED_USERS and check_user_joined_channel(u_id) and country_code in targets_list and get_user_balance(u_id) > 0:
                                    markup = InlineKeyboardMarkup()
                                    markup.add(InlineKeyboardButton("🛒 شراء الآن", callback_data=f"claim_{phone_number}_{idx}"))
                                    formatted_msg = f"🥳 🎰 <b>الدولة متاحة الآن</b>\n\n{flag} {c_name}\n✅ رقم جاهز وفريش تماماً!\n💰 سعر الشراء: <b>${price:.2f}</b>\n\n🛒 اضغط شراء الآن لحجزه فوراً"
                                    try: bot.send_message(u_id, formatted_msg, reply_markup=markup, parse_mode="HTML")
                                    except: pass
                            break
                except: pass
                time.sleep(0.5)
            time.sleep(0.5)

def wait_for_sms(user_id, phone_number, price, acc_index, status_msg_id, c_name, flag):
    acc = DURIAN_ACCOUNTS[acc_index]
    sms_url = f"https://api.durianrcs.com/out/ext_api/getMsg?name={acc[0]}&ApiKey={acc[1]}&pn={phone_number}&pid={str(SETTINGS['pid'])}&serial=2"
    
    loading_steps = ["10%", "30%", "60%", "90%", "100%"]
    for step in loading_steps:
        try:
            progress_markup = InlineKeyboardMarkup()
            progress_markup.add(InlineKeyboardButton(f"{step}", callback_data="none"))
            timer_text = f"🔄 <b>جاري تجهيز الخط... {step}</b>\n📱 الرقم: <code>[ جاري التأمين... * * * * * * * * * ]</code>"
            bot.edit_message_text(chat_id=user_id, message_id=status_msg_id, text=timer_text, reply_markup=progress_markup, parse_mode="HTML")
            time.sleep(0.3) 
        except: pass

    try:
        init_timer_text = (f"🎰 <b>تم حجز الرقم بنجاح!</b>\n\n"
                          f"🌍 <b>الدولة:</b> {flag} {c_name}\n"
                          f"📱 <b>الرقم المحجوز لك:</b> <code>{phone_number}</code>\n\n"
                          f"⏳ <b>جاري فحص وصول الكود الحين...</b>\n"
                          f"✨ <i>يرجى الانتظار، سيتم ترحيل الكود فور وصوله تلقائياً.</i>")
        bot.edit_message_text(chat_id=user_id, message_id=status_msg_id, text=init_timer_text, reply_markup=None, parse_mode="HTML")
    except: pass

    total_wait_seconds = 300  
    check_interval = 15       
    loops = total_wait_seconds // check_interval
    
    for i in range(loops):
        try:
            time.sleep(check_interval)

            if is_number_banned_on_telegram(phone_number, acc_index): break
                
            res = requests.get(sms_url, timeout=5).json()
            if res.get("code") == 200:
                sms_code = res.get("data")
                
                if user_id not in USER_BALANCES: USER_BALANCES[user_id] = 0.00
                USER_BALANCES[user_id] = max(0.00, USER_BALANCES[user_id] - price)
                save_data("balances")
                
                success_text = f"✅ <b>تم شراء الرقم واستلام الكود بنجاح!</b>\n\n{flag} {c_name}\n📱 الرقم: <code>{phone_number}</code>\n💰 السعر: <b>{price}$</b>\n\n📥 الكود وصلك بالأسفل وتم تثبيته فوق 📌"
                bot.edit_message_text(chat_id=user_id, message_id=status_msg_id, text=success_text, reply_markup=None, parse_mode="HTML")
                
                pin_msg_text = f"✅ تم استلام الكود! • الرقم: <code>{phone_number}</code> • الدولة: {flag} {c_name}\n🔑 كود تفعيل التليجرام: <code>{sms_code}</code>"
                sent_pin_msg = bot.send_message(user_id, pin_msg_text, parse_mode="HTML")
                try: bot.pin_chat_message(chat_id=user_id, message_id=sent_pin_msg.message_id, disable_notification=False)
                except: pass
                
                # 🔥 إرسال الإثبات التلقائي لقناة التفعيلات الخاصة بك علانية لزيادة الثقة
                try:
                    channel_log_msg = (f"🎰 <b>تم حجز وتفعيل رقم جديد بنجاح!</b>\n\n"
                                       f"🌍 <b>الدولة:</b> {flag} {c_name}\n"
                                       f"📱 <b>الرقم:</b> <code>{phone_number[:-4]}****</code>\n"
                                       f"🔑 <b>كود التفعيل:</b> <code>{sms_code}</code>\n\n"
                                       f"🎯 <b>عبر سستم بوت:</b> {CHANNEL_USER}")
                    bot.send_message(CHANNEL_USER, channel_log_msg, parse_mode="HTML")
                except: pass

                log_order(user_id, f"📱 {phone_number} | كود: {sms_code} | سعر: {price}$")
                SYSTEM_STATS["successful_orders"] += 1
                SYSTEM_STATS["total_sales"] += price
                
                try:
                    admin_log_msg = f"🔔 <b>بيع ناجح:</b>\n• الزبون: <code>{user_id}</code>\n• الرقم: <code>{phone_number}</code>\n• الكود: <code>{sms_code}</code>"
                    bot.send_message(ADMIN_ID, admin_log_msg, parse_mode="HTML")
                except: pass
                return
        except: pass
    
    release_bad_number(phone_number, acc_index)
    SYSTEM_STATS["failed_orders"] += 1
    
    fail_text = f"❌ <b>انتهى وقت الانتظار لعدم وصول الكود للرقم:</b>\n<code>{phone_number}</code>\n\n💰 لم يتم خصم أي مبلغ من رصيدك لعدم استلام كود التفعيل، محفظتك في أمان كامل!"
    try: bot.edit_message_text(chat_id=user_id, message_id=status_msg_id, text=fail_text, reply_markup=None, parse_mode="HTML")
    except: pass

def process_admin_target_id(message, action):
    try:
        target_id = int(message.text.strip())
        admin_state[message.from_user.id] = {"action": action, "target_user": target_id, "mode": "admin_amount"}
        msg = bot.send_message(message.chat.id, "💰 أدخل القيمة بالدولار الآن:")
        bot.register_next_step_handler(msg, process_admin_amount)
    except: bot.send_message(message.chat.id, "❌ الـ ID غير صحيح.")

def process_admin_amount(message):
    admin_id = message.from_user.id
    if admin_id in admin_state and admin_id == ADMIN_ID:
        try:
            amount = float(message.text.strip())
            target_id = admin_state[admin_id]["target_user"]
            action = admin_state[admin_id]["action"]
            if target_id not in USER_BALANCES: USER_BALANCES[target_id] = 0.00
            if action == "add":
                USER_BALANCES[target_id] += amount
                save_data("balances")
                bot.send_message(admin_id, f"✅ تم شحن {amount}$ لحساب {target_id}!")
                try: bot.send_message(target_id, f"💰 **تم شحن محفظتك بـ +{amount:.2f}$ من قبل الإدارة!**")
                except: pass
            else:
                USER_BALANCES[target_id] = max(0.00, USER_BALANCES[target_id] - amount)
                save_data("balances")
                bot.send_message(admin_id, f"✅ تم خصم {amount}$ من حساب {target_id}!")
            del admin_state[admin_id]
        except:
            bot.send_message(admin_id, "❌ خطأ في القيمة.")
            if admin_id in admin_state: del admin_state[admin_id]

def process_admin_broadcast(message):
    text = message.text
    count = 0
    for u_id in list(USER_BALANCES.keys()):
        if u_id == ADMIN_ID: continue
        try:
            bot.send_message(u_id, f"📢 **إعلان من الإدارة:**\n\n{text}")
            count += 1
        except: pass
    bot.send_message(ADMIN_ID, f"✅ تم الإرسال لـ {count} زبون بنجاح.")

def run_bot_polling():
    while True:
        try:
            bot.infinity_polling(timeout=80, long_polling_timeout=40)
        except Exception as e:
            print(f"⚠️ خطأ في البولينج: {e}")
            time.sleep(3)

def run_bot_safe():
    load_all_data()
    print("🕸️🕷️ إطلاق المنظومة السيبرانية وحماية الـ Polling والويب 24/7... 🚀✨📌")
    
    # 1. تشغيل محرك التليجرام (Polling) في خيط مستقل بالخلفية
    threading.Thread(target=run_bot_polling, daemon=True).start()
    
    # 2. تشغيل منظومة البنج الذاتي الفائقة (كل 3 دقائق) في خيط مستقل
    threading.Thread(target=keep_alive_ping, daemon=True).start()
    
    # 3. تشغيل محرك الصيد التلقائي بعد استقرار المتغيرات في خيط مستقل
    threading.Thread(target=global_auto_buyer, daemon=True).start()
    
    # 4. جعل خادم الويب الأساسي (Flask) هو العملية الرئيسية لمنع النوم نهائياً
    run_flask_server()

if __name__ == "__main__":
    run_bot_safe()
