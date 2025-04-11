from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome

def before_all(context):
    context.driver = webdriver.Chrome()

def after_all(context):
    context.driver.quit()

def before_scenario(context, scenario):
    context.wait_time = 2

