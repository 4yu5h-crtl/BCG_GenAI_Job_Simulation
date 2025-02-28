from flask import Flask, request, jsonify, json
import pandas as pd

app = Flask(__name__)

# Load financial data
data = pd.read_csv('financial_data.csv')

# After loading the data
print("Loaded CSV data:")
print(data.head())
print("\nColumns:", data.columns.tolist())
print("\nDataset Info:")
print(data.info())
print("\nUnique Companies:", data['Company'].unique())
print("\nUnique Years:", data['Fiscal Year'].unique())

# Define a function to handle queries
def get_financial_info(company, year, metric):
    try:
        result = data[(data['Company'].str.lower() == company.lower()) &
                      (data['Fiscal Year'] == int(year))][metric].values[0]
        return result
    except IndexError:
        return None

# Define route for chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    # Check if 'query' is in the JSON data
    if 'query' not in request.json:
        return jsonify({'error': 'Missing query parameter'}), 400
        
    user_query = request.json.get('query', '').lower()
    
    # Check if query is empty
    if not user_query:
        return jsonify({'error': 'Query cannot be empty'}), 400
        
    if 'total revenue' in user_query:
        try:
            company = user_query.split('for')[1].split('in')[0].strip()
            year = user_query.split('in')[1].strip()
            result = get_financial_info(company, year, 'Total Revenue')
            if result:
                response = f"The total revenue for {company.title()} in {year} was {result}."
            else:
                response = "I'm sorry, I couldn't find that information."
        except IndexError:
            response = "Invalid query format. Please use format: 'total revenue for COMPANY in YEAR'"
    elif 'net income' in user_query:
        company = user_query.split("'s")[0].strip()
        years = [int(s) for s in user_query.split() if s.isdigit()]
        if len(years) == 2:
            result1 = get_financial_info(company, years[0], 'Net Income')
            result2 = get_financial_info(company, years[1], 'Net Income')
            if result1 and result2:
                change = result2 - result1
                response = (f"{company.title()}'s net income changed by {change} "
                            f"from {years[0]} to {years[1]}.")
            else:
                response = "I'm sorry, I couldn't find that information."
        else:
            response = "Please provide two years to compare."
    else:
        response = "I'm sorry, I can only provide information on predefined queries."
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)