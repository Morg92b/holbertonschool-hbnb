from abc import ABC, abstractmethod
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity, PlaceAmenity
from app.models.review import Review
from sqlalchemy.orm import subqueryload
from sqlalchemy.orm import joinedload

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


# class InMemoryRepository(Repository):
#     def __init__(self):
#         self._storage = {}

#     def add(self, obj):
#         self._storage[obj.id] = obj

#     def get(self, obj_id):
#         return self._storage.get(obj_id)

#     def get_all(self):
#         return list(self._storage.values())

#     def update(self, obj_id, updated_obj):
#         self._storage[obj_id] = updated_obj

#     def delete(self, obj_id):
#         if obj_id in self._storage:
#             del self._storage[obj_id]

#     def get_by_attribute(self, attr_name, attr_value):
#         return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
    

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    # def update(self, obj_id, data):
    #     obj = self.get(obj_id)
    #     if obj:
    #         for key, value in data.items():
    #             setattr(obj, key, value)
    #         db.session.commit()

    def update(self, obj_id, obj):
        existing_obj = self.get(obj_id)
        if existing_obj:
            for key, value in vars(obj).items():
                if hasattr(existing_obj, key) and getattr(existing_obj, key) != value:
                    setattr(existing_obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter_by(**{attr_name: attr_value}).first()


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)


class PlaceAmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(PlaceAmenity)


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

