d = {'a': 1, 'b': 2, 'c': 3}

new_dict = {k: v for k, v in d.items() if k != 'c'}

print(new_dict)
