import requests
import json
def save_home_page_html(home_page_url, output_path):
    try:
        # Send GET request to the URL
        response = requests.get(home_page_url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Save the content of the response to the specified output path
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Successfully crawled the URL and saved the content to {output_path}")
        else:
            print(f"Error: Failed to crawl the URL (Status Code: {response.status_code})")
    except requests.RequestException as e:
        # Handle any request exceptions
        print(f"Error: {e}")

def save_data_to_json(data, json_file_path):
    try:
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Data saved to {json_file_path}")
    except Exception as e:
        print(f"Error: {e}")