import json

from nandboxbots.data.Image import Image
class Category:
    def __init__(self, dictionary):
        self.id = dictionary.get('id')
        self.name = dictionary.get('name')
        self.description = dictionary.get('description')
        self.softId = dictionary.get('soft_id')
        self.createdDate = dictionary.get('created_date')
        self.version = dictionary.get('version')
        self.status = dictionary.get('status')
        self.images = [Image(img) for img in dictionary.get('image', [])]

    def to_json_obj(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'soft_id': self.softId,
            'created_date': self.createdDate,
            'version': self.version,
            'status': self.status,
            'image': [img.to_json_obj() for img in self.images]
        }
