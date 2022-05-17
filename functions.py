import json
import requests
import mysql.connector
import sys
import re
from datetime import date, datetime


# Get state id given state abbreviation (ie 'CA' for 'California')
def get_state_id(cnx, state_abbrev):
    cursor = cnx.cursor()
    
    query = f'''
        SELECT state_id
        FROM d_state
        WHERE state_code = "{state_abbrev}"
    '''
    
    # Run query
    try:
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result
    except mysql.connector.Error as err:
        print(f"An error occured while fetching state_id for: {state_abbrev}.")
        print(err)
    except TypeError:
        print(f"TypeError for input field: {state_abbrev}.")
        
    # Close connection
    cursor.close()

# Get sector id given sector code (ie 'RES' for 'Residential')
def get_sector_id(cnx, sector_code):
    cursor = cnx.cursor()
    
    query = f'''
        SELECT sector_id
        FROM d_sector
        WHERE sector_code = "{sector_code}"
    '''
    
    # Run query
    try:
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result
    except mysql.connector.Error as err:
        print(f"An error occured while fetching sector_id for: {sector_code}.")
        print(err)
    except TypeError:
        print(f"TypeError for input field: {sector_code}.")
        
    
    # Close connection
    cursor.close()


# Get unit id given unit name
def get_unit_id(cnx, full_unit):
    unit = re.sub('\s', '_', full_unit)
    
    cursor =  cnx.cursor()
    
    query = f'''
        SELECT unit_id
        FROM d_unit
        WHERE unit_desc = "{unit}"
    '''
    
    # Run query
    try:
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result
    except mysql.connector.Error as err:
        print(f"An error occured while fetching unit_id for: {full_unit}.")
        print(err)
    except TypeError:
        print(f"TypeError for input field: {full_unit}.")
              
    # Close connection
    cursor.close()


# Insert function to fact table
def insert_fact(cnx, state_id, sector_id, unit_id, date, sales):
    cursor = cnx.cursor()
    
    last_updated = str(datetime.now())
    
    # duplicate key update is not working properly.. 
    query = f'''
        INSERT INTO f_elec_sales (state_id, sector_id, unit_id, date, sales, last_updated)
        VALUES ({state_id}, {sector_id}, {unit_id}, \'{date}\', {sales}, \'{last_updated}\')
        ON DUPLICATE KEY UPDATE
            last_updated = \'{last_updated}\'
    '''
    
    # Run query
    try:
        cursor.execute(query)
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"Something went wrong inserting value set: {state_id, sector_id, unit_id, date, sales}.")
        print(err)
    except TypeError:
        print(f"TypeError for value set: {state_id, sector_id, unit_id, date, sales}.")