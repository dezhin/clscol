# -*- coding: utf-8 -*-
import sys
import os
from argparse import ArgumentParser
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import clscol
from clscol.base import Classifier


def get_engine_and_session(db_url):
    engine = create_engine(db_url)
    session = Session(bind=engine)
    return (engine, session)


def get_classifier(name):
    for sc in Classifier.__subclasses__():
        if sc.name == name:
            return sc


def classifiers(subparsers):

    def execute(args):
        for sc in Classifier.__subclasses__():
            print '%-8s %-8s %s' % (sc.name, sc.abbr, sc.desc)

    parser = subparsers.add_parser('classifiers',
        help=u"Перечислить доступные классификаторы")
    parser.set_defaults(command=execute)


def import_data(subparsers):

    def execute(args):
        engine, session = get_engine_and_session(args.db)
        classifier = get_classifier(args.classifier)
        metadata, tables = classifier.metadata(version_key=args.vk)
        metadata.create_all(engine)

        classifier.import_data(args.source, session, metadata, tables)
        session.commit()

    parser = subparsers.add_parser('import',
        help=u"Импортировать классификатор в БД")
    parser.add_argument('--db', type=str,
        default=os.environ.get('CLSCOL_DB', None),
        help=u"SQLAlchemy строка подключения к БД")
    parser.add_argument('--vk', type=str,
        default=None,
        help=u"Ключ, используемый в именах таблиц")
    parser.add_argument('classifier', type=str)
    parser.add_argument('source', type=str)
    parser.set_defaults(command=execute)


def main(argv=sys.argv):
    parser = ArgumentParser()

    subparsers = parser.add_subparsers()
    import_data(subparsers)
    classifiers(subparsers)

    args = parser.parse_args(argv[1:])
    args.command(args)
