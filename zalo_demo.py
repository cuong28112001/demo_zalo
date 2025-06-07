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
    # Mở Chrome với remote debugging
    subprocess.Popen([chrome_path, debug_port, user_data_dir])
    time.sleep(2)  # Thời gian chờ để Chrome khởi động

    # Thiết lập Chrome Options để kết nối tới phiên Chrome đang mở
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # Kết nối tới Chrome đang mở
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    print("Đang mở trang web...")
    driver.execute_script("window.open('https://chat.zalo.me/', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(10)  # Chờ thêm để trang tải đầy đủ

except Exception as e:
    print(f"Lỗi khi mở trang web: {e}")
    driver.quit()
    sys.exit()


fn_data_id = 7587661490206614605
css__fn_anim_data_id = '.msg-item[anim-data-id="'+str(fn_data_id)+'"]'
fn_items = driver.find_elements(By.CSS_SELECTOR, css__fn_anim_data_id)
fn_items = fn_items[0]

while True:
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, ".msg-item div.z-noti-badge")
        
        if elements:
            msg_item = elements[0].find_element(By.XPATH, "./ancestor::div[contains(@class, 'msg-item')]")
            msg_item.click()
            print("Đã click")
            anim_data_id = msg_item.get_attribute("anim-data-id")
            print("author-id là:", anim_data_id)
            truncate_element = msg_item.find_element(By.CSS_SELECTOR, "div.truncate")
            truncate_value = truncate_element.text.strip()
            print("name là:", truncate_value)

            # Sau khi click
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".message-action span.text"))
                )
                message_spans = driver.find_elements(By.CSS_SELECTOR, ".message-action span.text")
                for index, span in enumerate(message_spans, start=1):
                    # print(span)

                    text_content = span.text.strip()
                    print(f"Nội dung tin nhắn thứ {index}: {text_content}")
                chat_input = driver.find_elements(By.CSS_SELECTOR, '#chat-input-content-id #richInput')
                chat_input = chat_input[0]
                chat_input.click()
                chat_input.send_keys("Tìm thấy: " + str(text_content) )
                chat_input.send_keys(Keys.ENTER)
                

            
            except Exception as e:
                print(".message-action span.text: ", e)
        else:
            print("msg-item div.z-noti-badge")
        #trỏ về mặc định
                
        fn_items.click()
    except Exception as ex:
        print("Lỗi 1", ex)
    
    time.sleep(0.5)

sys.exit()