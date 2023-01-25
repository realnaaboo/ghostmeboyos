from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os # to clear screen

version = '0.3'

def displayLogo():
    print(f'''
    
 ██████  ██   ██  ██████  ███████ ████████    ███    ███ ███████    ██████   ██████  ██    ██  ██████  ███████ 
██       ██   ██ ██    ██ ██         ██       ████  ████ ██         ██   ██ ██    ██  ██  ██  ██    ██ ██      
██   ███ ███████ ██    ██ ███████    ██       ██ ████ ██ █████      ██████  ██    ██   ████   ██    ██ ███████ 
██    ██ ██   ██ ██    ██      ██    ██       ██  ██  ██ ██         ██   ██ ██    ██    ██    ██    ██      ██ 
 ██████  ██   ██  ██████  ███████    ██    ██ ██      ██ ███████ ██ ██████   ██████     ██     ██████  ███████ {version}
                                                                                                               
                                                                                                               
''')

def checkVisibility(elem):
    return WebDriverWait(browser, 10).until(EC.visibility_of(elem))
def checkClickability(elem):
    return WebDriverWait(browser, 10).until(EC.element_to_be_clickable(elem))
# def checkPresenceOfElemID(elem):
#     return WebDriverWait(browser, 30).until(EC.presence_of_element_located(By.ID, elem))
# def checkPresenceOfElemCLASS(elem):
#     return WebDriverWait(browser, 30).until(EC.presence_of_element_located(By.CLASS_NAME, elem))
# def checkPresenceOfElemNAME(elem):
#     WebDriverWait(browser, 30).until(EC.presence_of_element_located(By.NAME, elem)) 

################# START #################



################# LOGIN #################

username = password = False
while not (username and password):
    os.system('cls')
    displayLogo()
    username = input('Enter username: ') 
    password = input('Enter password: ')
    print('')

browser = webdriver.Firefox.s()
site = 'https://www.bodybuilding.com/combined-signin?referrer=https%3A%2F%2Fforum.bodybuilding.com%2F%23&country=US'
browser.get(site)

try: 
    user_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    if checkVisibility(user_field):
        user_field.send_keys(username)
except: pass

try:
    pass_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    if checkVisibility(pass_field):
        pass_field.send_keys(password)
except: pass


# Click off "want 15% off?" popup
i = 'N'
while i != 'Y':
    i = input('\nDid you remove 15% off popup? (Y/N) ')


# try:
#     fifteenoff = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'ab-programmatic-close-button')))
#     if checkVisibility(fifteenoff):
#         if checkClickability(fifteenoff):
#             fifteenoff.click()
# except: pass

# didclose = input('did id close?')

try:
    login = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'combined-sign-in--button')))
except: pass

time.sleep(3)

################# USERID #################

dark_mode = 'https://forum.bodybuilding.com/?styleid=63'
browser.get(dark_mode)

try:
    id1 = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'welcomelink [HREF]')))
    print('Login successful...')
except: print('Not logged in...')

id2 = id1.get_attribute('href')
id3 = id2.split('=')
userid = id3[1]

################# POST HISTORY #################

post_history = f'https://forum.bodybuilding.com/search.php?do=finduser&userid={userid}&contenttype=vBForum_Post&showposts=1'
browser.get(post_history)

try: # create list of thread links
    thread_links_elem = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'posttitle [href]'))) 
except NameError: 
    print('\nPost history not found... (closing...)')

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
        
        try: # edits post for del. targ -> "vB::QuickEdit::" + post ID
            edit_post = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.NAME, z)))
        except: pass

        try: # deletes post
            delete_post = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, 'vB_Editor_QE_1_delete'))) 
        except: pass
        
        try: # toggle 'delete message radio button'
            dlt_radio_toggle = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dep_ctrl'))) 
        except: pass

        try: # confirm delete
            confirm_delete = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.ID, 'quickedit_dodelete')))
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
        next_page = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'prev_next [href]')))
    except: pass

    try:
        thread_links_elem = WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'posttitle [href]')))
    except NameError: 
        print('Post history not found... (press enter to close')
        break
