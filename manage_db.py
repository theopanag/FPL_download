from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, Float, MetaData, ForeignKey, join
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.schema import DDLElement
from sqlalchemy.sql import table, select
from sqlalchemy.ext import compiler

from models import (LeagueParticipants,
                    PLTeamsLookup,
                    PLPlayersLookup,
                    PLPlayersHistory,
                    UserAutomaticSubstitutions,
                    UserTransferHistory,
                    UserPickHistory,
                    UserGameweekHistory,
                    FPLFixtureList,
                    UserPickHistory_V,
                    UserChipHistory_V,
                    Base)

import logging


class Database():
    """ A class with the required SQL statements for our schema """

    def __init__(self, engine_loc):
        self.__engine = create_engine(engine_loc)
        self.Base = Base

    @property
    def engine(self):
        return self.__engine

    def create_objects_in_database_from_scratch(self):
        self.Base.metadata.drop_all(self.engine)
        # self.Base.metadata.clear()
        self.Base.metadata.create_all(self.engine)


    ### League admin details
    """ fpl_data.league_admin_details returns a dictionary.
    
    {'id': 151956, 'name': 'Amateurs', 'created': '2019-07-07T12:21:13.767946Z', 'closed': False, 'rank': None,
     'max_entries': None, 'league_type': 'x', 'scoring': 'c', 'admin_entry': 393978, 'start_event': 1,
     'code_privacy': 'p'}
     
    We can use **name**, year from **created** to name the corresponding db file, as well as other info to keep in our
    db 
    """