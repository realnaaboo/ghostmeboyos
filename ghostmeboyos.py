from selenium import webdriver
from selenium.webdriver.common.by import By

import time

print('\nGHOST ME BOYOS 0.1\n')
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
    i = input('\nDid you remove 15% off popup? (Y/N) ')

# browser.find_element(By.ID, "form button").click()
time.sleep(1)

browser.find_element(By.CLASS_NAME, 'combined-sign-in--button').click()

time.sleep(5)

dark_mode = 'https://forum.bodybuilding.com/?styleid=63'
browser.get(dark_mode)
id1 = browser.find_element(By.CLASS_NAME, 'welcomelink [HREF]')
idz = id1.get_attribute('href')
id2 = idz.split('=')
userid = id2[1]
post_history = f'https://forum.bodybuilding.com/search.php?do=finduser&userid={userid}&contenttype=vBForum_Post&showposts=1'
browser.get(post_history)

time.sleep(3)

thread_links_elem = browser.find_elements(By.CLASS_NAME, 'posttitle [href]') # enter thread

posts_deleted = 0
page = 0

while True:        
    page += 1
    print(f'PAGE: [{page}]')
    for count, x in enumerate(thread_links_elem, start=0):       
        # For each item in thread_list, GET 'HREF' attr
        thread_link = x.get_attribute('href')
        # Split post ID from URL
        x = thread_link.split('post')
        y = x[1]
        # concat to edit corresponding post ID
        z = 'vB::QuickEdit::' + y

        browser.execute_script(f'''window.open("{thread_link}", "_blank");''')

        window_name = browser.window_handles[-1] # focus last tab
        browser.switch_to.window(window_name=window_name)
        time.sleep(3)
        browser.find_element(By.NAME, z).click()  # edits post for del
        time.sleep(0.5)
        browser.find_element(By.ID, 'vB_Editor_QE_1_delete').click() # deletes post
        time.sleep(0.5)
        browser.find_element(By.CLASS_NAME, 'dep_ctrl').click() # toggle 'delete message'
        browser.find_element(By.ID, 'quickedit_dodelete').click() # confirm delete
        time.sleep(3)
        browser.close() # close thread
        posts_deleted += 1
        print(f'[{posts_deleted}] posts deleted')
        

        window_name = browser.window_handles[0] # focus first tab
        browser.switch_to.window(window_name=window_name)
    
    # GOTO next page if it exists
    # if browser.find_element(By.CLASS_NAME, 'prev_next [href]').exists():
    #     browser.find_element(By.CLASS_NAME, 'prev_next [href]').click()
    #     thread_links_elem = browser.find_elements(By.CLASS_NAME, 'posttitle [href]')

    browser.find_element(By.CLASS_NAME, 'prev_next [href]').click()   
    thread_links_elem = browser.find_elements(By.CLASS_NAME, 'posttitle [href]')
