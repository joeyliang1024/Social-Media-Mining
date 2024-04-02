import re
import time
import json
import os
import random
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class SingleBookProcessor:
    def __init__(self, type_name, first_page_url, save_path):
        self.opts = ChromeOptions()
        self.opts.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.opts)
        self.type_name = type_name
        self.save_path = save_path
        self.first_page_url = first_page_url # book's fist page url will be save here
        self.total_section_num = 0           # total sections number of this book
        self.sections = {}                   # ex: {"附錄1":{"section_first_page":"https://123456789"},"附錄2":{"section_first_page":"https://111222333"}}
        self.data = {}                       # not defined yet

    def title_cleaning(self, origin_title, return_list=True):
        clean_title = re.sub(u'\u3000', ' ', origin_title).strip()
        clean_title = re.sub(r'\(.+?\)|\d+日', '', clean_title).strip()
        title_list = [item for item in clean_title.split('／')[2:] if item != '']
        return title_list if return_list else ' '.join(title_list)

    def get_all_sections(self):
        self.driver.get(self.first_page_url)
        self.total_section_num = len(self.driver.find_element(By.XPATH, '//*[@class="div3"]/table').find_elements(By.TAG_NAME, 'tr'))-3
        self.sections = {column.find_element(By.TAG_NAME, 'font').text:{"section_first_page":column.find_element(By.TAG_NAME, 'font').find_element(By.XPATH, '..').get_attribute('href')}
                         for column in self.driver.find_element(By.XPATH, '//*[@class="div3"]/table').find_elements(By.TAG_NAME, 'tr')[3:] 
                         if column.find_element(By.TAG_NAME, 'font')}
        
    def click_next_page(self):
        '''
        return True if have next page, else return False
        '''
        # driver should start from the page: sections["section name"]["section_first_page"]
        # if the page title not in sections.key name, then this section is finished, return False
        # else return True 
        try:
            next_page_btn = self.driver.find_element(By.XPATH, '//*[@title="下一章"]').find_element(By.XPATH, '..')
            # 檢查是否同一個書目
            # 是：點選下一頁
            self.driver.get(next_page_btn.get_attribute('href'))
            book_name = self.title_cleaning(self.driver.find_element(By.XPATH, '//*[@class="gobookmark"]').text)[1]
            # 睡一下，怕爬太快被封
            time.sleep(random.uniform(0, 5))
            if book_name == self.type_name:
                return True
            # 否：換下一本
            else:
                return False
        except NoSuchElementException:
            # 沒有下一位
            return False
    
    def get_element_content(self):
        # title: <a> class="gobookmark"
        # contexts: <div> style="text-indent:0em;padding-left:0em;"
        try:
            title = self.title_cleaning(self.driver.find_element(By.XPATH, '//*[@class="gobookmark"]').text, return_list=False)
            contexts = [_.text for _ in self.driver.find_elements(By.XPATH, '//*[@style="text-indent:0em;padding-left:0em;"]')]
            return {"Title":title,
                    "Context":contexts} 
        except:
            return {"Title":"",
                    "Context":[]} 
        
    def save_book_result(self):
        save_dir = os.path.join(self.save_path, self.type_name)
        os.makedirs(save_dir, exist_ok=True) 
        with open(os.path.join(save_dir, "result.json"), 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False)

    def crawling(self, progress_bar=None):
        '''
        start crawing the book data, updata tqdm bar if finish a section.
        #TODO is finished
        '''
        self.data[self.type_name] = []
        for section in self.sections.values():
            count = 0
            self.driver.get(section['section_first_page'])
            # Now is first page.
            try:
                result_dict = self.get_element_content()
                self.data[self.type_name].append(result_dict)
                if progress_bar:
                    count+=1
                    progress_bar.set_postfix_str(f"Craw pages: {count}")
            except:
                pass
            # Now is other pages.
            while self.click_next_page():
                try:
                    result_dict = self.get_element_content()
                    self.data[self.type_name].append(result_dict)
                    if progress_bar:
                        count+=1
                        progress_bar.set_postfix_str(f"Craw pages: {count}")
                except:
                    pass  
            if progress_bar:
                progress_bar.update(1)
        progress_bar.close()
        self.driver.close()
        self.save_book_result()

class MutiThreadProcessor:
    def __init__(self, save_path):
        self.opts = ChromeOptions()
        self.opts.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.opts)
        self.init_url = None
        self.save_path = save_path
        self.object_url_dict = {} # {"太祖":{"first_section_url":url1}, "太宗":{"first_section_url":url2}}
        self.data = {}
    
    def get_home_page(self):
        self.driver.get('http://google.com')
        googlr_search_input_area = self.driver.find_element(By.XPATH, '//*[@class="gLFyf"]')
        googlr_search_input_area.send_keys("明實錄 中央研究院歷史語言研究所")
        googlr_search_input_area.send_keys(Keys.RETURN)
        google_results = []
        while len(google_results) == 0:
            google_results = self.driver.find_elements(By.XPATH, '//*[contains(text(), "合作建置計畫")]')
            if len(google_results) != 0:
                # found webp
                self.driver.get(google_results[0].find_element(By.XPATH, '..').get_attribute('href'))
            else:
                # not found, refresh.
                self.driver.refresh()
        self.init_url = self.driver.current_url
        
    def load_books_tree_graph(self):
        try:
            msl_btn = self.driver.find_element(By.XPATH, '//*[@id="frmTitle"]/table/tbody/tr[4]/td/div/table/tbody/tr[3]/td[4]/a[2]')
            msl_btn.click()
            next_chapter_btn = self.driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td[3]/table/tbody/tr[1]/td[2]/a[1]')
            next_chapter_btn.click()
        except:
            print("This page has no object tee graph you need.")

    def get_all_craw_types(self):
        not_need_books = ["版本說明", "校印本明實錄總目", "校勘記凡例"]
        book_names = [i.text for i in self.driver.find_elements(By.XPATH, '//*[@title="P.1"]') if i.text not in not_need_books]
        urls = []
        for element in self.driver.find_elements(By.XPATH, '//*[@class="ltd2"]'):
            try:
                urls.append(element.find_element(By.TAG_NAME, 'a').get_attribute("href"))
            except:
                pass
        self.object_url_dict = {book:{"first_page_url":url} for book, url in zip(book_names, urls)}

    def crawl_single_type(self, type_name, type_info):
        processor = SingleBookProcessor(type_name, type_info['first_page_url'], self.save_path)
        processor.get_all_sections()
        pbar = tqdm(total=int(processor.total_section_num), desc=type_name)
        processor.crawling(progress_bar=pbar)
        self.data.update(processor.data)
        
    def muti_thread_crawling(self):
        self.get_home_page()
        print(f"Home page url this time: {self.init_url}")
        print(f"Now driver url location is at {self.init_url}")
        self.load_books_tree_graph()
        print("Book tree graph loaded.")
        print("Now getting all books tpyes:")
        self.get_all_craw_types()
        for key, value in self.object_url_dict.items():
            print(f"Book: {'　' * (6 - len(key))}{key}, Url: {value['first_page_url']}")
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Create a list of arguments for crawl_single_type
            type_names, type_infos = [], []
            for type_name, type_info in self.object_url_dict.items():
                type_names.append(type_name) 
                type_infos.append(type_info)
            try:
                # Use executor.map to apply crawl_single_type to each set of arguments
                executor.map(self.crawl_single_type, type_names, type_infos)
            except Exception as e:
                print(f"An error occurred: {e}")

        self.driver.quit()
    
    def save_data(self):
        os.makedirs(self.save_path, exist_ok=True) 
        with open(os.path.join(self.save_path, "result.json"), 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False)

    

