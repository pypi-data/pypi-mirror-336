from simple_mongo.collection import Collection
from simple_mongo.database import MongoDB
class Users(Collection):
    collection_name = 'users'
    # def __init__(self, **data):
    #     super().__init__(**data)
    pass

class Address(Collection):
    collection_name = 'address'

def main():
    from pprint import pprint
    # result = MongoDB.create('users', {'name': 'John Doe', 'email': 'johndoe@gmail.com'})

    # if result:
    #     print('Document inserted successfully')
    # else:
    #     print('Document insertion failed')

    # MongoDB.all('users')
    address = Address(street='123 Main St.', city='Quezon City')
    # new_user = Users(name='John Doe Jr.', age=25, address=address)
    new_user = Users(name='John Doe III.', age=25)

    print(hasattr(new_user, '_data')) # True
    print(hasattr(address, '_data')) # True

    new_user.address = address

    # print(new_user.name)

    # new_user.gender = 'male'
    # # print(new_user.address.street)

    # print(isinstance(new_user, Collection))
    new_user.save()

    # users = Users.all()
    # users.age = 20

    # pprint(users)

    # pprint(users.name)s
    # pprint(users.age)


if __name__ == '__main__':
    main()