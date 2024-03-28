import re
import time
import json
import random
from tqdm.auto import tqdm
from tqdm.notebook import tqdm_notebook
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

class BasicLawProcessor:
    def __init__(self, init_url):
        self.opts = ChromeOptions()
        self.opts.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.opts)  # You may need to adjust this based on your setup
        self.init_url = init_url
        self.object_url_dict = {}
        self.data = {}

    def click_next_page(self):
        next_page_btns = self.driver.find_elements(By.XPATH, '//*[@id="hlPage"]')
        for btn in next_page_btns:
            try:
                next_page_btns = self.driver.find_elements(By.XPATH, '//*[@id="hlPage"]')
                for btn in next_page_btns:
                    if btn.text == "下一頁":
                        if btn.get_attribute('class') == "aspNetDisabled":
                            #print("No next page")
                            return False
                        else:
                            # Click successful, exit function
                            btn.click()
                            return True  
            except StaleElementReferenceException:
                # Handle StaleElementReferenceException by retrying
                pass  
        return False

    def get_element_content(self):
        result_dict = {}
        判決_table = self.driver.find_element(By.XPATH, '//*[@id="plRightList"]')
        判決_urls = 判決_table.find_elements(By.XPATH, '//*[@id="hlkNo"]') 
        判決_contents = self.driver.find_elements(By.XPATH, '//*[@class="col-td text-pre"]') 
        if len(判決_urls) == len(判決_contents):
            for url, context in zip(判決_urls, 判決_contents):
                result_dict[str(url.text)] = {
                    "url": url.get_attribute("href"),
                    "content": context.text
                }
        return result_dict
    
    def get_all_craw_types(self):
        種類_table = self.driver.find_element(By.XPATH, '//*[@id="plLeftCount"]')
        司法種類 = 種類_table.find_elements(By.TAG_NAME, "a")
        self.object_url_dict = {re.sub(r'\d+', '', 種類.text):{
            "first_page_url":種類.get_attribute('href'),
            "number_of_data":re.findall(r'\d+', 種類.text)[0]
                                                             }
                                 for 種類 in 司法種類[:-1]}

    def crawing(self):
        self.driver.get(self.init_url)
        self.get_all_craw_types()
        for type_name, type_info in self.object_url_dict.items():
            print(f"Now processing {type_name}:")
            print(f"Number of data: {type_info['number_of_data']}")
            progress_bar = tqdm(total=int(type_info['number_of_data']), initial=0)
            self.driver.get(type_info['first_page_url'])
            # init_data_dict
            self.data[type_name] = {}
            try:
                # first page
                result_dict = self.get_element_content()
                progress_bar.update(len(result_dict))
                self.data[type_name].update(result_dict)
            except:
                pass
            while self.click_next_page():
                # other pages
                try:
                    result_dict = self.get_element_content()
                    progress_bar.update(len(result_dict))
                    self.data[type_name].update(result_dict)
                except:
                    pass
                time.sleep(random.uniform(0, 5))
            progress_bar.close()

class SingleLawTypeProcessor:
    def __init__(self, type_name, first_page_url):
        self.opts = ChromeOptions()
        self.opts.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.opts)
        self.type_name = type_name
        self.first_page_url = first_page_url
        self.data = {}

    def click_next_page(self):
        next_page_btns = self.driver.find_elements(By.XPATH, '//*[@id="hlPage"]')
        for btn in next_page_btns:
            try:
                next_page_btns = self.driver.find_elements(By.XPATH, '//*[@id="hlPage"]')
                for btn in next_page_btns:
                    if btn.text == "下一頁":
                        if btn.get_attribute('class') == "aspNetDisabled":
                            #print("No next page")
                            return False
                        else:
                            # Click successful, exit function
                            btn.click()
                            return True  
            except StaleElementReferenceException:
                # Handle StaleElementReferenceException by retrying
                pass  
        return False
    
    def get_element_content(self):
        result_dict = {}
        判決_table = self.driver.find_element(By.XPATH, '//*[@id="plRightList"]')
        判決_urls = 判決_table.find_elements(By.XPATH, '//*[@id="hlkNo"]') 
        判決_contents = self.driver.find_elements(By.XPATH, '//*[@class="col-td text-pre"]') 
        if len(判決_urls) == len(判決_contents):
            for url, context in zip(判決_urls, 判決_contents):
                result_dict[str(url.text)] = {
                    "url": url.get_attribute("href"),
                    "content": context.text
                }
        return result_dict
    
    def crawling(self, progress_bar=None):
        self.driver.get(self.first_page_url)
        self.data[self.type_name] = {}
        try:
            result_dict = self.get_element_content()
            self.data[self.type_name].update(result_dict)
            if progress_bar:
                progress_bar.update(len(result_dict))
        except:
            pass
        while self.click_next_page():
            try:
                result_dict = self.get_element_content()
                self.data[self.type_name].update(result_dict)
                if progress_bar:
                    progress_bar.update(len(result_dict))
            except:
                pass
            time.sleep(random.uniform(0, 5))
        self.driver.close()

class MutiThreadLawProcessor:
    def __init__(self, init_url, save_path):
        self.opts = ChromeOptions()
        self.opts.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.opts)  # You may need to adjust this based on your setup
        self.init_url = init_url
        self.save_path = save_path
        self.object_url_dict = {}
        self.data = {}

    def get_all_craw_types(self):
        種類_table = self.driver.find_element(By.XPATH, '//*[@id="plLeftCount"]')
        司法種類 = 種類_table.find_elements(By.TAG_NAME, "a")
        self.object_url_dict = {re.sub(r'\d+', '', 種類.text):{
            "first_page_url":種類.get_attribute('href'),
            "number_of_data":re.findall(r'\d+', 種類.text)[0]
                                                             }
                                 for 種類 in 司法種類[:-1]}


    def crawl_single_type(self, type_name, type_info):
        #pbar = tqdm_notebook(total=int(type_info['number_of_data']), desc=type_name)
        pbar = tqdm(total=int(type_info['number_of_data']), desc=type_name)
        processor = SingleLawTypeProcessor(type_name, type_info['first_page_url'])
        processor.crawling(progress_bar=pbar)
        self.data.update(processor.data)

    def muti_thread_crawling(self):
        self.driver.get(self.init_url)
        self.get_all_craw_types()
        with ThreadPoolExecutor() as executor:
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
        with open(self.save_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False)


    

