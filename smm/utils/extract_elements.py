def extract_elements_by_class(soup, class_name):
    try:
        # Find all elements with the specified class name
        elements = soup.find_all(class_=class_name)
        
        return elements
    except Exception as e:
        print(f"Error: {e}")
        return []