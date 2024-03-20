from smm.utils.load_to_bs4 import load_html_to_soup, load_json
from smm.utils.save_file import save_data_to_json
from smm.utils.extract_elements import extract_elements_by_class
from smm.constant import HOME_PAGE_URL, HOME_PAGE_BOOK_PTH

def home_page_process(print_datails=False):
    data = []
    num_pages = 5
    pages_urls = [HOME_PAGE_URL+"&page="+str(i+1) for i in range(num_pages)]
    for url in pages_urls:
        soup = load_html_to_soup(url)
        if soup:
            class_name = "ctext booksearchresult"
            elements = extract_elements_by_class(soup, class_name)
            if elements:
                print(f"Found {len(elements)} elements with class '{class_name}' for home page: {HOME_PAGE_URL}")
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
    save_data_to_json(data, HOME_PAGE_BOOK_PTH)
    print(f"Number of data entries in JSON file '{HOME_PAGE_BOOK_PTH}': ", len(data))

def book_page_process(book_info_json, print_datails=False):
    book_info_json = load_json(book_info_json)
    for book in book_info_json:
        soup = load_html_to_soup(book['url'])
        if soup:
            elements = extract_elements_by_class(soup, class_name)