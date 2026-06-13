from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os


class SeleniumEnv:
    def __init__(self, episode_id=0):
        self.episode_id = episode_id

        options = Options()
        # options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)

        # 🔥 Now dynamic (can be changed anytime)
        self.base_url = "https://opensource-demo.orangehrmlive.com/"

    # =============================
    # OPEN URL
    # =============================
    def open_url(self):
        print("Opening URL...")
        self.driver.get(self.base_url)

        self.wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        time.sleep(1)


    def get_page_html(self):
        return self.driver.page_source

    # =============================
    # 🔥 SMART ELEMENT FINDER (CORE)
    # =============================
    def find_element_smart(self, target):
        """
        Try multiple locator strategies automatically
        """

        # 1️⃣ XPath (if looks like xpath)
        if target.startswith("//"):
            return self.wait.until(
                EC.presence_of_element_located((By.XPATH, target))
            )

        # 2️⃣ CSS selector
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, target))
            )
        except:
            pass

        # 3️⃣ ID
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.ID, target))
            )
        except:
            pass

        # 4️⃣ NAME
        try:
            return self.wait.until(
                EC.presence_of_element_located((By.NAME, target))
            )
        except:
            pass

        # 5️⃣ Placeholder fallback
        try:
            return self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//input[contains(@placeholder,'{target}')]")
                )
            )
        except:
            pass

        raise Exception(f"Element not found using smart strategy: {target}")

    # =============================
    # TYPE
    # =============================
    def type(self, target, value):
        print(f"Typing into {target}: {value}")

        try:
            elem = self.find_element_smart(target)

            elem.clear()
            elem.send_keys(value)

            time.sleep(0.5)

        except Exception as e:
            raise Exception(f"Typing failed: {e}")

    # =============================
    # CLICK
    # =============================
    def click(self, target):
        print(f"Clicking {target}")

        try:
            elem = self.find_element_smart(target)

            self.wait.until(EC.element_to_be_clickable(elem))
            elem.click()

            time.sleep(2)

        except Exception as e:
            raise Exception(f"Click failed: {e}")

    # =============================
    # VERIFY
    # =============================
    def verify(self, target):
        print("Verifying result...")

        os.makedirs("outputs/screenshots", exist_ok=True)
        filename = f"outputs/screenshots/episode_{self.episode_id}_{int(time.time())}.png"

        try:
            # 🔥 URL-based verification (generic)
            current_url = self.driver.current_url
            print("🔍 CURRENT URL:", current_url)

            self.driver.save_screenshot(filename)

            if target in current_url:
                return 1, f"{target} detected in URL"
            else:
                return -1, f"{target} NOT found"

        except Exception as e:
            return -1, str(e)

    # =============================
    # CLOSE
    # =============================
    def close(self):
        print("Closing browser...")
        self.driver.quit()