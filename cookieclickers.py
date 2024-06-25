from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://orteil.dashnet.org/cookieclicker/")

cookie_id = "bigCookie"
cookies_id = "cookies"
productPrefix = "product"
productPricePrefix = "productPrice"

WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]")))

language = driver.find_element(By.XPATH, "//*[contains(text(), 'English')]")
language.click()

WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, cookie_id))) 

cookie = driver.find_element(By.ID, cookie_id)

# Função para fechar o aviso de cookies, se existir
def close_cookie_warning():
    try:
        dismiss_button = driver.find_element(By.CLASS_NAME, "cc_btn_accept_all")
        dismiss_button.click()
    except Exception as e:
        print("Aviso de cookies não encontrado ou já fechado")

while True:
    cookie.click()
    cookies_count = driver.find_element(By.ID, cookies_id).text.split(" ")[0]
    cookies_count = int(cookies_count.replace(",", ""))
    
    for i in range(4):
        product_price = driver.find_element(By.ID, productPricePrefix + str(i)).text.replace(",","")
        
        if not product_price.isdigit():
            continue

        product_price = int(product_price)

        if cookies_count >= product_price:
            product = driver.find_element(By.ID, productPrefix + str(i)) 

            close_cookie_warning()

            try:
                wait = WebDriverWait(driver, 10)
                product = wait.until(ec.element_to_be_clickable((By.ID, productPrefix + str(i))))
                product.click()
            except Exception as e:
                print(f"Nao foi possivel clicar no produto {i}: {e}")
            break