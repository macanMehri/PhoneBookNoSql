import random
from pymongo import MongoClient
from local_settings import DATABASE
from constant_lists import *


def generate_random_datas() -> list:
    '''This function creates amd returns a random list of dictionaries'''
    random_data = [
        {
            'FirstName': random.choice(FIRST_NAMES),
            'LastName': random.choice(LAST_NAMES),
            'Number': random.randint(1_000, 100_000_000_000),
            'Provice': random.choice(PROVICES),
            'City': random.choice(CITIES),
            'Street': i,
            'HouseName': random.randint(1, 100),
        }
        for i in range(10)
    ]
    return random_data


def show_all_datas(collection: list) -> None:
    '''Show all datas in database'''
    all_datas = collection.find()
    for i, data in enumerate(all_datas):
        print(
            f'ID: {i}\n'
            f'First Name: {data['FirstName']}\n'
            f'Last Name: {data['LastName']}\n'
            f'Number: {data['Number']}\n',
            f'Provice: {data['Provice']}\n',
            f'City: {data['City']}\n',
            f'Street: {data['Street']}\n',
            f'HouseName: {data['HouseName']}'
        )
        print('-'*20)


def add_random_data(collection: list) -> None:
    '''Add random datas to database'''

    datas = generate_random_datas()
    collection.insert_many(datas)


if __name__ == '__main__':
    client = MongoClient(host=DATABASE['host'], port=DATABASE['port'])
    # Create database
    phonebook_database = client[DATABASE['name']]

    collections = phonebook_database.list_collection_names()

    if 'user' in collections:
        data_collection = phonebook_database.get_collection('user')
    else:
        data_collection = phonebook_database['user']


    order = int(input('Please enter you order: '))

    match order:
        case 0:
            pass
        case 1:
            show_all_datas(collection=data_collection)
        case 2:
            add_random_data(collection=data_collection)

