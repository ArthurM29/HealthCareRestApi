from test_framework.models.UserModel import UserModel

# from test_framework.api.users_api import UsersAPI
#
# h = {"content": "application/xml"}
#
# user = UserModel()
# users_api = UsersAPI(payload=user.json(), headers=h, debug=True)
# create_resp = users_api.create_user()
# print(create_resp)
#
# get_resp = users_api.get_user(create_resp.json()['id'])
# print(get_resp.text)

# import sqlite3
#
#
# def exec_db_query(db_file, sql, params=()):
#     """ take sql query as string and parameters as tuple """
#     connection = cursor = None
#     try:
#         connection = sqlite3.connect(db_file)
#         cursor = connection.cursor()
#         cursor.execute(sql, params)
#         # make the changes to the database persistent
#         connection.commit()
#         rows = cursor.fetchall()
#         return rows
#     except sqlite3.DatabaseError as err:
#         print(err)
#     finally:
#         # close communication with the database
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()
#
# sql = 'select  * from user where email=?'
#
# result = exec_db_query('data.sqlite', sql, params=('abc@mac.com',))
# print(result)


class Alphabet:
    def __init__(self, url, id=None):
        self._url = url
        self.id = id

        # getting the values

    @property
    def url(self):
        print('Getting value')
        if self.id:
            return self._url + '/' + str(self.id)
        else:
            return self._url

        # setting the values

    @url.setter
    def url(self, url):
        print('Setting value to ' + url)
        self._url = url


x = Alphabet('https://macadamian.com')
print(x.url)


