# import internal modules
import os

# import external modules
import requests
import pandas as pd


def main():
    """ Creates new accounts from dataset of all nursing homes in the following states: 
        Arizona, Nevada, Utah & Colorado. First checks if such account exists, if not creates it.

        New fields needed:
        Assigned Sales rep


    """
    #       Work with sql query endpoint. One state query works, many states query does not
    # query = '[SELECT * FROM 0ae91eb2-22da-5fe3-9dce-9811cdd6f1a8][WHERE State IN ("AZ", "NV", "UT", "CO")][LIMIT 2]'
    # query_one_state = '[SELECT * FROM 0ae91eb2-22da-5fe3-9dce-9811cdd6f1a8][WHERE State = "AZ"][LIMIT 10]'
    # request_url = f'https://data.cms.gov/provider-data/api/1/datastore/sql?query={query_one_state}'
    # response = requests.get(request_url, headers={'accept': 'application/json'})
    # data = response.json()

    df = pd.read_csv('https://data.cms.gov/provider-data/sites/default/files/resources/e923f267504f72a3b10c2daa39efed8a_1757685912/NH_ProviderInfo_Sep2025.csv')
    df = df[df['State'].isin(['AZ', 'NV', 'UT', 'CO'])]
    df.rename(columns={
        # slaesforce standard feilds
        'Provider Name': 'Name',
        'Provider Address': 'BillingStreet',
        'City/Town': 'BillingCity',
        'State': 'BillingState',
        'ZIP Code': 'BillingPostalCode',
        'Telephone Number': 'Phone',
        'Provider Type': 'Type',
        'Ownership Type': 'Industry',
        
        # Custom Fields
        'CMS Certification Number (CCN)': 'CCN__c',
        'Legal Business Name': 'Legal_Business_Name__c',
        'Provider SSA County Code': 'SSA_County_Code__c',
        'County/Parish': 'County__c',
        'Number of Certified Beds': 'Certified_Beds__c',
        'Average Number of Residents per Day': 'Avg_Residents_Per_Day__c',
        'Chain Name': 'Chain_Name__c',
        'Chain ID': 'Chain_ID__c',
        'Number of Facilities in Chain': 'Facilities_In_Chain__c',
        'Overall Rating': 'Overall_Rating__c',
        'Health Inspection Rating': 'Health_Inspection_Rating__c',
        'QM Rating': 'QM_Rating__c',
        'Staffing Rating': 'Staffing_Rating__c',
        'Special Focus Status': 'Special_Focus_Status__c',
        'Provider Changed Ownership in Last 12 Months': 'Ownership_Changed_12Mo__c',
        'Latitude': 'Geolocation__Latitude__s',  # Salesforce geolocation field
        'Longitude': 'Geolocation__Longitude__s',  # Salesforce geolocation field
        'Date First Approved to Provide Medicare and Medicaid Services': 'Medicare_Medicaid_Approval_Date__c',
    }, 
        inplace=True
    )



if __name__ == "__main__":
    main()

"""
"015009","BURNS NURSING HOME, INC.","701 MONROE STREET NW","RUSSELLVILLE","AL","35653","2563324110","290","Franklin",For profit - Corporation,57,44.6,,Medicare and Medicaid,"N","BURNS NURSING HOME, INC.",1969-09-01,,,,,,,,N,,N,Y,N,Resident,Yes,3,,2,,4,,5,,3,,5,,,,2.84006,0.51925,1.27714,1.79639,4.63645,3.77686,0.72445,0.01135,23.810,,7.143,,0,,1.34467,0.97336,2.24172,0.84503,0.65968,3.74643,3.31331,2.90180,0.53054,1.30490,4.73725,3.85897,2023-03-02,4,4,3,56,1,0,56,2019-08-21,2,2,0,8,1,0,8,44.000,2,0,,1,23989.00,0,1,"701 MONROE STREET NW,RUSSELLVILLE,AL,35653",34.5149,-87.736,,2025-09-01

"""