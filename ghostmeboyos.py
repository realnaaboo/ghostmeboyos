from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

version = '0.2'

print(f'\nGHOST ME BOYOS {version}\n')

username = input('Enter username: ') 
password = input('Enter password: ')

browser = webdriver.Firefox()
site = 'https://www.bodybuilding.com/combined-signin?referrer=https%3A%2F%2Fforum.bodybuilding.com%2F%23&country=US'
browser.get(site)

try: 
    user_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    user_field.send_keys(username)
except: pass


try:
    pass_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
except: pass
pass_field.send_keys(password)


# Click off "want 15% off?" popup
i = 'N'
while i != 'Y':
    i = input('\nDid you remove 15% off popup? (Y/N) ')

try:
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'combined-sign-in--button'))).click()
except: pass

time.sleep(3)

dark_mode = 'https://forum.bodybuilding.com/?styleid=63'
browser.get(dark_mode)

try:
    id1 = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'welcomelink [HREF]')))
except: pass

id2 = id1.get_attribute('href')
id3 = id2.split('=')
userid = id3[1]

post_history = f'https://forum.bodybuilding.com/search.php?do=finduser&userid={userid}&contenttype=vBForum_Post&showposts=1'
browser.get(post_history)

try: # create list of thread links
    thread_links_elem = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'posttitle [href]'))) 
except: pass

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
        
        try: # edits post for del
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.NAME, z))).click()  
        except: pass

        try: # deletes post
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'vB_Editor_QE_1_delete'))).click() 
        except: pass
        
        try: # toggle 'delete message radio button'
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'dep_ctrl'))).click() 
        except: pass

        try: # confirm delete
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID, 'quickedit_dodelete'))).click() 
        except: pass
        
        # close thread
        browser.close() 
        posts_deleted += 1
        print(f'[{posts_deleted}] posts deleted')
        
        # focus first tab
        window_name = browser.window_handles[0] 
        browser.switch_to.window(window_name=window_name)
    
    # GOTO next page if it exists
    # if browser.find_element(By.CLASS_NAME, 'prev_next [href]').exists():
    #     browser.find_element(By.CLASS_NAME, 'prev_next [href]').click()
    #     thread_links_elem = browser.find_elements(By.CLASS_NAME, 'posttitle [href]')

    try:
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'prev_next [href]'))).click()
    except: pass

    try:
        thread_links_elem = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'posttitle [href]')))
    except: pass
