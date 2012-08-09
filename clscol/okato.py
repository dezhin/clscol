# -*- coding: utf-8 -*-
from collections import namedtuple
import yaml
from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

from clscol.base import Classifier

OkatoTables = namedtuple('OkatoTables', ['okato', ])


class OkatoClassifier(Classifier):
    name = 'okato'
    abbr = u"ОКАТО"
    desc = u"Общероссийский классификатор объектов административно-территориального деления"

    @staticmethod
    def metadata(version_key=None):
        if not version_key or version_key == '':
            version_key = ''
        else:
            version_key = '_' + version_key

        Base = declarative_base()

        class Okato(Base):
            __tablename__ = 'okato%s' % version_key

            id = Column(Unicode(11), primary_key=True)
            name = Column(Unicode(200), nullable=False)

        return (Base.metadata, OkatoTables(okato=Okato))

    @staticmethod
    def import_data(source, dbsession, metadata, tables):
        with open(source, 'r') as fp:
            header = None
            for doc in yaml.load_all(fp):
                if not header:
                    header = doc
                else:
                    for code, name in doc:
                        obj = tables.okato(
                            id=unicode(code),
                            name=unicode(name)
                        )
                        dbsession.add(obj)

                    dbsession.flush()
