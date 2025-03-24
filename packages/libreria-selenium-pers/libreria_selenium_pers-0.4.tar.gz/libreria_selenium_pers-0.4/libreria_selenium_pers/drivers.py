from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from .config import config_chrome_options

def initialize_chrome_driver():
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=config_chrome_options()
    )

def initialize_mozilla_driver():
    return webdriver.Firefox

def initialize_edge_driver():
    return webdriver.Edge
