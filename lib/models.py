from sqlalchemy import Boolean, ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///auditions.db')
Session = sessionmaker(bind=engine)
session = Session()

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer(), primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean())
    role_id = Column(Integer(), ForeignKey('roles.id'))

    def call_back(self):
        self.hired = True
        session.commit()
        return self.hired    

    def __repr__(self):
        return f'Audition: {self.id}, ' + \
               f'Actor: {self.actor}, ' + \
               f'Location: {self.location},' + \
               f'Phone: {self.phone}, ' + \
               f'Hired: {self.hired}, ' + \
               f'Role: {self.role_id} '
    
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    character_name = Column(String())

    auditions = relationship('Audition', backref=backref('role') )
    
    def lead (self):
        for audition in self.auditions:
            if audition.hired == True:
                return audition
        return "no actor has been hired for this role."    
        
    def understudy(self):
        counter = 0
        for audition in self.auditions:
            if audition.hired == True:
                counter +=1
                if counter == 2:
                    return audition
        return "no actor has been hired for understudy for this role."        

    def __repr__(self):
        return f'Role: {self.character_name}'
    
