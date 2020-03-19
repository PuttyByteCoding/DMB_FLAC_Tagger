import sqlalchemy
from sqlalchemy import create_engine
engine = create_engine("sqlite:///:memory:", echo=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    # address = relationship("Address", order_by=Address.id, back_populates="user")

    def __repr__(self):
        return f"<User(name={self.name}, fullname={self.fullname}, nickname={self.nickname}>"

#Create a schema
Base.metadata.create_all(engine)


ed_user = User(name="Ed", fullname="Ed Jones", nickname="edsnickname")

print(ed_user)

#Create a Session.  Session is a class that serves as a factory for Session Objects.
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

session.add(ed_user)

# Query the database
our_user = session.query(User).filter_by(name='Ed').first()
print(our_user)

#Add more entries
session.add_all(
    [
        User(name='wendy', fullname='Wendy Williams', nickname='windy'),
        User(name='mary', fullname='Mary Contrary', nickname='mary'),
        User(name='fred', fullname='Fred Flintstone', nickname='freddy')
    ])
ed_user.nickname = 'eddie'
session.commit() #flushes changes to database


# Building relationships
from sqlalchemy import ForeignKey


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="Addresses")

    def __repr__(self):
        return f"<Address(email_address={self.email_address})>"

#Note: This was added here because both User and Address classes needed to be defined first.
User.address = relationship("Address", order_by=Address.id, back_populates="user")

