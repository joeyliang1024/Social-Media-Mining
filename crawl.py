from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re
import pandas as pd
import sys
from pprint import pprint as pp
from selenium.webdriver import ChromeOptions
opts = ChromeOptions()
opts.add_argument("--headless")
driver = webdriver.Chrome(options=opts)
driver.get('http://google.com')

# get crawl home page
googlr_search_input_area = driver.find_element(By.XPATH, '//*[@class="gLFyf"]')
googlr_search_input_area.send_keys("明實錄 中央研究院歷史語言研究所")
googlr_search_input_area.send_keys(Keys.RETURN)
for webp in driver.find_elements(By.XPATH, '//*[@jsname="UWckNb"]'):
    try:
        herf_value = webp.get_attribute("href")
        if re.match(r"https://hanchi.+", herf_value):
            print(herf_value)
            driver.get(herf_value)
    except StaleElementReferenceException:
        # Retry the operation after a short delay
        #time.sleep(1)
        continue

def load_books_tree_graph():
    msl_btn = driver.find_element(By.XPATH, '//*[@id="frmTitle"]/table/tbody/tr[4]/td/div/table/tbody/tr[3]/td[4]/a[2]')
    msl_btn.click()
    
    next_chapter_btn = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td[3]/table/tbody/tr[1]/td[2]/a[1]')
    next_chapter_btn.click()

load_books_tree_graph()

books_list_cur = driver.find_element(By.CLASS_NAME, 'treehit')
books_list = driver.find_elements(By.CLASS_NAME, 'tree')
require_book_list = [ book.text for book in books_list if book.text != '史' and book.text != '編年' and book.text != '明實錄' and book.text != '校勘記' ]
all_books_list = list()
all_books_list.append(books_list_cur.text)
all_books_list += require_book_list

print(all_books_list)
# ['校印本明實錄總目', '版本說明', '校印明實錄序', '校勘記凡例', '太祖', '太宗', '仁宗', '宣宗', '英宗', '憲宗', '孝宗', '武宗', '世宗', '穆宗', '神宗', '光宗', '熹宗', '附錄']

def title_cleaning(origin_title):
    clean_title = re.sub(u'\u3000', ' ', origin_title).strip()
    clean_title = re.sub(r'\(.+?\)|\d+日', '', clean_title).strip()
    title_list = [item for item in clean_title.split('／')[2:] if item != '']
    title = ' '.join(title_list)

    return title

def dict_size_mb(d):
    return sys.getsizeof(d) / (1024 * 1024)

def to_dataframe(dict_data):
    df = pd.DataFrame()

    for key, value in dict_data.items():
        new_df = pd.DataFrame({'field': [value['field']] * len(value['text']), 'title': key, 'text': value['text']})
        df = pd.concat([df, new_df], ignore_index=True)
    
    return df

def reload_to_current_dir(search_text):
    main_page_btn = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/a")
    main_page_btn.click()
    database_btn = driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td/a")
    database_btn.click()
    load_books_tree_graph()

    driver.find_element(By.XPATH, '//*[@id="frmTitle"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/input[2]').clear()
    driver.find_element(By.XPATH, '//*[@id="frmTitle"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/input[2]').send_keys(search_text)
    search_btn = driver.find_element(By.XPATH, '//*[@id="frmTitle"]/table/tbody/tr[2]/td/table/tbody/tr[6]/td/input[1]')
    search_btn.click()
    to_book_btn = driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td[3]/div/table[2]/tbody/tr[2]/td[4]/a')
    to_book_btn.click()
    to_pre_target_page = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[2]/td[3]/table[2]/tbody/tr[1]/td[2]/a")
    to_pre_target_page.click()
    to_target_page_btn = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[2]/td[3]/table/tbody/tr[1]/td[2]/a[2]")
    to_target_page_btn.click()

wait = WebDriverWait(driver, 10)

msl_corpus = dict()
field_num = 0
book_counter = 0
size_limit = 1
file_counter = 1

while 1:
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        if book_counter > 17:
            print(f"book_counter: {book_counter}")
            break
        
        book_title = driver.find_element(By.CLASS_NAME, 'gobookmark')
        title = title_cleaning(book_title.text)

        if all_books_list[book_counter] in title:
            if title not in msl_corpus:
                field_num += 1
                msl_corpus[title] = {
                    "field": field_num,
                    "text": []
                }
        
            div_text = soup.select_one('div.div2').text.strip()
            div_texts = soup.select('div.div2 div')
            for div in div_texts:
                msl_corpus[title]["text"].append(div.text.strip())

            next_page_btn = driver.find_element(By.XPATH, '//img[@title="下一章"]')
            next_page_btn.click()
        else:
            book_counter += 1
        
        if dict_size_mb(msl_corpus) >= size_limit:
            print(f"size: {dict_size_mb(msl_corpus)}")
            df = to_dataframe(msl_corpus)
            df.to_csv(f'./origin_craw_data/msl_corpus_part{file_counter}.csv', index=False)
            print(f'Data part {file_counter} written to CSV.')

            msl_corpus.clear()
            file_counter += 1

    except NoSuchElementException as e:
        reload_to_current_dir(msl_corpus[title]['text'][-1][:15])
        print("No such element exception.")

    except TimeoutException:
        driver.refresh()

if msl_corpus:
    df = to_dataframe(msl_corpus)
    df.to_csv(f'./origin_craw_data/msl_corpus_part{file_counter}.csv', index=False)
    print(f'Final part {file_counter} written to CSV.')
