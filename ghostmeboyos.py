from selenium import webdriver
from selenium.webdriver.common.by import By

import time

print('DID NOT TEST THIS CODE. LMK IF WORKS.')
username = input('Enter username: ') 
password = input('Enter password: ')

browser = webdriver.Firefox()
site = 'https://www.bodybuilding.com/combined-signin?referrer=https%3A%2F%2Fforum.bodybuilding.com%2F%23&country=US'
browser.get(site)

time.sleep(3)

user_field = browser.find_element(By.NAME, 'username')
pass_field = browser.find_element(By.NAME, 'password')

user_field.send_keys(username)
pass_field.send_keys(password)

# Click off "want 15% off?" popup
i = 'N'
while i != 'Y':
    i = input('Did you remove 15% off popup? (Y/N)')

# browser.find_element(By.ID, "form button").click()
time.sleep(1)
browser.find_element(By.CLASS_NAME, 'combined-sign-in--button').click()

time.sleep(2)
# GOTO user CP
browser.get('https://forum.bodybuilding.com/usercp.php')

time.sleep(2)
browser.find_element(By.CLASS_NAME, 'smallfont').click() # first thread in control panel
time.sleep(2)
browser.find_element(By.CLASS_NAME, 'username').click() # open username menu
time.sleep(1)
browser.find_element(By.CLASS_NAME, 'right').click() # opens post history link
time.sleep(3)

# thread_list = browser.find_elements(By.CLASS_NAME, 'posttitle a')
# thread_names = browser.find_elements(By.CLASS_NAME, 'username_container h2 a')


thread_links_elem = browser.find_elements(By.CLASS_NAME, 'posttitle [href]') # enter thread

while True:        
    for count, x in enumerate(thread_links_elem, start=0):       
        # For each item in thread_list, GET 'HREF' attr
        thread_link = x.get_attribute('href')
        # Split post ID from URL
        x = thread_link.split('post')
        y = x[1]
        # concat to edit corresponding post ID
        z = 'vB::QuickEdit::' + y

        browser.execute_script(f'''window.open("{thread_link}", "_blank");''')

        window_name = browser.window_handles[-1]
        browser.switch_to.window(window_name=window_name)
        time.sleep(3)

        browser.find_element(By.NAME, z).click()  # edits post for del
        # time.sleep(1)
        browser.find_element(By.ID, 'vB_Editor_QE_1_delete').click() # deletes post
        browser.close()
        window_name = browser.window_handles[0]
        browser.switch_to.window(window_name=window_name)
    
    # GOTO next page if it exists
    # if browser.find_element(By.CLASS_NAME, 'prev_next [href]').exists():
    #     browser.find_element(By.CLASS_NAME, 'prev_next [href]').click()
    #     thread_links_elem = browser.find_elements(By.CLASS_NAME, 'posttitle [href]')

    browser.find_element(By.CLASS_NAME, 'prev_next [href]').click()   
    thread_links_elem = browser.find_elements(By.CLASS_NAME, 'posttitle [href]')
