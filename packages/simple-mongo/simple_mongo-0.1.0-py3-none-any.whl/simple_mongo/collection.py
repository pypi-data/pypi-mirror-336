from .database import MongoDB
from bson import ObjectId
import re

class Collection:

    def __init__(self, **data):
        super().__setattr__('_data', data)
        self._collection_name = re.sub(r'(?<!^)(?=[A-Z])', '_', self.__class__.__name__).lower()

    def __str__(self):
        return str(self._data)

    def __getattr__(self, name):
        if name == '_data':
            return super().__getattribute__(name)
        
        result = self._data.get(name, None)
        if result is None:
            return None
            # raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        return result
    
    def __setattr__(self, name, value):
        if name == '_data' or name == '_collection_name':
            super().__setattr__(name, value)
            return
        self._data[name] = value
    
    @property
    def collection_name(self):
        return self._collection_name
    
    @property
    def id(self):
        return str(self._data.get('_id', None))
    
    @collection_name.setter
    def set_collection_name(self, name):
        self._collection_name = name

    def save(self):
        data : dict = self._data
        print(data)
        for k,v in data.items():
            print(k, v)
            if isinstance(v, Collection):
                result = v.save()
                print(f"{k} Id", result.inserted_id)
                data[k] = result.inserted_id
            if isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, Collection):
                        result = item.save()
                        print(f"{k} Id", result.inserted_id)
                        data[k][i] = result.inserted_id
        return MongoDB.create(self.collection_name, self._data)
    
    @classmethod
    def find(cls, id : str):
        result = MongoDB.find_one(cls().collection_name, {'_id': ObjectId(id)})

        if result is None:
            return None
        
        return cls(**result) 
    
    def update(self):
        return MongoDB.update_by_id(self._collection_name, self._data._id, self._data)
    
    def delete(self):
        return MongoDB.delete(self._collection_name, {'_id': ObjectId(self._data._id)})
    
    @classmethod
    def all(cls):
        result = MongoDB.all(cls()._collection_name)

        return [cls(**data)._data for data in result.to_list()]