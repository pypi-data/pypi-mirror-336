import json
from nandboxbots.data.Category import Category

class ListCollectionItemResponse:
    def __init__(self, category_list):
        # Directly initializing categories from the list of dictionaries
        self.categories = [Category(category_dict) for category_dict in category_list]

    def to_json_obj(self):
        # Returns a dictionary suitable for converting to JSON
        return {
            'data': [category.to_json_obj() for category in self.categories]
        }
