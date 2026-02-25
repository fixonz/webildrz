import os
import telebot
from telebot import types
from core import generate_and_save, update_site_links
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PUBLIC_URL = os.getenv("PUBLIC_URL", "https://your-app-name.railway.app")

if not TOKEN:
    print("WARNING: TELEGRAM_BOT_TOKEN not found. Bot disabled.")
    exit(0)

bot = telebot.TeleBot(TOKEN)

# In-memory storage for user sessions
user_sessions = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    user_sessions[chat_id] = {'step': 'name'}
    bot.send_message(chat_id, "Salut! 👋 Sunt asistentul tău personal **WEB? DONE!**.\n\nVrei un site profesionist generat instant de AI? Hai să începem!\n\n**Cum se numește afacerea ta?**", parse_mode='Markdown')

@bot.message_handler(commands=['cancel'])
def cancel_cmd(message):
    chat_id = message.chat.id
    user_sessions.pop(chat_id, None)
    bot.send_message(chat_id, "Am anulat procesul. Trimite /start când vrei să reîncepem. ✌️")

@bot.message_handler(commands=['edit'])
def edit_cmd(message):
    chat_id = message.chat.id
    # Check if we have a site_id in history or current session
    site_id = user_sessions.get(chat_id, {}).get('last_site_id')
    if not site_id:
        bot.send_message(chat_id, "Nu am găsit niciun site recent generat de tine. Generează unul nou cu /start sau trimite-mi codul site-ului.")
        return
    
    user_sessions[chat_id]['step'] = 'edit_info'
    bot.send_message(chat_id, f"Vrei să modifici link-urile pentru site-ul `{site_id}`? ✅\n\nTrimite-mi noile link-uri de Social Media sau info (sau /skip).", parse_mode='Markdown')

@bot.message_handler(func=lambda m: user_sessions.get(m.chat.id, {}).get('step') == 'name')
def get_biz_name(message):
    chat_id = message.chat.id
    user_sessions[chat_id]['name'] = message.text
    user_sessions[chat_id]['step'] = 'category'
    bot.send_message(chat_id, f"Super, **{message.text}**! ✅\n\nAcum spune-mi, care este **nișa sau categoria** afacerii? (ex: Restaurant Italian, Service Auto, Salon de Înfrumusețare, Cabinet Stomatologic, etc.)", parse_mode='Markdown')

@bot.message_handler(func=lambda m: user_sessions.get(m.chat.id, {}).get('step') == 'category')
def get_biz_category(message):
    chat_id = message.chat.id
    user_sessions[chat_id]['category'] = message.text
    user_sessions[chat_id]['step'] = 'media'
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    markup.add(types.KeyboardButton('/skip'))
    bot.send_message(chat_id, "Excelent! 🚀\n\nTrimite-mi acum un **logo sau o poză** reprezentativă (sau scrie /skip dacă vrei să folosim poze AI).", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(content_types=['photo', 'document'], func=lambda m: user_sessions.get(m.chat.id, {}).get('step') == 'media')
def get_biz_media(message):
    chat_id = message.chat.id
    user_sessions[chat_id]['step'] = 'social'
    bot.send_message(chat_id, "Am primit media! ✅ Va arăta super pe site.\n\nMai avem un ultim pas: ai link-uri de **Facebook, Instagram** sau alte info pe care vrei să le includem? Scrie-le aici sau trimite /skip.", reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')

@bot.message_handler(commands=['skip'])
def skip_step(message):
    chat_id = message.chat.id
    if chat_id not in user_sessions: return
    
    step = user_sessions[chat_id].get('step')
    if step == 'media':
        user_sessions[chat_id]['step'] = 'social'
        bot.send_message(chat_id, "Nicio problemă, folosim imagini premium AI! 🎨\n\nAI link-uri de social media (FB/Insta) sau info extra? Scrie-le aici sau /skip.", reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
    elif step == 'social':
        user_sessions[chat_id]['extra_info'] = ""
        start_generation(message)
    elif step == 'edit_info':
        bot.send_message(chat_id, "Nicio schimbare efectuată. Site-ul tău râmâne intact. ✌️")
        user_sessions[chat_id]['step'] = None

@bot.message_handler(func=lambda m: user_sessions.get(m.chat.id, {}).get('step') in ['social', 'edit_info'])
def handle_info_steps(message):
    chat_id = message.chat.id
    step = user_sessions[chat_id].get('step')
    
    if step == 'social':
        user_sessions[chat_id]['extra_info'] = message.text
        start_generation(message)
    elif step == 'edit_info':
        site_id = user_sessions[chat_id].get('last_site_id')
        bot.send_message(chat_id, "⚡ Actualizăm link-urile... Stai așa.")
        success, res = update_site_links(site_id, message.text)
        if success:
            url = f"{PUBLIC_URL}/demos/{res}"
            bot.send_message(chat_id, f"Actualizat! ✅ Noile info sunt acum live pe site.\n\n🔗 [Vezi Schimbările]({url})", parse_mode='Markdown')
        else:
            bot.send_message(chat_id, f"Eroare: {res}")
        user_sessions[chat_id]['step'] = None

def start_generation(message):
    chat_id = message.chat.id
    data = user_sessions.get(chat_id)
    if not data: return

    bot.send_message(chat_id, "BAM! ⚡ Pornim motoarele AI pentru tine.\n\nConstruim design-ul, scriem textele și optimizăm totul. Te anunț imediat ce e gata!")
    
    biz_data = {
        "name": data.get('name', 'Afacere'),
        "category": data.get('category', 'General'),
        "address": "Din Telegram Bot",
        "phone": "Contact rapid",
        "reviews": [], "rating": 5, "reviews_count": 0,
        "extra_info": data.get('extra_info', '')
    }
    
    try:
        site_id, filename = generate_and_save(biz_data)
        url = f"{PUBLIC_URL}/demos/{filename}"
        
        # Save site_id for future /edit calls
        user_sessions[chat_id]['last_site_id'] = site_id
        
        caption = f"Gata! 🎉 Site-ul tău e live.\n\n🔗 [Vizualizează Site-ul]({url})\n🔑 **Cod unic:** `{site_id}`\n\nDacă vrei să schimbi link-urile, scrie /edit. 🚀"
        bot.send_message(chat_id, caption, parse_mode='Markdown')
        user_sessions[chat_id]['step'] = None
    except Exception as e:
        print(f"BOT GEN ERROR: {e}")
        bot.send_message(chat_id, f"Oops! A apărut o eroare la generare: {e}\n\nÎncearcă din nou folosind /start.")

if __name__ == '__main__':
    print("ShapeShift Bot is running...", flush=True)
    bot.polling(none_stop=True)
