# import internal modules
import os
import time

# import external modules
import pandas as pd
from dotenv import load_dotenv
from simple_salesforce import Salesforce


"""
Complete examples for adding new accounts to Salesforce
Covers single accounts, bulk imports, and error handling
"""


def connect_to_salesforce(consumer_key, consumer_secret, domain):
    """Connect to Salesforce"""
    try:
        sf = Salesforce(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            domain=domain
        )
        print("✓ Connected to Salesforce\n")
        return sf
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return None


def add_account(sf, account_data):
    """Add account only if it doesn't already exist
    """
    
    account_name, account_ccn = account_data['Name'], account_data['CCN__c']
    
    # Check if account exists

    query = f"SELECT Id FROM Account WHERE CCN_c = '{account_ccn}' LIMIT 1"
    
    try:
        result = sf.query(query)
        
        if result['totalSize'] > 0:
            existing = result['records'][0]
            print(f"  ⊗ Account '{account_name}' already exists (ID: {existing['Id']})")
            return {'success': False, 'message': 'Duplicate', 'id': existing['Id']}
        
        # Create new account
        new_account = sf.Account.create(account_data)
        print(f"  ✓ Created new account: {account_name} (ID: {new_account['id']})")
        return {'success': True, 'id': new_account['id'], 'created': True}
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return {'success': False, 'error': str(e)}


def add_accounts_from_dataframe(sf, df):
    """Import accounts from a pandas DataFrame with custom mapping
    """
    
    print(f"Importing {len(df)} records...\n")
    
    results = []
    
    for index, row in df.iterrows():
        try:
            # Build account data from mapping
            account_data = {}
            
            # Create account
            result = add_account(sf, account_data)
            results.append({
                'success': True,
                'id': result['id'],
                'name': account_data.get('Name', 'Unknown')
            })
            print(f"  [{index + 1}/{len(df)}] ✓ {account_data.get('Name', 'Unknown')}")
            
            time.sleep(0.1)
            
        except Exception as e:
            results.append({
                'success': False,
                'error': str(e),
                'name': row.get('Provider Name', 'Unknown')
            })
            print(f"  [{index + 1}/{len(df)}] ✗ Error: {str(e)}")
    
    success_count = sum(1 for r in results if r.get('success'))
    print(f"\n✓ Created {success_count}/{len(df)} accounts")
    
    return results


def main():
    """ Creates new accounts from dataset of all nursing homes in the following states: 
        Arizona, Nevada, Utah & Colorado. First checks if such account exists, if not creates it.

        New fields needed:
        Assigned Sales rep


    """

    # Configuration
    load_dotenv()
    CONSUMER_KEY = os.getenv['CONSUMER_KEY']
    CONSUMER_SECRET = os.getenv['CONSUMER_SECRET']
    DOMAIN = 'dwu00000ymz9b2af-dev-ed.develop.my'
    
    # Connect to Salesforce
    sf = connect_to_salesforce(CONSUMER_KEY, CONSUMER_SECRET, DOMAIN)

    #       Work with sql query endpoint. One state query works, many states query does not
    # query = '[SELECT * FROM 0ae91eb2-22da-5fe3-9dce-9811cdd6f1a8][WHERE State IN ("AZ", "NV", "UT", "CO")][LIMIT 2]'
    # query_one_state = '[SELECT * FROM 0ae91eb2-22da-5fe3-9dce-9811cdd6f1a8][WHERE State = "AZ"][LIMIT 10]'
    # request_url = f'https://data.cms.gov/provider-data/api/1/datastore/sql?query={query_one_state}'
    # response = requests.get(request_url, headers={'accept': 'application/json'})
    # data = response.json()

    df = pd.read_csv('https://data.cms.gov/provider-data/sites/default/files/resources/e923f267504f72a3b10c2daa39efed8a_1757685912/NH_ProviderInfo_Sep2025.csv')
    df = df[df['State'].isin(['AZ', 'NV', 'UT', 'CO'])]
    mapped_columns = {
        'Provider Name': 'Name',
        'Provider Address': 'BillingStreet',
        'City/Town': 'BillingCity',
        'State': 'BillingState',
        'ZIP Code': 'BillingPostalCode',
        'Telephone Number': 'Phone',
        'Provider Type': 'Type',
        'Ownership Type': 'Industry',
    }
    df_columns = df.columns
    for column in df_columns:
        if column == 'CMS Certification Number (CCN)':
            mapped_columns[column] = 'CCN__c'
        else:
            mapped_columns[column] = f'{column}__c'
        
    df.rename(columns=mapped_columns, inplace=True)
    add_accounts_from_dataframe(sf, df[:2])




if __name__ == "__main__":
    main()

