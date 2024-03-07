import logging
import random
from pymongo import MongoClient
from local_settings import DATABASE
from constants import *



logging.basicConfig(filename='loggings.log')


def generate_random_datas(count: int, last_id: int) -> list:
    '''This function creates amd returns a random list of dictionaries'''

    random_data = [
        {
            'ID': last_id + i,
            'FirstName': random.choice(FIRST_NAMES),
            'LastName': random.choice(LAST_NAMES),
            'Number': random.randint(1_000, 100_000_000_000),
            'Provice': random.choice(PROVICES),
            'City': random.choice(CITIES),
            'Street': i,
            'HouseName': random.randint(1, 100),
        }
        for i in range(count)
    ]
    return random_data


def new_id(collection) -> int:
    '''Calculates last id + 1 in a collection'''
    collection_length = collection.count_documents(filter={})
    while True:
        if not collection.find_one(filter={'ID': collection_length}):
            break
        collection_length += 1
    return collection_length


def show_all_datas(collection) -> None:
    '''Show all datas in database'''
    all_datas = collection.find()
    for data in all_datas:
        print(
            f'ID: {data['ID']}\n'
            f'First Name: {data['FirstName']}\n'
            f'Last Name: {data['LastName']}\n'
            f'Number: {data['Number']}\n',
            f'Provice: {data['Provice']}\n',
            f'City: {data['City']}\n',
            f'Street: {data['Street']}\n',
            f'HouseName: {data['HouseName']}'
        )
        print('-'*20)


def add_random_data(collection, count: int) -> None:
    '''Add random datas to database'''

    datas = generate_random_datas(count=count, last_id=new_id(collection=collection))
    collection.insert_many(datas)


def add_data(collection) -> None:
    '''Add new data to the collection'''

    while True:
        first_name = input('Please enter your name: ').capitalize()
        if not first_name.isnumeric() and len(first_name) > 3:
            break
        print('This name is not allowed! Please try again.')
    while True:
        last_name = input('Please enter your last name: ').capitalize()
        if not last_name.isnumeric() and len(last_name) > 3:
            break
        print('This last name is not allowed! Please try again.')
    while True:
        number = input('Please enter your number: ')
        if number.isnumeric() and len(number) > 3:
            break
        print('This number is not allowed! Please try again.')
    while True:
        provice = input('Please enter your provice: ').capitalize()
        if not provice.isnumeric() and len(provice) > 3:
            break
        print('This provice name is not allowed! Please try again.').capitalize()
    while True:
        city = input('Please enter your city: ').capitalize()
        if not city.isnumeric() and len(city) > 3:
            break
        print('This city name is not allowed! Please try again.')
    street = input('Please enter your street: ').capitalize()
    house_name = input('Please enter your house name: ').capitalize()

    new_data = {
        'ID': new_id(collection=collection),
        'FirstName': first_name,
        'LastName': last_name,
        'Number': number,
        'Provice': provice,
        'City': city,
        'Street': street,
        'HouseName': house_name,
    }
    collection.insert_one(new_data)


def delete_data(collection, data_id: int) -> None:
    '''Delete a data with this id from a collection'''
    collection.delete_one(filter={'ID': data_id})


def update_data(collection, data_id: int) -> None:
    '''Update data info in a collection'''
    filter_id = {'ID': data_id}
    while True:
        print('1. First name.\n'
              '2. Last name.\n'
              '3. Number.\n'
              '4. Address.\n'
              '0. Exit changing.'
        )
        order = int(input('What do you want to change? '))
        match order:
            case 0:
                break
            case 1:
                while True:
                    new_name = input('Please enter new name: ').capitalize()
                    if not new_name.isnumeric() and len(new_name) > 3:
                        break
                    print('This name is not allowed! Please try again.')
                new_name = {'$set': {'FirstName': new_name}}
                collection.update_one(filter_id, new_name)
            case 2:
                while True:
                    new_last_name = input('Please enter new last name: ').capitalize()
                    if not new_last_name.isnumeric() and len(new_last_name) > 3:
                        break
                    print('This last name is not allowed! Please try again.')
                new_last_name = {'$set': {'lastName': new_last_name}}
                collection.update_one(filter_id, new_last_name)
            case 3:
                while True:
                    new_number = input('Please enter new number: ')
                    if new_number.isnumeric() and len(new_number) > 3:
                        break
                    print('This number is not allowed! Please try again.')
                new_number = {'$set': {'Number': new_number}}
                collection.update_one(filter_id, new_number)
            case 4:
                while True:
                    provice = input('Please enter your provice: ').capitalize()
                    if not provice.isnumeric() and len(provice) > 3:
                        break
                    print('This provice name is not allowed! Please try again.').capitalize()
                while True:
                    city = input('Please enter your city: ').capitalize()
                    if not city.isnumeric() and len(city) > 3:
                        break
                    print('This city name is not allowed! Please try again.')
                street = input('Please enter your street: ').capitalize()
                house_name = input('Please enter your house name: ').capitalize()

                provice = {'$set': {'Provice': provice}}
                collection.update_one(filter_id, provice)

                city = {'$set': {'City': city}}
                collection.update_one(filter_id, city)

                street = {'$set': {'Street': street}}
                collection.update_one(filter_id, street)

                house_name = {'$set': {'HouseName': house_name}}
                collection.update_one(filter_id, house_name)


if __name__ == '__main__':
    client = MongoClient(host=DATABASE['host'], port=DATABASE['port'])
    # Create database
    phonebook_database = client[DATABASE['name']]

    collections = phonebook_database.list_collection_names()

    if 'phonebook_data' in collections:
        data_collection = phonebook_database.get_collection('phonebook_data')
    else:
        data_collection = phonebook_database['phonebook_data']

    try:
        while True:
            print(MENU)
            order = int(input('Please enter you order: '))

            match order:
                case 0:
                    break
                case 1:
                    show_all_datas(collection=data_collection)
                case 2:
                    count = int(input('How many datas do you want to add? '))
                    add_random_data(collection=data_collection, count=count)
                case 3:
                    # Add new data
                    add_data(collection=data_collection)
                case 4:
                    # Delete data
                    while True:
                        user_id = int(input('Please enter a data id: '))
                        if data_collection.find_one(filter={'ID': user_id}):
                            break
                        print('This id is not existing! Please try again.')
                    delete_data(collection=data_collection, data_id=user_id)
                case 5:
                    # Update data
                    while True:
                        user_id = int(input('Please enter a data id: '))
                        if data_collection.find_one(filter={'ID': user_id}):
                            break
                        print('This id is not existing! Please try again.')
                    update_data(collection=data_collection, data_id=user_id)

    except ValueError as error:
        print('ValueError:', error)
        logging.error(error)
