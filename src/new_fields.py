"""
Programmatically create custom fields in Salesforce for Healthcare Facility data
Using simple-salesforce-metadata2 library for easier implementation

Installation:
pip install simple-salesforce simple-salesforce-metadata2
"""

from simple_salesforce import Salesforce
from simple_salesforce.metadata import SfdcMetadataApi
import time


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
        self.metadata_api = SfdcMetadataApi(
            session_id=sf.session_id,
            instance=sf.sf_instance
        )
        print("✓ Metadata API initialized\n")
    
    def check_field_exists(self, object_name, field_name):
        """
        Check if a custom field already exists
        
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
        
        field_metadata = {
            'fullName': full_name,
            'label': label,
            'type': 'Text',
            'length': length,
            'required': required,
            'unique': unique,
            'externalId': external_id
        }
        
        if description:
            field_metadata['description'] = description
        
        try:
            result = self.metadata_api.create_metadata('CustomField', [field_metadata])
            
            if result and result[0].get('success'):
                print(f"  ✓ Created text field: {field_name}")
                return {'success': True, 'field': field_name}
            else:
                error_msg = result[0].get('errors', [{}])[0].get('message', 'Unknown error') if result else 'No response'
                print(f"  ✗ Failed to create {field_name}: {error_msg}")
                return {'success': False, 'field': field_name, 'error': error_msg}
                
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
        
        field_metadata = {
            'fullName': full_name,
            'label': label,
            'type': 'Number',
            'precision': precision,
            'scale': scale,
            'required': required
        }
        
        if description:
            field_metadata['description'] = description
        
        try:
            result = self.metadata_api.create_metadata('CustomField', [field_metadata])
            
            if result and result[0].get('success'):
                print(f"  ✓ Created number field: {field_name}")
                return {'success': True, 'field': field_name}
            else:
                error_msg = result[0].get('errors', [{}])[0].get('message', 'Unknown error') if result else 'No response'
                print(f"  ✗ Failed to create {field_name}: {error_msg}")
                return {'success': False, 'field': field_name, 'error': error_msg}
                
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
        
        field_metadata = {
            'fullName': full_name,
            'label': label,
            'type': 'Checkbox',
            'defaultValue': default_value,
            'required': required
        }
        
        if description:
            field_metadata['description'] = description
        
        try:
            result = self.metadata_api.create_metadata('CustomField', [field_metadata])
            
            if result and result[0].get('success'):
                print(f"  ✓ Created checkbox field: {field_name}")
                return {'success': True, 'field': field_name}
            else:
                error_msg = result[0].get('errors', [{}])[0].get('message', 'Unknown error') if result else 'No response'
                print(f"  ✗ Failed to create {field_name}: {error_msg}")
                return {'success': False, 'field': field_name, 'error': error_msg}
                
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
        
        field_metadata = {
            'fullName': full_name,
            'label': label,
            'type': 'Date',
            'required': required
        }
        
        if description:
            field_metadata['description'] = description
        
        try:
            result = self.metadata_api.create_metadata('CustomField', [field_metadata])
            
            if result and result[0].get('success'):
                print(f"  ✓ Created date field: {field_name}")
                return {'success': True, 'field': field_name}
            else:
                error_msg = result[0].get('errors', [{}])[0].get('message', 'Unknown error') if result else 'No response'
                print(f"  ✗ Failed to create {field_name}: {error_msg}")
                return {'success': False, 'field': field_name, 'error': error_msg}
                
        except Exception as e:
            print(f"  ✗ Exception creating {field_name}: {str(e)}")
            return {'success': False, 'field': field_name, 'error': str(e)}
    
    def create_picklist_field(self, object_name, field_name, label, 
                             picklist_values, required=False, description=None):
        """Create a picklist custom field"""
        
        full_name = f"{object_name}.{field_name}"
        
        if self.check_field_exists(object_name, field_name):
            print(f"  ⊗ Field {field_name} already exists, skipping...")
            return {'success': False, 'message': 'Field already exists'}
        
        # Format picklist values
        formatted_values = []
        for idx, value in enumerate(picklist_values):
            formatted_values.append({
                'fullName': value,
                'default': idx == 0  # First value is default
            })
        
        field_metadata = {
            'fullName': full_name,
            'label': label,
            'type': 'Picklist',
            'required': required,
            'valueSet': {
                'valueSetDefinition': {
                    'sorted': False,
                    'value': formatted_values
                }
            }
        }
        
        if description:
            field_metadata['description'] = description
        
        try:
            result = self.metadata_api.create_metadata('CustomField', [field_metadata])
            
            if result and result[0].get('success'):
                print(f"  ✓ Created picklist field: {field_name}")
                return {'success': True, 'field': field_name}
            else:
                error_msg = result[0].get('errors', [{}])[0].get('message', 'Unknown error') if result else 'No response'
                print(f"  ✗ Failed to create {field_name}: {error_msg}")
                return {'success': False, 'field': field_name, 'error': error_msg}
                
        except Exception as e:
            print(f"  ✗ Exception creating {field_name}: {str(e)}")
            return {'success': False, 'field': field_name, 'error': str(e)}
    
    def create_currency_field(self, object_name, field_name, label, precision=18, 
                             scale=10, required=False, description=None):
        """Create a currency custom field"""
        
        full_name = f"{object_name}.{field_name}"
        
        if self.check_field_exists(object_name, field_name):
            print(f"  ⊗ Field {field_name} already exists, skipping...")
            return {'success': False, 'message': 'Field already exists'}
        
        field_metadata = {
            'fullName': full_name,
            'label': label,
            'type': 'Currency',
            'precision': precision,
            'scale': scale,
            'required': required
        }
        
        if description:
            field_metadata['description'] = description
        
        try:
            result = self.metadata_api.create_metadata('CustomField', [field_metadata])
            
            if result and result[0].get('success'):
                print(f"  ✓ Created currency field: {field_name}")
                return {'success': True, 'field': field_name}
            else:
                error_msg = result[0].get('errors', [{}])[0].get('message', 'Unknown error') if result else 'No response'
                print(f"  ✗ Failed to create {field_name}: {error_msg}")
                return {'success': False, 'field': field_name, 'error': error_msg}
                
        except Exception as e:
            print(f"  ✗ Exception creating {field_name}: {str(e)}")
            return {'success': False, 'field': field_name, 'error': str(e)}

    def create_geolocation_field(self, object_name, field_name, label, 
                                 display_location_in_decimal=True, 
                                 scale=7, required=False, description=None):
        """
        Create a geolocation custom field for latitude/longitude
        
        This creates a compound field with automatic Latitude and Longitude components.
        Access pattern in Salesforce:
        - Latitude: Field_Name__Latitude__s
        - Longitude: Field_Name__Longitude__s
        """
        
        full_name = f"{object_name}.{field_name}"
        
        if self.check_field_exists(object_name, field_name):
            print(f"  ⊗ Field {field_name} already exists, skipping...")
            return {'success': False, 'message': 'Field already exists'}
        
        field_metadata = {
            'fullName': full_name,
            'label': label,
            'type': 'Location',
            'displayLocationInDecimal': display_location_in_decimal,
            'scale': scale,
            'required': required
        }
        
        if description:
            field_metadata['description'] = description
        
        try:
            result = self.metadata_api.create_metadata('CustomField', [field_metadata])
            
            if result and result[0].get('success'):
                print(f"  ✓ Created geolocation field: {field_name}")
                print(f"    → Access latitude as: {field_name.replace('__c', '__Latitude__s')}")
                print(f"    → Access longitude as: {field_name.replace('__c', '__Longitude__s')}")
                return {'success': True, 'field': field_name}
            else:
                error_msg = result[0].get('errors', [{}])[0].get('message', 'Unknown error') if result else 'No response'
                print(f"  ✗ Failed to create {field_name}: {error_msg}")
                return {'success': False, 'field': field_name, 'error': error_msg}
                
        except Exception as e:
            print(f"  ✗ Exception creating {field_name}: {str(e)}")
            return {'success': False, 'field': field_name, 'error': str(e)}



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
    
    # Define all fields to create
    fields_to_create = [
        # Text Fields
        ('text', {
            'object_name': 'Account',
            'field_name': 'CCN__c',
            'label': 'CMS Certification Number',
            'length': 50,
            'unique': True,
            'external_id': True,
            'description': 'CMS Certification Number (CCN) - unique identifier'
        }),
        ('text', {
            'object_name': 'Account',
            'field_name': 'Legal_Business_Name__c',
            'label': 'Legal Business Name',
            'length': 255,
            'description': 'Legal business name of the facility'
        }),
        ('text', {
            'object_name': 'Account',
            'field_name': 'SSA_County_Code__c',
            'label': 'SSA County Code',
            'length': 10,
            'description': 'Provider SSA County Code'
        }),
        ('text', {
            'object_name': 'Account',
            'field_name': 'County__c',
            'label': 'County',
            'length': 100,
            'description': 'County or Parish'
        }),
        ('text', {
            'object_name': 'Account',
            'field_name': 'Chain_Name__c',
            'label': 'Chain Name',
            'length': 255,
            'description': 'Name of the healthcare chain'
        }),
        ('text', {
            'object_name': 'Account',
            'field_name': 'Chain_ID__c',
            'label': 'Chain ID',
            'length': 50,
            'description': 'Chain identification number'
        }),
        ('text', {
            'object_name': 'Account',
            'field_name': 'Special_Focus_Status__c',
            'label': 'Special Focus Status',
            'length': 50,
            'description': 'Special Focus Facility status'
        }),
        
        # Number Fields
        ('number', {
            'object_name': 'Account',
            'field_name': 'Certified_Beds__c',
            'label': 'Number of Certified Beds',
            'precision': 10,
            'scale': 0,
            'description': 'Number of certified beds in the facility'
        }),
        ('number', {
            'object_name': 'Account',
            'field_name': 'Avg_Residents_Per_Day__c',
            'label': 'Average Residents Per Day',
            'precision': 10,
            'scale': 2,
            'description': 'Average number of residents per day'
        }),
        ('number', {
            'object_name': 'Account',
            'field_name': 'Facilities_In_Chain__c',
            'label': 'Facilities in Chain',
            'precision': 10,
            'scale': 0,
            'description': 'Number of facilities in the chain'
        }),
        ('number', {
            'object_name': 'Account',
            'field_name': 'Overall_Rating__c',
            'label': 'Overall Rating',
            'precision': 3,
            'scale': 1,
            'description': 'Overall 5-star rating (0-5)'
        }),
        ('number', {
            'object_name': 'Account',
            'field_name': 'Health_Inspection_Rating__c',
            'label': 'Health Inspection Rating',
            'precision': 3,
            'scale': 1,
            'description': 'Health inspection rating (0-5)'
        }),
        ('number', {
            'object_name': 'Account',
            'field_name': 'QM_Rating__c',
            'label': 'QM Rating',
            'precision': 3,
            'scale': 1,
            'description': 'Quality Measures rating (0-5)'
        }),
        ('number', {
            'object_name': 'Account',
            'field_name': 'Staffing_Rating__c',
            'label': 'Staffing Rating',
            'precision': 3,
            'scale': 1,
            'description': 'Staffing rating (0-5)'
        }),
        ('number', {
            'object_name': 'Account',
            'field_name': 'Latitude__c',
            'label': 'Latitude',
            'precision': 10,
            'scale': 7,
            'description': 'Latitude coordinate'
        }),
        ('number', {
            'object_name': 'Account',
            'field_name': 'Longitude__c',
            'label': 'Longitude',
            'precision': 10,
            'scale': 7,
            'description': 'Longitude coordinate'
        }),
        
        # Checkbox Fields
        ('checkbox', {
            'object_name': 'Account',
            'field_name': 'Ownership_Changed_12Mo__c',
            'label': 'Ownership Changed (12 Months)',
            'default_value': False,
            'description': 'Provider changed ownership in last 12 months'
        }),
        ('checkbox', {
            'object_name': 'Account',
            'field_name': 'Resides_In_Hospital__c',
            'label': 'Resides in Hospital',
            'default_value': False,
            'description': 'Provider resides in hospital'
        }),
        ('checkbox', {
            'object_name': 'Account',
            'field_name': 'CCRC__c',
            'label': 'Continuing Care Retirement Community',
            'default_value': False,
            'description': 'Is a Continuing Care Retirement Community'
        }),
        ('checkbox', {
            'object_name': 'Account',
            'field_name': 'Has_Resident_Family_Council__c',
            'label': 'Has Resident Family Council',
            'default_value': False,
            'description': 'With a Resident and Family Council'
        }),
        ('checkbox', {
            'object_name': 'Account',
            'field_name': 'Has_Sprinkler_Systems__c',
            'label': 'Has Sprinkler Systems',
            'default_value': False,
            'description': 'Automatic sprinkler systems in all required areas'
        }),
        
        # Date Fields
        ('date', {
            'object_name': 'Account',
            'field_name': 'Medicare_Medicaid_Approval_Date__c',
            'label': 'Medicare/Medicaid Approval Date',
            'description': 'Date first approved to provide Medicare and Medicaid services'
        }),
    ]
    
    total_fields = len(fields_to_create)
    
    # Create each field
    for idx, (field_type, field_config) in enumerate(fields_to_create, 1):
        print(f"[{idx}/{total_fields}] Creating {field_config['field_name']}...")
        
        # Call appropriate method based on field type
        if field_type == 'text':
            result = field_manager.create_text_field(**field_config)
        elif field_type == 'number':
            result = field_manager.create_number_field(**field_config)
        elif field_type == 'checkbox':
            result = field_manager.create_checkbox_field(**field_config)
        elif field_type == 'date':
            result = field_manager.create_date_field(**field_config)
        elif field_type == 'picklist':
            result = field_manager.create_picklist_field(**field_config)
        elif field_type == 'currency':
            result = field_manager.create_currency_field(**field_config)
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
        if idx < total_fields:
            time.sleep(delay)
    
    # Print summary
    print(f"\n{'='*70}")
    print("Field Creation Summary")
    print(f"{'='*70}")
    print(f"Successfully created: {len(results['created'])}")
    print(f"Already existed (skipped): {len(results['skipped'])}")
    print(f"Failed: {len(results['failed'])}")
    
    if results['created']:
        print("\nCreated fields:")
        for field in results['created']:
            print(f"  ✓ {field}")
    
    if results['skipped']:
        print("\nSkipped (already exist):")
        for field in results['skipped']:
            print(f"  ⊗ {field}")
    
    if results['failed']:
        print("\nFailed fields:")
        for failed in results['failed']:
            print(f"  ✗ {failed['field']}: {failed['error']}")
    
    print(f"{'='*70}\n")
    
    return results


def main():
    """Main execution function"""
    
    print("Healthcare Facility Custom Field Creator")
    print("Using simple-salesforce-metadata2\n")
    
    # Salesforce connection details
    CONSUMER_KEY = 'your_consumer_key_here'
    CONSUMER_SECRET = 'your_consumer_secret_here'
    DOMAIN = 'dwu00000ymz9b2af-dev-ed.develop.my'
    
    try:
        # Connect to Salesforce
        print("Connecting to Salesforce...")
        sf = Salesforce(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            domain=DOMAIN
        )
        print("✓ Connected successfully\n")
        
        # Create all healthcare fields
        results = create_healthcare_fields(sf, delay=2)
        
        # Return results
        return results
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return None


if __name__ == "__main__":
    results = main()
    
    if results:
        print("\n✓ Field creation process completed!")
        print(f"Total created: {len(results['created'])}")
    else:
        print("\n✗ Field creation process failed!")