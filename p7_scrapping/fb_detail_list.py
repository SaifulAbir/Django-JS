import time
from selenium import webdriver

driver = webdriver.Chrome('driver/chromedriver')  # Optional argument, if not specified will search path.
driver.get('https://m.facebook.com/groups/119479435370179/?ref=br_rs&_rdc=1&_rdr')

driver.maximize_window()
# print('start action')
# First more button
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.find_element_by_link_text('More').click()
time.sleep(5)
# Second more button
driver.find_element_by_link_text('More').click()

SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

post_time = driver.find_element_by_css_selector('._52jc._5qc4._78cz._24u0._36xo').text
print('post Date: ', post_time)

post_detils = driver.find_element_by_css_selector('._5rgt._5nk5').text
print('Post Details: ', post_detils)
url = driver.current_url
print('Current post url: ', url)

driver.back()
time.sleep(3)

driver.quit()








# driver.find_element_by_id('m_login_email').send_keys('maisuraco@outlook.com')
# driver.find_element_by_id('m_login_password').send_keys('ish123@#')
# time.sleep(3) # Let the user actually see something!
# driver.find_element_by_name('login').click()
# time.sleep(2)
# driver.find_element_by_class_name('_54k8 _56bs _26vk _56b_ _56bw _56bu').click()
# time.sleep(2)
# driver.find_element_by_tag_name('body').click()
# time.sleep(5)
# search_box = driver.find_element_by_name('q')
# time.sleep(2)
# search_box.send_keys('Ishraak solutions')
# time.sleep(2)
# search_box.submit()
# time.sleep(2)
# driver.find_element_by_link_text('Ishraak Solutions').click()