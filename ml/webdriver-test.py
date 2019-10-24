from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
# you need chrome78 to use selenium
# curl https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
# echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
# apt update
# apt install google-chrome-stable

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path='/code/chromedriver' ,options=options)
driver.get('https://www.nankankeiba.com/program/00000000000000.do')
print(driver.title)
driver.save_screenshot('before.png')

btn = driver.find_element_by_xpath('//*[@id="race-cal"]/div/a')
btn.click()

# TODO try loop to escape error
# time.sleep(5)
# btn.click()

# past_btn_loc = driver.find_element_by_xpath('//*[@id="race-cal"]/div/a').location
# action = ActionChains(driver)
# action.move_by_offset(9, 365).click().perform()

driver.save_screenshot('after.png')
driver.quit()
print('end')