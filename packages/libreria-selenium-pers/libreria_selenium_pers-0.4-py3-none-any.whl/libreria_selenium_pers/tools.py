import time
import logging
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def functionOpenPage(driver, page):
    driver.get(page)
    time.sleep(2)

def selectClickButton(driver, xpath):
    WebDriverWait(driver, 15).until(
       EC.presence_of_element_located((By.XPATH, xpath))
    ).click()
    time.sleep(1)
    logger.info(f"Boton clickeado {xpath}")

def introduceText(driver, id, text):
    elem = driver.find_element(By.ID, id)
    elem.send_keys(text)
    logger.info("Texto enviado")

#This function receives a message and send it by Telegram with the given variables.
#Param: message, the message that is going to be send.
def sendMessage(message):
    send_text = 'https://api.telegram.org/bot' + API_KEY + '/sendMessage?chat_id=' + MESSAGE_ID + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_text)
    return response



