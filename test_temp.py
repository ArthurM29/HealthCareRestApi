from test.models.UserModel import UserModel
from test.api.users_api import UsersAPI

# user = UserModel()
# users_api = UsersAPI(debug=True)
# users_api.payload = user.json()
# create_resp = users_api.create()
# print(create_resp)
#
# get_resp = users_api.read(12)
# print(get_resp.text)


from hypothesis import given, settings, Verbosity
import hypothesis.strategies as st


# def digit_sum(num):
#     if num <0:
#         return 0
#     sum = 0
#     while num != 0:
#         digit = num % 10
#         num = num // 10
#         sum += digit
#
#     return sum
#
#
# @settings(verbosity=Verbosity.verbose)
# @given(st.integers())
# def test_digit_sum(s):
#     assert isinstance(digit_sum(s), int)
#     assert digit_sum(s) >= 0

# def word_count(s):
#     return len(s.split())
#
#
#
# @settings(verbosity=Verbosity.verbose)
# @given(st.text())
# def test_word_count(s):
#     assert isinstance(word_count(s), int)
#     assert word_count(s) >= 0
#     print(word_count(s))

# def sort_list(list_):
#     for i in range(len(list_) - 1):
#         for j in range(len(list_) - 1):
#             if list_[j] > list_[j + 1]:
#                 temp = list_[j]
#                 list_[j] = list_[j + 1]
#                 list_[j + 1] = temp
#     return list_
#
#
# @settings(verbosity=Verbosity.verbose)
# @given(st.lists(st.integers()))
# def test_sort_list(ul):
#     sl = sort_list(ul)
#     assert isinstance(sl, list)
#     assert Counter(ul) == Counter(sl)
#     assert all(
#         x <= y for x, y in zip(sl, sl[1:])
#     )


