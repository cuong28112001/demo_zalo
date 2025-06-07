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

class CustomBot(ZaloAPI):
    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        print("mid:", mid)
        print("author_id:", author_id)
        print("message_object:", message_object)
        print("message:", message)
        print("Thread ID:", thread_id)
        print("Thread Type:", thread_type)

        if author_id == thread_id:
            msg = Message(text="Tìm thấy: " + str(message))
            response = self.sendMessage(msg, thread_id, thread_type)
            print("Response từ server:", response)

# Khởi tạo bot
bot = CustomBot("0559959149", "Cuong@1416", imei=imei, cookies=cookies)

bot.listen(thread=True)