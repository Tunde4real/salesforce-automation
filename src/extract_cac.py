# import internal modules
import json

# import external modules
import requests
from bs4 import BeautifulSoup



""" Module documentation
"""


def extract_cac(provider_name:str):
    """ Extract Cheif Administrator Contact of an health care facility, provided it's name.
        This method uses the requests library to send a post requests. This post requests 
        requires a hidden user id available in the form data. A future update would be to use
        browser automation to automatically fetch the user id.

        arguments:
            provider_name : the name of the health care facility

        returns:
            cheif_administrator : The name of the cheif administrator for the facility
    """

    # Fecth facility id
    url = f"https://hsapps.azdhs.gov/ls/sod/Provider.aspx?ProviderName={provider_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    hidden_id = soup.find(id="ctl00_ContentPlaceHolder1_HiddenField1").get('value')

    # fetch facility details
    url = 'https://azcarecheck.azdhs.gov/s/sfsites/aura?r=1&aura.ApexAction.execute=2'
    form_data = {
        'message' : '{"actions":[{"id":"79;a","descriptor":"aura://ApexActionController/ACTION$execute","callingDescriptor":"UNKNOWN","params":{"namespace":"","classname":"AZCCFacilityDetailsTabController","method":"getFacilityDetails","params":{"facilityId":"' + hidden_id + '"},"cacheable":true,"isContinuation":false}}]}',
        'aura.context' : '{"mode":"PROD","fwuid":"VFJhRGxfRlFsN29ySGg2SXFsaUZsQTFLcUUxeUY3ZVB6dE9hR0VheDVpb2cxMy4zMzU1NDQzMi4yNTE2NTgyNA","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"1411_cmG25dptuXHlZVEVTc27wQ"},"dn":[],"globals":{},"uad":true}',
        'aura.pageURI' : f'/s/facility-details?facilityId={hidden_id}&programType=Health%20Care%20Facilties',
        'aura.token' : 'null'
    }
    headers = {
        'Origin': 'https://azcarecheck.azdhs.gov',
        "Referer" : f"https://azcarecheck.azdhs.gov/s/facility-details?facilityId={hidden_id}&programType=Health%20Care%20Facilties",
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    response = requests.post(url, headers=headers, data=form_data)
    response_json = json.loads(response.text)
    cheif_administrator = response_json['actions'][0]['returnValue']['returnValue']['chiefAdministrativeOfficer']
    names = cheif_administrator.split()
    first_name, last_name = names[0], names[-1]

    return [first_name, last_name]


if __name__ == "__main__":
    extract_cac()