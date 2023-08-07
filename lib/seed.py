#!/usr/bin/env python3

from faker import Faker
import random

from random import choice as rc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Audition, Role

engine = create_engine('sqlite:///auditions.db')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

def delete_records():
    session.query(Audition).delete()
    session.query(Role).delete()
    session.commit()

def create_auditions():
    auditions=[]
    for i in range (20):
        audition = Audition(
           actor=fake.name(), 
           location=fake.city(),
           phone=fake.phone_number(),
           hired=fake.boolean(chance_of_getting_true=50),
        )
        session.add(audition)   
        session.commit  
        auditions.append(audition) 
    
def create_roles():
    roles = []
    for i in range (5):
        role = Role(
            character_name = fake.name()
        )
        session.add(role)
        session.commit
        roles.append(role)
    
if __name__ == '__main__':
    delete_records()
    create_auditions()
    create_roles()
    