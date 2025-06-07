from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import re  
import sys
import subprocess
from selenium.webdriver.chrome.options import Options

def get_imei_and_cookies():
    imei = None
    cookies = None
    driver = None
    chrome_process = None  # Lưu handle của tiến trình Chrome
    try:
        # Khởi động Chrome với remote debugging và lưu tiến trình vào biến chrome_process
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        debug_port = "--remote-debugging-port=9222"
        user_data_dir = r'--user-data-dir=C:/Chrome_dev'
        chrome_process = subprocess.Popen([chrome_path, debug_port, user_data_dir])
        time.sleep(2)  # Chờ cho Chrome khởi động

        # Thiết lập Chrome Options để kết nối tới phiên Chrome đang mở
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        # Kết nối tới Chrome đang mở
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        print("Đang mở trang web...")
        driver.execute_script("window.open('https://chat.zalo.me/', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(10)  # Chờ thêm để trang tải đầy đủ

        # Lấy log từ performance để kiểm tra các network call
        logs = driver.get_log("performance")
        for entry in logs:
            log_message = json.loads(entry["message"])["message"]
            # Tìm URL request chứa chuỗi "getServerInfo?imei="
            url = log_message.get("params", {}).get("request", {}).get("url", "")
            if "getServerInfo?imei=" in url:
                # Sử dụng biểu thức chính quy để trích xuất giá trị imei
                match = re.search(r'getServerInfo\?imei=([^&]*)', url)
                if match:
                    imei = match.group(1)
                    print("Giá trị imei là:", imei)
                    # Lấy cookies của trang web dưới dạng danh sách các dict
                    cookies_list = driver.get_cookies()
                    # Chuyển đổi cookies thành dict: key là tên cookie, value là giá trị cookie
                    cookies = {cookie["name"]: cookie["value"] for cookie in cookies_list}
                    break
                else:
                    print("Không tìm thấy giá trị imei trong URL:", url)
        return imei, cookies, chrome_process
    except Exception as e:
        print(f"Lỗi: {e}")
        return imei, cookies, chrome_process
    finally:
        # Đảm bảo rằng phiên WebDriver được đóng lại
        if driver is not None:
            driver.quit()

if __name__ == '__main__':
    imei, cookies, chrome_process = get_imei_and_cookies()
    if imei is None or cookies is None:
        print("Không lấy được giá trị imei hoặc cookies. Thoát chương trình.")
        # Nếu chrome_process đã được khởi tạo, hãy đảm bảo đóng nó
        if chrome_process is not None:
            chrome_process.terminate()
        sys.exit(1)
    # Lưu thông tin vào file cấu hình JSON
    config = {"imei": imei, "cookies": cookies}
    with open("zalo_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    print("Thông tin imei và cookies đã được lưu vào file zalo_config.json")
    
    # Sau khi hoàn thành, đóng tiến trình Chrome nếu nó vẫn đang chạy
    if chrome_process is not None:
        chrome_process.terminate()
        print("Đóng tiến trình Chrome.")