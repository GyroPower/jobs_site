from typing import Any
from sqlalchemy.ext.declarative import as_declarative,declared_attr

@as_declarative()
class Base:
    id:Any 
    __name__: str 
    
    #to generate tablename from class name
    @declared_attr
    def __tablename__(csl) -> str:
        return csl.__name__.lower()
    