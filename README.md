# Installation

1. Clone the repository using git clone command
2. After cloning create virtual environment using `python -m venv env`
3. Activate the virtual environment
4. Install the dependencies using `pip install -r requirements.txt`
5. Run the project using `python main.py`

# Testing

1. To run tests just run `python -m unittest tests.test`

# Endpoints

1. /frequency: Analyzes the word frequency of a Wikipedia article.
2. /history: Retrieves the search history.
   - # Usage
     - Open postman and do GET request to
       `http://127.0.0.1:5000/frequency?topic=Python&n=5`
       `http://127.0.0.1:5000/history`
