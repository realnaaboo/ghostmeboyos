from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
# from dontclickonstream import getUserPass
import time 
import os   # to clear screen
import sys  # to exit program 

version = '0.7'

def displayLogo():
    print(f'''
    
 ██████  ██   ██  ██████  ███████ ████████    ███    ███ ███████    ██████   ██████  ██    ██  ██████  ███████ 
██       ██   ██ ██    ██ ██         ██       ████  ████ ██         ██   ██ ██    ██  ██  ██  ██    ██ ██      
██   ███ ███████ ██    ██ ███████    ██       ██ ████ ██ █████      ██████  ██    ██   ████   ██    ██ ███████ 
██    ██ ██   ██ ██    ██      ██    ██       ██  ██  ██ ██         ██   ██ ██    ██    ██    ██    ██      ██ 
 ██████  ██   ██  ██████  ███████    ██    ██ ██      ██ ███████ ██ ██████   ██████     ██     ██████  ███████ {version}
                                                                                                               
                                                                                                               
''')
################# LOGIN #################\


def user_pass():
    # username, password = getUserPass()
    username = password = False
    # Enter user/pass
    while not (username and password):
        os.system('cls')
        displayLogo()
        username = input('Enter username: ') 
        password = input('Enter password: ')
        print('')
    return username, password
        
def chooseBrowser():
    choice = False
    while not (choice == 1 or choice == 2 or choice == 3):
        os.system('cls')
        displayLogo()

        try: choice = int(input('\n1) Firefox\n2) Chrome\n3) Safari\n\nChoose browser: Chrome not working...\n-> '))        
        except ValueError: pass
    print('\nloading...')
    match choice:
        case 1:
            return webdriver.Firefox()
        case 2:
            return webdriver.Chrome()
        case 3: 
            return webdriver.Safari()

def load_signin(browser):
    # site = 'https://www.bodybuilding.com/combined-signin?referrer=https%3A%2F%2Fforum.bodybuilding.com%2F%23&country=US'
    site = 'https://forum.bodybuilding.com/?styleid=63'
    browser.get(site) 


def user_pass_field(browser, username, password):
    # Search for username field, input username
    try: 
        user_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'navbar_username')))
        user_field.send_keys(username)
    except ElementNotVisibleException: print('Username field not found...')

    # Search for password field, input password
    try:
        pass_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'navbar_password_hint')))
        pass_field.send_keys(password)
    except ElementNotVisibleException: print('Password field not found...')
            
def check_popup():
    # Click off "want 15% off?" popup
    ugh = 'N'
    while ugh != 'Y':
        ugh = input('\nDid you remove 15% off popup? (Y/N) ')
        
def sign_in(browser):
    # Click 'sign-in' button
    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'loginbutton'))).click()
    except ElementClickInterceptedException: print('Sign-in not reached...')

def login_loop():
    browser = False
    id = False
    while not id:
        username, password = user_pass()
        if not browser:
            browser = chooseBrowser()
        load_signin(browser)
        user_pass_field(browser, username, password)
        check_popup()
        sign_in(browser)
        time.sleep(3)   # Wait page load
        # load_darkmode(browser)
        id = get_userid(browser)
    return browser, id


# try:
#     fifteenoff = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ab-programmatic-close-button')))
# except: pass
# didclose = input('did it close?')

################# USERID #################

def load_darkmode(browser):
    # Load BB.com dark theme
    dark_mode = 'https://forum.bodybuilding.com/?styleid=63'
    browser.get(dark_mode)

def get_userid(browser):
    # Checks for user id (determines login success)
    try:
        id1 = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'welcomelink [HREF]')))
        print('Login successful...')
    except (NameError, NoSuchElementException, ElementNotVisibleException, TimeoutException): 
        print('Login unsuccessful...')
        time.sleep(3)
        return False

    try:
        # Split id from link
        id2 = id1.get_attribute('href')
        id3 = id2.split('=')
        return id3[1]
    except NameError: 
        print('uid not returned...')
        time.sleep(1.5)

################# POST HISTORY #################

def load_posthistory(browser, user_id):
    post_history = f'https://forum.bodybuilding.com/search.php?do=finduser&userid={user_id}&contenttype=vBForum_Post&showposts=1'
    browser.get(post_history)

def get_search_id(browser):    
    # get temp search id
    search_id_a = browser.current_url
    search_id_b = search_id_a.split('=')
    return search_id_b[1]

def get_post_history_page(search_id):
    # option to not delete recent posts
    post_history_page_num = input('\n(Default is 1)\nEnter page # to start deleting from: ')
    return f'https://forum.bodybuilding.com/search.php?searchid={search_id}&pp=&page={post_history_page_num}', post_history_page_num

def load_post_history_page_check(browser, post_history_page, post_history_page_num):
    if int(post_history_page_num) > 1:
        browser.get(post_history_page)

def get_thread_links(browser):
    try: # return list of thread links
        return WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'posttitle [href]'))) 
    except TimeoutException: 
        print('\nUnable to load post history...')
        input('\nPress enter to close program:\n')
        sys.exit()
    except NoSuchElementException:
        print('\nPost history not found...\n')
        input('\nPress enter to close program:\n')
        sys.exit()

################# PAGES + THREAD #################


################# MULT TABS #################
def create_post_id_pairs(browser):
    # Empty list for post pairs
    link_post_id = []
    # Get thread links
    thread_links_list = get_thread_links(browser)
    # Iterate through list
    for link in thread_links_list:
        post_link = link.get_attribute('href')
        
        # Split post ID from URL
        x = post_link.split('post')
        post_id = x[1]
        
        # concat to edit corresponding post ID
        vB_post_id = 'vB::QuickEdit::' + post_id

        post_dict = {f'link': post_link, 'postid': vB_post_id}
        
        link_post_id.append(post_dict)
    return link_post_id

def mult_tabs(browser):
    while True:
        link_post_id_pairs = create_post_id_pairs(browser)
        pagecycle = 0
        while pagecycle < len(link_post_id_pairs):
            # choice = input('(Range 1-5)\nEnter # of tabs to open: ')
            new_list = []
            choice = 5
            for count, pair in enumerate(link_post_id_pairs, start=1):

                if count < len(link_post_id_pairs):
                    isLast = False
                else: isLast = True

                new_pair = {'link': pair['link'], 'postid': pair['postid']}
                new_list.append(new_pair) # new_pair.items?
                
                browser.execute_script(f'''window.open("{pair['link']}", "_blank");''')
                pagecycle += 1
                time.sleep(1)
                
                if ((count > 0) and (count % choice == 0)):
                    
                    time.sleep(3)
                    # Get window name of last tab
                    thread_loop(browser, new_list, count)
                    new_list = []

                elif (count % choice-1 or choice-2 or choice-3 or choice-4 == 0) and (isLast == True): #4
                    
                    time.sleep(3)
                    # Get window name of last tab
                    thread_loop(browser, new_list, count)
                    new_list = []

                # elif (count % choice-2 == 0) and (isLast == True): #3

                #     time.sleep(3)
                #     # Get window name of last tab
                #     thread_loop(browser, new_list, count)
                #     new_list = []

                # elif (count % choice-3 == 0) and (isLast == True): #2

                #     time.sleep(3)
                #     # Get window name of last tab
                #     thread_loop(browser, new_list, count)                              
                #     new_list = []

                # elif (count % choice-4 == 0) and (isLast == True): #1

                #     time.sleep(3)
                #     # Get window name of last tab
                #     thread_loop(browser, new_list, count)
                #     new_list = []

            break  
            # if pagecycle > len(link_postid_pairs):
            #     break
        check_next_page(browser)

def check_next_page(browser):
        global post_history_page_num
        try: # next page   
            next_page_list = WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'prev_next [href]')))
            next_page = next_page_list[1]
            next_page.click()
            # update page num
            post_history_page_num = str(int(post_history_page_num) + 1)
        except (ElementNotVisibleException, NoSuchElementException): 
            print('Next page not found...')
            input('Press enter to close program.\n')
            sys.exit()


def thread_loop(browser, new_list, count):
    global post_history_page_num
    print(f'\nPAGE: [{post_history_page_num}]')
    inner_thread_loop(browser, new_list, count)

def inner_thread_loop(browser, new_list, count):
    for count, x in enumerate(new_list, start=0):
        
        window_name = browser.window_handles[-1] # focus last tab
        browser.switch_to.window(window_name=window_name)

        # check if locked thread
        thread_status = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, 'newcontent_textcontrol')))
        if thread_status.text == 'Closed Thread' and count == 4:
            print('Thread locked.')
            browser.close()
            window_name = browser.window_handles[0] 
            browser.switch_to.window(window_name=window_name)
            break
        elif thread_status.text == 'Closed Thread':
            print('Thread locked.')
            browser.close()
            # focus first tab
            window_name = browser.window_handles[0] 
            browser.switch_to.window(window_name=window_name)
            continue

        try: # edits post for del. targ -> "vB::QuickEdit::" + post ID
            WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.NAME, x['postid']))).click()
        except ElementClickInterceptedException: 
            print('Unable to click edit button...')

        try: # deletes post
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'vB_Editor_QE_1_delete'))).click() 
        except ElementClickInterceptedException: 
            print('Unable to click delete button...')
        except TimeoutException:
            print('Unable to delete post... [skipping]')
            # close thread
            browser.close() 
            # focus first tab
            window_name = browser.window_handles[0] 
            browser.switch_to.window(window_name=window_name)
            if (x == new_list[-1]): break
            else: continue
        
        try: # toggle 'delete message radio button'
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'dep_ctrl'))).click() 
        except ElementClickInterceptedException: 
            print('Unable to click toggle delete button...')

        try: # confirm delete
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'quickedit_dodelete'))).click()
        except ElementClickInterceptedException: 
            print('Unable to click confirm delete button...')

        global posts_deleted 
        posts_deleted += 1
        print(f'[{posts_deleted}] posts deleted')
        
        # close thread
        browser.close() 
        
        # focus first tab
        window_name = browser.window_handles[0] 
        browser.switch_to.window(window_name=window_name)

################# START #################

def main():
    '''
        main function: this runs the program
        for MISC users, read each line to understand how it works.  
    '''
    global post_history_page_num
    global posts_deleted 
    posts_deleted = 0   #stats
    browser, user_id = login_loop()
    load_posthistory(browser, user_id)
    search_id = get_search_id(browser)
    post_history_page, post_history_page_num = get_post_history_page(search_id)
    load_post_history_page_check(browser, post_history_page, post_history_page_num)
    # thread_loop(browser, post_history_page_num)
    mult_tabs(browser)

main()
