import functions
import json
import requests
import mysql.connector
import sys

def main():
    # Welcome message
    print(f"Hello! Program initializing..\n")

    # Load connection info
    try:
        f = open("connection.json", "r")
        connection_info = json.load(f)
        f.close()
        print(f"Database information successfully loaded..\n")

    except json.Error as err:
        print(f"Something went wrong loading the database connection {err}.\n")


    # Load API information
    try:
        f = open("/home/tyler/keys/us_gov_api.txt", "r")
        api_key = f.readline()
        f.close()
        print(f"API key loaded successfully..\n")

    except OSError as err:
        print(f"Error loading API key: {err}.\n")


    # Set up relevant control structure variables
    total = sys.maxsize
    limit = 5000
    offset = 0


    api_url = "https://api.eia.gov/v2/electricity/retail-sales/data?facets[sectorid][]=RES&data[]=sales"
    api_calls = 0


    # Control structure dictating how many API calls are needed.
    while (offset < total) and (api_calls < 10):
        parameters = {
            "frequency": "monthly",
            "start": "2001-01",
            "end": "2022-02",
            "offset": offset,
            "length": limit,
            "api_key": api_key
        }
        

        # Create database connection
        try:
            cnx = mysql.connector.connect(user=connection_info['user'],
                                        password=connection_info['password'],
                                        host=connection_info['host'],
                                        database=connection_info['database'])
            print(f"Database connection successful..\n")

        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}.\n")
        
        
        # Make API Call
        try:
            r = requests.get(api_url, params=parameters)
            r = r.json()
            
            # Print statement
            api_calls += 1
            print(f"API called: {api_calls} times.")

            # Saving information from API call
            data = r["response"]["data"]
            total = r["response"]["total"]
            


            # Loop structure for inputting data pieces from API call
            for entry in data:
                called_date = f'{entry["period"]}-01'
                called_state_code = entry["stateid"]
                called_sector_code = entry["sectorid"]
                called_sales = entry["sales"]
                called_units = entry["sales-units"]
                
                
                state_id = get_state_id(cnx, called_state_code)
                sector_id = get_sector_id(cnx, called_sector_code)
                unit_id = get_unit_id(cnx, called_units)
                
                
                # Insert into fact table
                insert_fact(cnx, state_id, sector_id, unit_id, called_date, called_sales)

                
            # Closing connections
            offset += limit
            cnx.close()
            print("Information parsing success!\n")
        
        except requests.exceptions.RequestException as rerr:
            print(f"Error with requests: {rerr}")
  

    # Confirmation message
    print(f"Program terminating..\n")