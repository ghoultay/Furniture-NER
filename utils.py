from bs4 import BeautifulSoup
from collections import OrderedDict
from furniture_terms import furniture_terms_non_plural as furniture_terms
from concurrent.futures import ProcessPoolExecutor
import re

def get_data(response, verbose=True):
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove unnecessary tags: scripts, styles, iframes, and <sup> tags
    for script in soup(["script", "style", "iframe", "sup"]):
        script.decompose()
    
    # Extract text specifically from block elements (use more specific tags to avoid duplicates)
    block_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'alt', 'a'])
    
    # Create an empty set to collect unique text (avoiding duplicates)
    seen_text = set()
    
    # Collect text, ensuring that duplicates are avoided
    extracted_text = []
    for element in block_elements:
        text = element.get_text(separator=' ', strip=True)
        if text not in seen_text:
            seen_text.add(text)
            extracted_text.append(text)
    
    # Join the extracted text into one long string separated by ' ~ '
    combined_text = ' ~ '.join(extracted_text)
    
    # Clean text: replace special characters, extra spaces, and clean up
    cleaned_text = re.sub(r'\s+', ' ', combined_text)  # Replace multiple spaces/newlines with a single space
    cleaned_text = cleaned_text.replace("&", "and")
    cleaned_text = re.sub(r'[^A-Za-z0-9\s~]', '', cleaned_text)  # Remove non-alphanumeric characters except ~
    cleaned_text = re.sub(r'^\s*|\s\s*', ' ', cleaned_text)  # Remove extra whitespaces
    cleaned_text = cleaned_text.strip()  # Remove leading/trailing whitespaces
    
    # Split the cleaned text by the separator '~'
    data = cleaned_text.split(" ~ ")
    
    # Remove any empty strings or extra spaces from the resulting list
    return [item.strip() for item in data if item.strip()]

# Function to detect valid plural forms (avoid words like 'mattress')
def is_plural_word(word):
    # Check if word ends with 's' and singular form exists in the furniture terms list
    return word.lower().endswith('s') and word[:-1].lower() in furniture_terms

# Function to check if the entire text contains any plural form
def contains_plural(text):
    words = text.split()
    return any(is_plural_word(word) for word in words)

# Function to filter out irrelevant content and check for complete product names
def is_relevant(text):
    # Exclude text that contains any plural forms
    if contains_plural(text):
        return False
    # Include only if singular furniture terms match and there are at least 2 words
    return re.search(r'\b(' + '|'.join(map(re.escape, furniture_terms)) + r')\b', text, re.IGNORECASE) and len(text.split()) >= 2

# Function to remove duplicates and irrelevant content
def clean_data(data):
    # Remove duplicates while preserving order
    unique_data = list(OrderedDict.fromkeys(data))
    # Remove empty strings and irrelevant content
    filtered_data = [text for text in unique_data if is_relevant(text)]
    return filtered_data

# Parallel version (optional for large datasets)
def clean_data_parallel(data):
    # Remove duplicates first
    unique_data = list(OrderedDict.fromkeys(data))
    
    # Apply parallel processing for relevance check
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(is_relevant, unique_data))
    
    # Return filtered data
    return [text for text, keep in zip(unique_data, results) if keep]