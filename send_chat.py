import json
from zlapi import ZaloAPI
from zlapi.models import *

# Đọc cấu hình từ file zalo_config.json
try:
    with open("zalo_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    imei = config["imei"]
    cookies = config["cookies"]
except Exception as e:
    print("Không thể đọc file cấu hình zalo_config.json:", e)
    exit(1)

# Khởi tạo bot
bot = ZaloAPI("0559959149", "Cuong@1416", imei=imei, cookies=cookies)

thread_id = "5509432355200907380"
thread_type = ThreadType.USER
msg = Message(text="Hello, đây là tin nhắn test!")


response=bot.sendMessage(msg,thread_id,  thread_type)

print("Response từ server:", response)