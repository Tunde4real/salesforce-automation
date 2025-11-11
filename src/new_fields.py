# import internal modules
import os
import time
import json
import re
import traceback


# import external libraries
from dotenv import load_dotenv
from simple_salesforce import Salesforce
from simple_salesforce.metadata import SfdcMetadataApi


""" Programmatically create custom fields in Salesforce for Healthcare Facility data
"""

class SalesforceFieldManager:
    """Manage custom field creation using Metadata API
    """
    
    def __init__(self, sf):
        """
        Initialize with Salesforce connection
        
        Args:
            sf: simple_salesforce.Salesforce instance
        """
        self.sf = sf
        self.mdapi = sf.mdapi
        print("✓ Metadata API initialized\n")
    
    def check_field_exists(self, object_name, field_name):
        """
        Check if a custom field already exists.
        For some reasons, new fields created are not being returned as of now.
        
        Args:
            object_name: Object API name (e.g., 'Account')
            field_name: Field API name (e.g., 'CCN__c')
            
        Returns:
            bool: True if field exists, False otherwise
        """
        try:
            obj = getattr(self.sf, object_name)
            metadata = obj.describe()
            existing_fields = {field['name'] for field in metadata['fields']}
            return field_name in existing_fields
            
        except Exception as e:
            print(f"Warning: Could not check if field exists: {e}")
            return False
    
    def create_text_field(self, object_name, field_name, label, length=255, 
                         required=False, unique=False, external_id=False, 
                         description=None):
        """Create a text custom field
        """
        
        full_name = f"{object_name}.{field_name}"
        
        # Check if exists
        if self.check_field_exists(object_name, field_name):
            print(f"  ⊗ Field {field_name} already exists, skipping...")
            return {'success': False, 'message': 'Field already exists'}

        custom_field = self.mdapi.CustomField(
            fullName = full_name,
            label = label,
            type = self.mdapi.FieldType("Text"),
            length = length,
            required = required,
            unique = unique,
            externalId = external_id
        )
        
        if description:
            custom_field['description'] = description
        
        try:
            self.mdapi.CustomField.create(custom_field)
            print(f"  ✓ Created text field: {field_name}")
            return {'success': True, 'field': field_name}   
          
        except Exception as e:
            print(f"  ✗ Exception creating {field_name}: {str(e)}")
            return {'success': False, 'field': field_name, 'error': str(e)}
    
    def create_number_field(self, object_name, field_name, label, precision=18, 
                           scale=10, required=False, description=None):
        """Create a number custom field
            Precision represents the number of digits to the left of the decimal point.
        """
        
        full_name = f"{object_name}.{field_name}"
        
        if self.check_field_exists(object_name, field_name):
            print(f"  ⊗ Field {field_name} already exists, skipping...")
            return {'success': False, 'message': 'Field already exists'}
        
        custom_field = self.mdapi.CustomField(
            fullName = full_name,
            label = label,
            type = self.mdapi.FieldType("Number"),
            required = required,
            precision = precision,
            scale = scale
        )
        
        if description:
            # this has not been confirmed to be working
            custom_field['description'] = description
        
        try:
            self.mdapi.CustomField.create(custom_field)
            print(f"  ✓ Created text field: {field_name}")
            return {'success': True, 'field': field_name}  
                
        except Exception as e:
            print(f"  ✗ Exception creating {field_name}: {str(e)}")
            return {'success': False, 'field': field_name, 'error': str(e)}
    
    def create_checkbox_field(self, object_name, field_name, label, 
                             default_value=False, required=False, description=None):
        """Create a checkbox custom field"""
        
        full_name = f"{object_name}.{field_name}"
        
        if self.check_field_exists(object_name, field_name):
            print(f"  ⊗ Field {field_name} already exists, skipping...")
            return {'success': False, 'message': 'Field already exists'}
        
        custom_field = self.mdapi.CustomField(
            fullName = full_name,
            label = label,
            type = self.mdapi.FieldType("Checkbox"),
            required = required,
            defaultValue = default_value
        )
        
        if description:
            custom_field['description'] = description
        
        try:
            self.mdapi.CustomField.create(custom_field)
            print(f"  ✓ Created text field: {field_name}")
            return {'success': True, 'field': field_name}  
                
        except Exception as e:
            print(f"  ✗ Exception creating {field_name}: {str(e)}")
            return {'success': False, 'field': field_name, 'error': str(e)}
    
    def create_date_field(self, object_name, field_name, label, 
                         required=False, description=None):
        """Create a date custom field"""
        
        full_name = f"{object_name}.{field_name}"
        
        if self.check_field_exists(object_name, field_name):
            print(f"  ⊗ Field {field_name} already exists, skipping...")
            return {'success': False, 'message': 'Field already exists'}
        
        custom_field = self.mdapi.CustomField(
            fullName = full_name,
            label = label,
            type = self.mdapi.FieldType("Date"),
            required = required,
        )
        
        if description:
            custom_field['description'] = description
        
        try:
            self.mdapi.CustomField.create(custom_field)
            print(f"  ✓ Created text field: {field_name}")
            return {'success': True, 'field': field_name}   
                
        except Exception as e:
            print(f"  ✗ Exception creating {field_name}: {str(e)}")
            return {'success': False, 'field': field_name, 'error': str(e)}
    
    # def create_currency_field(self, object_name, field_name, label, precision=18, 
    #                          scale=10, required=False, description=None):
    #     """Create a currency custom field"""
        
    #     full_name = f"{object_name}.{field_name}"
        
    #     if self.check_field_exists(object_name, field_name):
    #         print(f"  ⊗ Field {field_name} already exists, skipping...")
    #         return {'success': False, 'message': 'Field already exists'}
        
    #     field_metadata = {
    #         'fullName': full_name,
    #         'label': label,
    #         'type': 'Currency',
    #         'precision': precision,
    #         'scale': scale,
    #         'required': required
    #     }
        
    #     if description:
    #         field_metadata['description'] = description
        
    #     try:
    #         result = self.metadata_api.create_metadata('CustomField', [field_metadata])
            
    #         if result and result[0].get('success'):
    #             print(f"  ✓ Created currency field: {field_name}")
    #             return {'success': True, 'field': field_name}
    #         else:
    #             error_msg = result[0].get('errors', [{}])[0].get('message', 'Unknown error') if result else 'No response'
    #             print(f"  ✗ Failed to create {field_name}: {error_msg}")
    #             return {'success': False, 'field': field_name, 'error': error_msg}
                
    #     except Exception as e:
    #         print(f"  ✗ Exception creating {field_name}: {str(e)}")
    #         return {'success': False, 'field': field_name, 'error': str(e)}

    # def create_geolocation_field(self, object_name, field_name, label, 
    #                              display_location_in_decimal=True, 
    #                              scale=7, required=False, description=None):
    #     """
    #     Create a geolocation custom field for latitude/longitude
        
    #     This creates a compound field with automatic Latitude and Longitude components.
    #     Access pattern in Salesforce:
    #     - Latitude: Field_Name__Latitude__s
    #     - Longitude: Field_Name__Longitude__s
    #     """
        
    #     full_name = f"{object_name}.{field_name}"
        
    #     if self.check_field_exists(object_name, field_name):
    #         print(f"  ⊗ Field {field_name} already exists, skipping...")
    #         return {'success': False, 'message': 'Field already exists'}
        
    #     field_metadata = {
    #         'fullName': full_name,
    #         'label': label,
    #         'type': 'Location',
    #         'displayLocationInDecimal': display_location_in_decimal,
    #         'scale': scale,
    #         'required': required
    #     }
        
    #     if description:
    #         field_metadata['description'] = description
        
    #     try:
    #         result = self.metadata_api.create_metadata('CustomField', [field_metadata])
            
    #         if result and result[0].get('success'):
    #             print(f"  ✓ Created geolocation field: {field_name}")
    #             print(f"    → Access latitude as: {field_name.replace('__c', '__Latitude__s')}")
    #             print(f"    → Access longitude as: {field_name.replace('__c', '__Longitude__s')}")
    #             return {'success': True, 'field': field_name}
    #         else:
    #             error_msg = result[0].get('errors', [{}])[0].get('message', 'Unknown error') if result else 'No response'
    #             print(f"  ✗ Failed to create {field_name}: {error_msg}")
    #             return {'success': False, 'field': field_name, 'error': error_msg}
                
    #     except Exception as e:
    #         print(f"  ✗ Exception creating {field_name}: {str(e)}")
    #         return {'success': False, 'field': field_name, 'error': str(e)}


def create_healthcare_fields(sf, delay=2):
    """
    Create all custom fields needed for healthcare facility data
    
    Args:
        sf: Salesforce connection
        delay: Seconds to wait between field creations
        
    Returns:
        dict: Summary of created and failed fields
    """
    
    field_manager = SalesforceFieldManager(sf)
    
    results = {
        'created': [],
        'failed': [],
        'skipped': []
    }
    
    print("Creating Healthcare Facility Custom Fields on Account Object")
    
    fields_to_create = []
    salesforce_inbuilt_fields = {
        'Provider Name': 'Name',
        'Provider Address': 'BillingStreet',
        'City/Town': 'BillingCity',
        'State': 'BillingState',
        'ZIP Code': 'BillingPostalCode',
        'Telephone Number': 'Phone',
        'Provider Type': 'Type',
        'Ownership Type': 'Industry',
    }
    with open('data/metadata.json') as file:
        metadata = json.loads(file.read()) 
        fields_metadata = metadata['columns']['fields']

        for field in fields_metadata:
            field_type = fields_metadata[field]
            if field in salesforce_inbuilt_fields:
                continue
            elif field == 'CMS Certification Number (CCN)' :
                fields_to_create += [
                    (field_type,
                    {
                        'object_name': 'Account',
                        'field_name': 'CCN__c',
                        'label': 'CMS Certification Number',
                        'length': 50,
                        'unique': True,
                        'external_id': True,
                        'description': 'CMS Certification Number (CCN) - unique identifier'
                    }
                    )
                ]
            elif field == 'County/Parish':
                fields_to_create += [
                    (field_type,{
                        "object_name":"Account",
                        "field_name":"County__c",
                        "label":"County"
                    })
                ]
            else:
                # remove unsupported characters 
                field = re.sub(r'[^A-Za-z0-9_]', ' ', field)
                if len(field) > 25:
                    words = field.split()
                    field = words[0]
                    for word in words[1:]:
                        abbreviate = False
                        if len(field) + len(word) > 25 or abbreviate==True:
                            abbreviate = True
                            field += f'_{word[0].upper()}'
                            # 40 characters is the limit for salesforce
                            # if greater than 40, keep at current lenght
                            if len(field) > 40:
                                field = field[:-2]
                                break
                        else: field += f'_{word}'

                try: field = field.replace(' ', '_')
                except: pass
                fields_to_create += [
                    (field_type,
                    {
                        'object_name': 'Account',
                        'field_name': f'{field}__c',
                        'label': f'{field}'
                    }
                    )
                ]
                

    total_fields = len(fields_to_create)
    
    # Create each field
    for index, (field_type, field_config) in enumerate(fields_to_create, 1):
        print(f"[{index}/{total_fields}] Creating {field_config['field_name']}...")
        
        # Call appropriate method based on field type
        if field_type == 'text':
            result = field_manager.create_text_field(**field_config)
        elif field_type == 'num':
            result = field_manager.create_number_field(**field_config)
        elif field_type == 'checkbox':
            result = field_manager.create_checkbox_field(**field_config)
        elif field_type == 'date':
            result = field_manager.create_date_field(**field_config)
        else:
            result = {'success': False, 'error': 'Unknown field type'}
        
        # Track results
        if result.get('success'):
            results['created'].append(field_config['field_name'])
        elif result.get('message') == 'Field already exists':
            results['skipped'].append(field_config['field_name'])
        else:
            results['failed'].append({
                'field': field_config['field_name'],
                'error': result.get('error', 'Unknown error')
            })
        
        # Delay between field creations
        if index < total_fields:
            time.sleep(delay)
    
    print(f"Successfully created {len(results['created'])} fields : {results['created']} ")
    print(f"{len(results['skipped'])} fields already existed and hence skipped : {results['skipped']}")
    print(f"{len(results['failed'])} fields failed: {results['failed']}")
    
    return results


def main():
    """Main execution function"""
    
    print("Healthcare Facility Custom Field Creator")
    print("Using simple-salesforce-metadata2\n")
    
    load_dotenv()
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    DOMAIN = os.getenv('DOMAIN')
    
    try:
        # Connect to Salesforce
        print("Connecting to Salesforce...")
        sf = Salesforce(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            domain=DOMAIN
        )
        sf.mdapi
        print("✓ Connected successfully\n")
        
        
        # Create all healthcare fields
        results = create_healthcare_fields(sf, delay=2)
        
        # Return results
        return results
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print(traceback.format_exc())
        return None


if __name__ == "__main__":
    results = main()
    
    if results:
        print("\n✓ Field creation process completed!")
        print(f"Total created: {len(results['created'])}")
    else:
        print("\n✗ Field creation process failed!")