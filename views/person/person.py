from typing import Optional
from flask import Blueprint, render_template, request
from models import Person, lru_decorator
import time


persons = Blueprint('persons',__name__)


@lru_decorator
def get_person(name:str) -> Optional[Person]:
    time.sleep(5)
    person = Person.query.where(Person.name == name).first()
    return person


@persons.route("/<name>")
def person_page(name):
    person = get_person(name)
    return render_template("persons/person.html", person=person)



@persons.route("/list")
def list_persons():
    page = request.args.get('page', 1 , type=int)

    list_of_persons = Person.query.paginate(page,20,False)

    return render_template("persons/persons.html",page=page, pagination = list_of_persons)