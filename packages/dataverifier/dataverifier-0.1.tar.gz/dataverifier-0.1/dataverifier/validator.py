
import re # importing regex module

class DATAVALIDATOR:
    """
    A class DATAVALIDATOR is created that houses attributes and several methods
    """
    def __init__(self, data):
        """A function was created using the __init__ constructor and the contains attributes data,datatype
        """
        self.data = data # This is the an attribute parsed into each method that is checked using regex
        self.datatype = None # This is an attribute parsed into each method that specified what datatype is being checked i.e email's phone, dates or url's

    def validate_email(self):
        """
            Validates whether the given data is a properly formatted email address.

            This method checks if the `self.data` attribute matches a valid email pattern.
            It updates `self.datatype` to 'email' before performing validation.

            Returns:
                bool: True if `self.data` is a valid email, False otherwise.
        """
        self.datatype = 'email' # specialised datatype
        return bool(re.match(r'^[a-zA-Z0-9_&*$!#+]+(\.)?@[a-zA-Z.-]+\.[a-zA-Z]{2,}$', self.data))# regex for checking emails

    def african_numbers(self):
        """
            Validates whether the given data is a properly formatted number belonging to the African continent.

            This method checks if the `self.data` attribute matches a valid african number pattern.
            It updates `self.datatype` to 'phone' and afterward it performs the validation.

            Returns:
                bool: True if `self.data` is a valid africannumber, False otherwise.
        """
        self.datatype = 'phone_number'
        pattern = r'^\+?(213\d{9}|20\d{10}|218\d{9}|212\d{9}|249\d{9}|216\d{9}|229\d{8}|226\d{8}|238\d{7}|225\d{8}|220\d{7}|233\d{9}|224\d{9}|245\d{7}|231\d{7}|223\d{8}|222\d{8}|227\d{8}|234\d{10}|221\d{9}|232\d{8}|228\d{8}|257\d{8}|211\d{9}|255\d{9}|256\d{9}|252\d{9}|254\d{9}|250\d{9}|291\d{7}|253\d{8}|244\d{9}|237\d{9}|236\d{8}|235\d{8}|242\d{9}|243\d{9}|240\d{9}|239\d{9}|241\d{9}|267\d{8}|266\d{8}|261\d{9}|258\d{9}|265\d{9}|264\d{9}|27\d{9}|268\d{8}|260\d{9}|263\d{9})$'# regex pattern for matching numbers in the african continent
        return bool(re.match(pattern, self.data)) # output

    def southAmerican_numbers(self):
        """
            Validates whether the given data is a properly formatted number belonging to the southamerican continent.

            This method checks if the `self.data` attribute matches a valid southamerican number pattern.
            It updates `self.datatype` to 'phone' and afterward it performs the validation.

            Returns:
                bool: True if `self.data` is a valid southamerican_number, False otherwise.
        """
        self.datatype = 'phone_number' #datatype for phonenumbers
        pattern = r'^\+?(54\d{8}|591\d{8}|55\d{10}|55\d{11}|56\d{8}|57\d{10}|593\d{8}|593\d{9}|58\d{10}|592\d{7}|595\d{9}|51\d{9}|597\d{8})$'
        return bool(re.match(pattern, self.data))

    def northAmerican_numbers(self):
        """
            Validates whether the given data is a properly formatted number belonging to the northamerican continent.

            This method checks if the `self.data` attribute matches a valid northamerican number pattern.
            It updates `self.datatype` to 'phone' and afterward it performs the validation.

            Returns:
                bool: True if `self.data` is a valid northamerican_number, False otherwise.
        """
        self.datatype = 'phone_number'
        pattern = r'^\+?(1(\s|-)?\d{3}(\s|-)?\d{3}(\s|-)?\d{4})$|^\+?(5(\s|-)?\d{2}(\s|-)?\d{4}(\s|-)?\d{4})$|^\+?(5\d{1}(\s|-)?\d{4}(\s|-)?\d{4})$|^\+?(5\d{2}(\s|-)?\d{3}(\s|-)?\d{4})$|^\+?(5\d{1}(\s|-)?\d{2}(\s|-)?\d{4}(\s|-)?\d{4})$'
        return bool(re.match(pattern, self.data))

    def australian_numbers(self):
        """
            Validates whether the given data is a properly formatted number belonging to the australian continent.

            This method checks if the `self.data` attribute matches a valid australian number pattern.
            It updates `self.datatype` to 'phone' and afterward it performs the validation.

            Returns:
                bool: True if `self.data` is a valid australian_number, False otherwise.
        """
        self.datatype = 'phone_number'
        pattern = r'^\+61\s?\d{1}\s?\d{4}\s?\d{4}$'
        return bool(re.match(pattern, self.data))

    def asian_numbers(self):
        """
            Validates whether the given data is a properly formatted number belonging to the asian continent.

            This method checks if the `self.data` attribute matches a valid asian number pattern.
            It updates `self.datatype` to 'phone' and afterward it performs the validation.

            Returns:
                bool: True if `self.data` is a valid asian number, False otherwise.
        """
        self.datatype = 'phone_number'
        asian_pattern = r'^\+((93\d{8})|(374\d{8,9})|(994\d{8,9})|(973\d{8})|(880\d{10})|(975\d{8})|(673\d{7})|(855\d{8})|(86\d{11})|(995\d{9})|(852\d{8})|(91\d{10})|(62\d{10})|(98\d{10})|(964\d{10})|(972\d{9})|(81\d{10})|(962\d{9})|(7\d{10})|(965\d{8})|(996\d{9})|(856\d{8})|(961\d{8})|(853\d{8})|(60\d{9})|(960\d{7})|(976\d{8})|(95\d{9})|(977\d{9})|(850\d{6,17})|(968\d{8})|(92\d{10})|(63\d{10})|(974\d{8})|(966\d{9})|(65\d{8})|(82\d{10})|(94\d{9})|(963\d{9})|(886\d{9})|(992\d{9})|(66\d{9})|(90\d{10})|(993\d{8})|(971\d{9})|(998\d{9})|(84\d{10})|(967\d{9}))$'
        return bool(re.match(asian_pattern, self.data))

    def european_numbers(self):
        """
            Validates whether the given data is a properly formatted number belonging to the european continent.

            This method checks if the `self.data` attribute matches a valid european number pattern.
            It updates `self.datatype` to 'phone' and afterward it performs the validation.

            Returns:
                bool: True if `self.data` is a valid european number, False otherwise.
        """
        self.datatype = 'phone_number'
        europe_pattern =r'^\+?(44(\s|-)?\d{2,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|49(\s|-)?\d{1,4}(\s|-)?\d{2,4}(\s|-)?\d{4,9}$|33(\s|-)?\d{1}(\s|-)?\d{2}(\s|-)?\d{2}(\s|-)?\d{2}(\s|-)?\d{2}$|34(\s|-)?\d{2}(\s|-)?\d{3}(\s|-)?\d{2}(\s|-)?\d{2}$|39(\s|-)?\d{2,4}(\s|-)?\d{6,10}$|31(\s|-)?\d{1,2}(\s|-)?\d{3}(\s|-)?\d{4}$|32(\s|-)?\d{1,2}(\s|-)?\d{3}(\s|-)?\d{4}$|46(\s|-)?\d{1,3}(\s|-)?\d{2,4}(\s|-)?\d{4}$|47(\s|-)?\d{2}(\s|-)?\d{2}(\s|-)?\d{2}(\s|-)?\d{2}$|41(\s|-)?\d{2}(\s|-)?\d{3}(\s|-)?\d{2}(\s|-)?\d{2}$|43(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|45(\s|-)?\d{2}(\s|-)?\d{2}(\s|-)?\d{2}(\s|-)?\d{2}$|358(\s|-)?\d{1,3}(\s|-)?\d{3,4}(\s|-)?\d{4}$|353(\s|-)?\d{1,3}(\s|-)?\d{3,4}(\s|-)?\d{4}$|30(\s|-)?\d{2,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|48(\s|-)?\d{2}(\s|-)?\d{3}(\s|-)?\d{3}(\s|-)?\d{3}$|351(\s|-)?\d{2}(\s|-)?\d{3}(\s|-)?\d{4}$|420(\s|-)?\d{3}(\s|-)?\d{3}(\s|-)?\d{3}$|36(\s|-)?\d{1,2}(\s|-)?\d{3}(\s|-)?\d{4}$|359(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|40(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|421(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|386(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|385(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|372(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|371(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|370(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|357(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|352(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|356(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|354(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|376(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|355(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|375(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|387(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|389(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|373(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|382(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|381(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|380(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4}$|7(\s|-)?\d{1,4}(\s|-)?\d{3,4}(\s|-)?\d{4})$'
        return bool(re.match(europe_pattern, self.data))

    def validate_phone(self):
        """
            Validates whether the given data is a properly formatted number belonging to all six continents in my class DATAVALIDATOR 

            This method checks if the `self.data` attribute matches a valid phonenumber pattern in the specified six continents.
            It updates `self.datatype` to 'phone' and afterward it performs the validation.

            Returns:
                bool: True if `self.data` is a valid phone_number in those six continents, False otherwise.
        """
        self.datatype = 'phone_number'# datatype for validating phonenumbers
        # the code below groups all phone numbers frommeach continent and stores them in a list named valid_regions
        valid_regions = [
            self.african_numbers,
            self.asian_numbers,
            self.australian_numbers,
            self.southAmerican_numbers,
            self.northAmerican_numbers,
            self.european_numbers
        ]
        """
        The for loop iterates through the list "valid_regions" and returns true if the phone number is a valid one else false
        """
        for method in valid_regions:# for loop for looping through each attribute that can validate phone numbers
            if method():
                return True # output(bool) is the method is a valid phone number
        return False # output(bool) is the method is a invalid phone number

    def validate_date(self):
        """
            Validates whether the given data is a properly formatted date.

            This method checks if the `self.data` attribute matches a valid date format.
            It updates `self.datatype` to 'email' before performing validation.

            Returns:
                bool: True if `self.data` is a valid date, False otherwise.
        """
        self.datatype = 'date'
        """
        Regular expression pattern for validating date formats.

        This pattern supports multiple date formats, including:
            - DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY
            - YYYY/MM/DD, YYYY-MM-DD, YYYY.MM.DD
            - Supports both two-digit and four-digit years.

        Pattern Explanation:
            -Matches day (01-31), month (01-12), and year (two or four digits). 
            - Allows separators `/`, `-`, or `.` between date components.
            - Supports both `DD/MM/YYYY` and `YYYY/MM/DD` formats.

        Example Matches:
            - "12/05/2024"
            - "2024-05-12"
            - "01.01.99"

        Non-Matches:
            - "32/01/2024" (Invalid day)
            - "2024/13/12" (Invalid month)
            - "05-2024-12" (Incorrect format)
        """
        date_pattern = r'((0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[0-2])[\/\-\.](\d{4}|\d{2}))|((\d{4}|\d{2})[\/\-\.](0?[1-9]|1[0-2])[\/\-\.](0?[1-9]|[12][0-9]|3[01]))$'
        return bool(re.match(date_pattern, self.data))

    def validate_url(self):
        """
            Validates whether the given data is a properly formatted url address.

            This method checks if the `self.data` attribute matches a valid url format.
            It updates `self.datatype` to 'email' before performing validation.

            Returns:
                bool: True if `self.data` is a valid url, False otherwise.
        """
        self.datatype = 'url'
        """
        Regex fpr matching valid url's
        A url could begin with a www|http://www|https://www followed by the dot notation and afterwards match any [-a-zA-Z0-9@:%._\#=] charater in the closed bracket, then a dot notation followed by the domain name
        the domain name is restricted to contain a min of a 1 character and a max of 6. A special group that could occur or not(*meaning zero or more)is included to accout for url's of dynamis websites that could have several sublinks
            Note: Special characters are escaped using backward slash 
        Valid matches
            - www.google.com
            - https://docs.pytest.org/en/stable/how-to/capture-warnings.html
            - http://wiki.com
        """
        pattern = r'^(https?:\/\/(www\.))?[-a-zA-Z0-9@:%._\+~#=]\.[a-zA-Z0-9]{1,6}([-a-zA-Z0-9@:%_\.#?&//=]*)|(www\.)[-a-zA-Z0-9@:%._\+~#=]\.[a-zA-Z0-9]{1,6}([-a-zA-Z0-9@:%_\.#?&//=]*)$'#regex pattern
        return bool(re.match(pattern, self.data))# output for valid and invalid regex
