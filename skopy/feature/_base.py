import sqlalchemy.ext.declarative
import sqlalchemy_utils


@sqlalchemy.ext.declarative.as_declarative()
class Base:
    id = sqlalchemy.Column(sqlalchemy_utils.UUIDType(binary=False), primary_key=True)
