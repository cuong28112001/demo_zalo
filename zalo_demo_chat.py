from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import sys
import subprocess

try:
    # Khởi động Chrome với remote debugging
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    debug_port = "--remote-debugging-port=9222"
    user_data_dir = r'--user-data-dir=C:/Chrome_dev'
    subprocess.Popen([chrome_path, debug_port, user_data_dir])
    time.sleep(2)  # Thời gian chờ để Chrome khởi động

    # Thiết lập Chrome Options để kết nối tới phiên Chrome đang mở
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)
    print("Đang mở trang web...")
    driver.execute_script("window.open('https://chat.zalo.me/', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(10)  # Chờ thêm để trang tải đầy đủ

except Exception as e:
    print(f"Lỗi khi mở trang web: {e}")
    driver.quit()
    sys.exit()

anim_data_id = 5509432355200907380
css_anim_data_id = '.msg-item[anim-data-id="'+str(anim_data_id)+'"]'
print("Selector:", css_anim_data_id)

try:
    # Tìm các phần tử có anim-data-id bằng giá trị cho trước
    msg_items = driver.find_elements(By.CSS_SELECTOR, css_anim_data_id)
    
    if msg_items:
        # Sử dụng phần tử đầu tiên nếu có nhiều phần tử
        msg_item = msg_items[0]
        msg_item.click()
        print("Đã click vào phần tử msg_item với anim-data-id =", anim_data_id)
        
        # Chat: tìm phần tử input và gửi tin nhắn "abcd"
        try:
            chat_input = driver.find_elements(By.CSS_SELECTOR, '#chat-input-content-id #richInput')
            chat_input = chat_input[0]
            chat_input.click()
            chat_input.send_keys("abcd")
            chat_input.send_keys(Keys.ENTER)
            print("Đã điền nội dung 'abcd' và nhấn Enter.")
        except Exception as chat_e:
            print("Lỗi khi thao tác với phần tử chat:", chat_e)
    else:
        print("Không tìm thấy phần tử msg_item với selector:", css_anim_data_id)
except Exception as e:
    print("Không tìm thấy, lỗi:", e)