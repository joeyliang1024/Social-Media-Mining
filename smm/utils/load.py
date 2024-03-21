import json
import requests
from bs4 import BeautifulSoup

def load_html_to_soup(url):
    try:
        # Send GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content into BeautifulSoup object
            soup = BeautifulSoup(response.content, 'html.parser')
            #print("HTML content loaded and parsed successfully.")
            return soup
        else:
            print(f"Error: Failed to load HTML content (Status Code: {response.status_code})")
            return None
    except requests.RequestException as e:
        # Handle any request exceptions
        print(f"Error: {e}")
        return None

def load_json_to_soup(json_file_path):
    try:
        # Open the JSON file and load the data
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Convert the JSON data back to BeautifulSoup object
        soup = BeautifulSoup(json_data, 'html.parser')
        
        return soup
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error: JSON decode error - {e}")
    except Exception as e:
        print(f"Error: {e}")

def load_txt_to_soup(text_file_path):
    try:
        # Open the text file and read its content
        with open(text_file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        # Create a BeautifulSoup object from the text content
        soup = BeautifulSoup(text_content, 'html.parser')
        
        return soup
    except FileNotFoundError:
        print(f"Error: File '{text_file_path}' not found.")
    except Exception as e:
        print(f"Error: {e}")

def load_json(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: JSON decode error - {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None