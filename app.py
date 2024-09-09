from flask import Flask, render_template, request
from utils import get_data, clean_data_parallel
import requests
import itertools

# Initialize Flask app
app = Flask(__name__)

# Function to extract product names from a URL
def extract_product_names(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = get_data(response)
            data = clean_data_parallel(data)
            print(data)

            response = requests.post('http://localhost:5001/process', json={"text": data})
            if response.json()["error"]:
                print(response.json()["error"])
                return ["Nothing was found"]
            data = list(itertools.chain(*[sublist for sublist in response.json()["predictions"] if sublist[0]]))
            print(data)
            data = [item for sublist in data for item in sublist if len(item.split()) > 1 and "sale" not in item.lower()]

            return data
        else:
            return [f'Response status code: {response.status_code}']
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return [f"An error occurred: {e}"]

@app.route('/', methods=['GET', 'POST'])
def index():
    products = []
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            products = extract_product_names(url)
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
