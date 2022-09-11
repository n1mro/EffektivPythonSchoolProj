from typing import Callable
from flask_sqlalchemy import SQLAlchemy
import barnum
import random

db = SQLAlchemy()
NUMBER_OF_PERSONS = 500


class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    personal_id_number = db.Column(db.String(50), unique=False, nullable=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)
    profession = db.Column(db.String(50), unique=False, nullable=False)
    phone_number = db.Column(db.String(50), unique=False, nullable=False)


class LRUPersons():
    __LRU_list:list[Person] = []
    LRU_CACHE_SIZE = 50

    def __new__(cls):
        cls._fill_lru_list_with_persons()
        return cls

    @classmethod
    def fetch_person_in_lru(cls,name:str) -> Person | None:

        for index,person in enumerate(cls.__LRU_list):
            if person.name == name:
                cls.__LRU_list.pop(index)
                cls.__LRU_list.insert(0,person)
                return person

        return None

    @classmethod
    def add_person_to_lru(cls,person:Person) -> None:
        cls.__LRU_list.pop(-1)
        cls.__LRU_list.insert(0,person)

    @classmethod
    def _fill_lru_list_with_persons(cls) -> None:

        if cls.__LRU_list: return

        cls.__LRU_list = [p for p in Person.query.limit(cls.LRU_CACHE_SIZE)]


def lru_decorator(func: Callable):

    """Returns a Person if in LRU, otherwise calls the function"""
    
    def _wrapper(*args, **kwargs):
        if args and isinstance(args[0],str):
            person = LRUPersons().fetch_person_in_lru(args[0])

            if person: return person

            new_person = func(*args,**kwargs)
            if new_person:
                LRUPersons().add_person_to_lru(new_person)
                return new_person

            # Person does not exist in the database
            return None


        raise ValueError("Invalid function call, invalid argument!")
        

    return _wrapper


def generate_persons(n):
    count = 0
    while count < n:
        person = Person()
        person.name = " ".join(barnum.create_name())
        person.personal_id_number = barnum.create_birthday().isoformat() + "-" + str(random.randint(1001,9999))
        zip,person.city,person.country = barnum.create_city_state_zip()
        person.profession = barnum.create_job_title()
        person.phone_number = barnum.create_phone()
        yield person
        count +=1


def save_person_to_db(person:Person):
    db.session.add(person)
    db.session.commit()


def seed_data(db):
    number_of_persons_in_db = Person.query.count()
    number_of_persons_to_generate = NUMBER_OF_PERSONS-number_of_persons_in_db

    [save_person_to_db(person) for person in generate_persons(number_of_persons_to_generate)
    if number_of_persons_to_generate > 0]
