from smm.utils.load_to_bs4 import load_html_to_soup, load_json
from smm.utils.save_file import save_data_to_json
from smm.utils.extract_elements import extract_elements_by_class
from smm.utils.constant import HOME_PAGE_URL, HOME_PAGE_BOOK_PTH
from tqdm import tqdm

def home_page_process(print_datails=False):
    data = []
    num_pages = 5
    pages_urls = [HOME_PAGE_URL+"&page="+str(i+1) for i in range(num_pages)]
    with tqdm(total=len(pages_urls), desc="Crawing total book") as pbar:
        for url in pages_urls:
            soup = load_html_to_soup(url)
            if soup:
                class_name = "ctext booksearchresult"
                elements = extract_elements_by_class(soup, class_name)
                if elements:
                    pbar.set_postfix_str(f"Found {len(elements)} elements for home page: {HOME_PAGE_URL}")
                    for element in elements:
                        # Extract text and URL
                        text = element.text.strip()
                        url = element.a['href']
                        data.append({"book": text, "url": url})
                        if print_datails:
                            print(f"Book: {text}, URL: {url}")    
                else:
                    print(f"No elements found with class '{class_name}'.")
            else:
                print("Failed to load HTML data.")
            pbar.update(1)
    save_data_to_json(data, HOME_PAGE_BOOK_PTH)
    print(f"Number of data entries in JSON file '{HOME_PAGE_BOOK_PTH}': ", len(data))

def book_page_process(book_info_json, print_details=False):
    book_info_json = load_json(book_info_json)
    with tqdm(total=len(book_info_json), desc="Crawing book pages") as pbar:
        for book in book_info_json:
            pages_dict = {}
            soup = load_html_to_soup(book['url'])
            if soup:
                elements = extract_elements_by_class(soup, "ctext")
                if elements:
                    result = elements[0].find_all("a")
                    for _ in result:
                        pages_dict[_.text.strip()] = "https://ctext.org/" + _['href']
                else:
                    elements = extract_elements_by_class(soup, "restable")
                    for element in elements:
                        pages_object = element.find_all("a", style='white-space: nowrap;')
                        for page in pages_object:
                            str_number = 4
                            while True:
                                soup1 = load_html_to_soup("https://ctext.org/" + page.get("href")[:-1] + str(str_number))
                                element = soup1.find('a', string='文字版')
                                if element:
                                    pages_dict[page.text.strip()] = "https://ctext.org/" + element.get("href")
                                    break
                                else:
                                    str_number += 1
                                    if str_number > 10:  # or any maximum number you want to set
                                        break  # Break the loop if the maximum number is exceeded
                            if page.text.strip() not in pages_dict:
                                pbar.set_postfix_str("No page urls found.")
            #print(f"Number of data entries in book '{book['book']}': {len(pages_dict)}")
            book["pages"] = pages_dict
            pbar.update(1)
            pbar.set_postfix_str(f"Number of data entries in book '{book['book']}': {len(pages_dict)}")
    
    # Save processed data
    save_data_to_json(book_info_json, "origin_craw_data/book_page_url.json")