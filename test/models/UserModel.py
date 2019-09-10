from test.models.BaseModel import BaseModel
from common.utils.utils import random_string


class UserModel(BaseModel):
    def __init__(self,
                 email="myemail+" + random_string(6) + "@gmail.com",
                 password="Password1!",
                 confirm_password="Password1!",
                 first_name="James",
                 last_name="Brown",
                 address_1="Jacksonville 779",
                 address_2="Suite 120",
                 city="Los Angeles",
                 state="CA",
                 zip_code="12345",
                 country="US",
                 phone="876-55-44-33",
                 user_level="admin"
                 ):
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.first_name = first_name
        self.last_name = last_name
        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone = phone
        self.user_level = user_level
        super().__init__()
