import json


class BaseModel(object):
    def __init__(self):
        pass

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    @staticmethod
    #TODO turn this into an instace method
    def remove_element(dic, path):
        """Take json path and remove element from dictionary"""
        if len(path) == 0:
            raise ValueError('Empty json path')
        path_list = path.split('.')

        def remove_el(dic, path_list):
            if len(path_list) == 1:
                try:
                    del dic[path_list[0]]
                except KeyError:
                    raise KeyError(f"Key '{path_list[0]}' does not exist in dictionary {dic}")
            else:
                remove_el(dic[path_list[0]], path_list[1:])

        remove_el(dic, path_list)

    def remove_fields(self, attributes):
        for attr in attributes:
            delattr(self, attr)

    def remove_field(self, attr):
        delattr(self, attr)

