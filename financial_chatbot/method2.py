import pandas as pd

# Load the financial data into a DataFrame
try:
    data = pd.read_csv('financial_data.csv')
    print("Dataset loaded successfully")
    print("\nDataset Info:")
    print(data.info())
except FileNotFoundError:
    print("Error: financial_data.csv file not found!")
    data = pd.DataFrame()
except Exception as e:
    print(f"Error loading data: {str(e)}")
    data = pd.DataFrame()

def get_financial_info(company, year, metric):
    # Map common query terms to actual column names
    metric_mapping = {
        'net income': 'Net Income',
        'revenue': 'Total Revenue',
        'total assets': 'Total Assets',
        'total liabilities': 'Total Liabilities',
        'cash flow': 'Cash Flow from Operating Activities'
    }
    
    try:
        if data.empty:
            print("No data available - DataFrame is empty")
            return None
            
        actual_metric = metric_mapping.get(metric.lower())
        if not actual_metric:
            print(f"Error: Metric '{metric}' not found in mapping")
            return None
            
        print(f"Searching for - Company: {company}, Year: {year}, Metric: {actual_metric}")
        
        filtered_data = data[(data['Company'].str.lower() == company.lower()) &
                           (data['Fiscal Year'] == int(year))]
        
        if filtered_data.empty:
            print(f"No data found for {company} in {year}")
            return None
            
        result = filtered_data[actual_metric].values[0]
        return result
    except Exception as e:
        print(f"Error in get_financial_info: {str(e)}")
        return None

def financial_chatbot(query):
    if 'net income' in query.lower():
        try:
            # Improved parsing
            parts = query.lower().split('for')[1].strip().split('in')
            if len(parts) != 2:
                return "Please provide the query in the format: 'net income for [Company] in [Year]'."
            
            company = parts[0].strip()
            year = parts[1].strip()
            
            # Validate year is a number
            try:
                year = int(year)
            except ValueError:
                return "Please provide a valid year."
                
            result = get_financial_info(company, str(year), 'net income')
            if result:
                response = f"The net income for {company.title()} in {year} was ${result:,.2f}"
            else:
                response = "I'm sorry, I couldn't find that information."
        except IndexError:
            response = "Please provide the query in the format: 'net income for [Company] in [Year]'."
    elif 'revenue' in query.lower():
        try:
            company = query.split('for')[1].split('in')[0].strip()
            year = query.split('in')[1].strip()
            result = get_financial_info(company, year, 'revenue')
            if result:
                response = f"The revenue for {company.title()} in {year} was ${result:,.2f}"
            else:
                response = "I'm sorry, I couldn't find that information."
        except IndexError:
            response = "Please provide the query in the format: 'revenue for [Company] in [Year]'."
    else:
        response = "I can help you find information about net income or revenue. Please ask about these metrics."
    return response

# Example interactions
print(financial_chatbot("net income for Tesla in 2021"))
print(financial_chatbot("revenue for Apple in 2020"))
