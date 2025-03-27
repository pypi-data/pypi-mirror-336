import json

from nandboxbots.data.ProductItem import ProductItem


class GetProductItemResponse:
    def __init__(self, obj):
        self.productItem = ProductItem(obj) if obj else None

    def to_json_obj(self):
        obj = {}
        if self.productItem:
            obj['productItem'] = self.productItem.to_json_obj()
        return obj
