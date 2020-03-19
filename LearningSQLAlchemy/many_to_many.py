from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///data.db", echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Association(Base):
    __tablename__ = 'association'
    left_id = Column('left_id', Integer, ForeignKey("left.id"), primary_key=True)
    right_id = Column('right_id', Integer, ForeignKey("right.id"), primary_key=True)
    extra_data = Column(String)
    child = relationship("Child", back_populates="parents")
    parent = relationship("Parent", back_populates="children"
)


class Parent(Base):
    __tablename__ = "left"
    id = Column(Integer, primary_key=True)
    children = relationship("Association", back_populates="parent")

class Child(Base):
    __tablename__ = "right"
    id = Column(Integer, primary_key=True)
    parents = relationship("Association", back_populates="child")


Base.metadata.create_all(engine)

#Testing
p = Parent()
a = Association(extra_data="Some Data")
a.child = Child()
p.children.append(a)

session.add(p)
session.add(a)
session.commit()

for assoc in p.children:
    print(assoc.extra_data)

