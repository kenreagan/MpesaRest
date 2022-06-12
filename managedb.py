import argparse
import os
import sys
from MpesaRest.models import Base
from sqlalchemy import create_engine
import unittest
from tests.tests import TestRestServices

parser = argparse.ArgumentParser()

parser.add_argument(
    '-c',
    '--create',
    'create',
    help='create database Models',
    type=bool,
)

parser.add_argument(
    '-d',
    '--destroy',
    'destroy',
    help='Destroy database Transaction Model',
    type=bool,
)

parser.add_argument(
    '-t',
    '--test',
    'test',
    help="test Application functionality"
)

engine = create_engine(
    'sqlite:///main.sqlite'
)

args = parser.parse_args(sys.argv[1:])


def initialize_db():
    print('initializing database Tables ...')
    Base.metadata.create_all(
        engine
    )
    print('Done')


def destroy_db():
    print('Destroying Database Table action undouble ...')
    Base.metadata.drop_all(
        engine
    )
    os.unlink('main.sqlite')
    print('Done')


def main():
    if args.create:
        initialize_db()

    if args.destroy:
        destroy_db()

    if args.tests:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(TestRestServices)
        results = unittest.TextTestRunner().run(tests)
        print(".......................................................................")
        print("correctness score = ", str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100))
