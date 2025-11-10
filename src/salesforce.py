# import internal libraries
import os

# import external libraries
import pandas as pd
from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceMalformedRequest
from dotenv import load_dotenv


""" Module documentation
"""


def connect_to_salesforce():
    """ Established a connection to salesforce and returns the salesforce object.
    """
    try:
        load_dotenv()

        # Connect to salesforce with username, password, consumer key and secret
        # username = os.getenv('USERNAME')
        # password = os.getenv('PASSWORD')
        # consumer_key = os.getenv('CONSUMER_KEY')
        # consumer_secret = os.getenv('CONSUMER_SECRET')
        # sf = Salesforce(username=username, password=password, consumer_key=consumer_key, consumer_secret=consumer_secret)
        
        # connect to salesforce with instance url, session id
        # instance_url = 'https://dwu00000ymz9b2af-dev-ed.develop.my.salesforce-setup.com'
        # session_id = '0AkWU00000uWg2R'      
        # sf = Salesforce(instance_url=instance_url, session_id=session_id)
        # accounts = sf.query("SELECT Id, Name, CreatedDate, CreatedBy.Name FROM Account")
        # for acc in accounts['records']:
        #     print(f"{acc['Name']} - Created: {acc['CreatedDate']} by {acc['CreatedBy']['Name']}")

        # connect to salesforce with consumer key, consumer secret, and domain name.
        consumer_key = os.getenv('CONSUMER_KEY')
        consumer_secret = os.getenv('CONSUMER_SECRET')
        domain = 'dwu00000ymz9b2af-dev-ed.develop.my'
        sf = Salesforce(consumer_key=consumer_key, consumer_secret=consumer_secret, domain=domain)
        return sf
    
    except Exception as e:
        print(f"✗ Failed to connect to Salesforce: {e}")
        return None



def create_accounts_batch(accounts:pd.DataFrame):
    """Create multiple accounts, skipping duplicates

        arguments:
            accounts: a dataframe containing all accounts needed to be created.

    """
    try:
        sf = connect_to_salesforce()
        account_names = accounts['Name']
        # Step 1: Query all existing accounts at once
        names_str = "', '".join([name.replace("'", "\\'") for name in account_names])
        query = f"SELECT Id, Name FROM Account WHERE Name IN ('{names_str}')"
        # query = f"SELECT Id, Name FROM Account WHERE CCN__c IN ('{}')"
        existing = sf.query(query)
        
        # existing_ccns = {record['CCN_c'] for record in existing['records']}
        existing_names = {record['Name'] for record in existing['records']}
        
        # Step 3: Create new accounts
        results = []
        for index, row in accounts.iterrows():
            name = row['Name']
            if name in existing_names: continue
            new_account = sf.Account.create({
                'Name': name
                





            })
            results.append({
                'Id': new_account['id'],
                'Name': name,
                'created': True
            })
            print(f"Created: {name}")
        
        # Add existing accounts to results
        for record in existing['records']:
            results.append({
                'Id': record['Id'],
                'Name': record['Name'],
                'created': False
            })
            print(f"Already exists: {record['Name']}")
        
        return results
    except SalesforceMalformedRequest as e:
        print(f"Invalid request: {e}")
        return
    except Exception as e:
        print(f"Error creating account: {e}")
        return

# # Usage
# accounts_to_create = ['Company A', 'Company B', 'Company C']
# results = create_accounts_batch(accounts_to_create)


if __name__=="__main__":
    connect_to_salesforce()