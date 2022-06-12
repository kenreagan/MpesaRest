from MpesaRest.mpesarest import StartService as Mpesa
# import argparse
# import os
# import sys
# from MpesaRest.models import Base
# from sqlalchemy import create_engine
#
# parser = argparse.ArgumentParser()
#
# parser.add_argument(
#     '--create',
#     help='create database Models',
#     type=bool,
# )
#
# parser.add_argument(
#     '--destroy',
#     help='create database Models',
#     type=bool,
# )
#
# engine = create_engine(
#     'sqlite:///main.sqlite'
# )
#
# args = parser.parse_args(sys.argv[1:])
#
# def initialize_db():
#     print('initializing database Tables ...')
#     Base.metadata.create_all(
#         engine
#     )
#     print('Done')
#
# def destroy_db():
#     print('Destroying Database Table action undouble ...')
#     Base.metadata.drop_all(
#         engine
#     )
#     os.unlink('main.sqlite')
#     print('Done')
#
#
# if args.create:
#     initialize_db()
#
# if args.destroy:
#     destroy_db()
