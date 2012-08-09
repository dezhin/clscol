# -*- coding: utf-8 -*-
from collections import namedtuple
import yaml

from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.ext.declarative import declarative_base

from clscol.base import Classifier

OktmoTables = namedtuple('OktmoTables', ['oktmo', 'oktmo_settlement'])


class OktmoClassifier(Classifier):
    name = 'oktmo'
    abbr = u"ОКТМО"
    desc = u"Общероссийский классификатор территорий муниципальных образований"

    @staticmethod
    def metadata(version_key=None):
        if not version_key or version_key == '':
            version_key = ''
        else:
            version_key = '_' + version_key

        Base = declarative_base()

        class Oktmo(Base):
            __tablename__ = 'oktmo%s' % version_key

            id = Column(Unicode(8), primary_key=True)
            name = Column(Unicode(200), nullable=False)

        class OktmoSettlement(Base):
            __tablename__ = 'oktmo%s_settlement' % version_key

            oktmo_id = Column(Unicode(8), primary_key=True)
            idx = Column(Integer, primary_key=True)
            okato_id = Column(Unicode(11))
            name = Column(Unicode(200))

        return (
            Base.metadata,
            OktmoTables(oktmo=Oktmo, oktmo_settlement=OktmoSettlement)
        )

    @staticmethod
    def import_data(source, dbsession, metadata, tables):
        with open(source, 'r') as fp:
            header = None
            for doc in yaml.load_all(fp):
                if not header:
                    header = doc
                else:
                    code = unicode(doc['code'])
                    name = unicode(doc['name'])
                    obj = tables.oktmo(id=code, name=name)
                    dbsession.add(obj)

                    if 'settlements' in doc:
                        settlements = doc['settlements']
                        idx = 0
                        for s in settlements:
                            obj_s = tables.oktmo_settlement(
                                oktmo_id=code,
                                idx=idx
                            )

                            obj_s.okato_id = unicode(s[0])
                            if len(s) == 2:
                                obj_s.name = unicode(s[1])
                            idx += 1
                            dbsession.add(obj_s)

                    dbsession.flush()

        dbsession.flush()
