from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# installation: pip install sqlalchemy-utils
from sqlalchemy_utils import create_view
from sqlalchemy import select, func, and_

Base = declarative_base()


############# TABLES ################

class LeagueParticipants(Base):
    '''
    Database model for league participants info

    ### League partitipants df
    """
                 id  event_total                    player_name  rank  last_rank  rank_sort  total    entry            entry_name
    0  10337068           64                     Aris Fragk     1          1          1   1213   874055          to panw rafi
    1   3372885           54                Karou Apostolos     2          2          2   1192   301326                K.F.C.
    2  14861495           59               Dimitris Karydis     3          3          3   1163  2638402  Donttakemytrophyaway
    3  30082036           57                   Chris Kavvir     4          4          4   1143  4894775      Deportivo Paltón
    4  17602878           58  Nektarios Dimitrios Foufoulas     5          5          5   1137  3088686             Foufulham

    """
    '''

    __tablename__ = "league_participants"

    id = Column("id", Integer, primary_key=True)
    event_total = Column('event_total', Integer)
    player_name = Column('player_name', String)
    rank = Column('rank', Integer)
    last_rank = Column('last_rank', Integer)
    rank_sort = Column('rank_sort', Integer)
    total = Column('total', Integer)
    entry = Column('entry', Integer)
    entry_name = Column('entry_name', String)
    subs = relationship("UserAutomaticSubstitutions")
    transfers = relationship("UserTransferHistory")
    picks = relationship("UserPickHistory")
    chips = relationship("UserChipHistory")
    history = relationship("UserGameweekHistory")

    def __repr__(self):
        return "<LeagueParticipant (player={player}, team={entry})>".format(
            player=self.player_name,
            entry=self.entry_name
        )


class PLTeamsLookup(Base):
    '''
    Database model for PL teams lookup table

    ### PL teams lookup info df
    """
    {'code': {0: 3, 1: 7, 2: 91, 3: 36, 4: 90},
     'draw': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'form': {0: None, 1: None, 2: None, 3: None, 4: None},
     'id': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5},
     'loss': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'name': {0: 'Arsenal',
              1: 'Aston Villa',
              2: 'Bournemouth',
              3: 'Brighton',
              4: 'Burnley'},
     'played': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'points': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'position': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'short_name': {0: 'ARS', 1: 'AVL', 2: 'BOU', 3: 'BHA', 4: 'BUR'},
     'strength': {0: 4, 1: 2, 2: 3, 3: 3, 4: 3},
     'strength_attack_away': {0: 1190, 1: 1060, 2: 1070, 3: 1160, 4: 1130},
     'strength_attack_home': {0: 1150, 1: 1030, 2: 1030, 3: 1040, 4: 1060},
     'strength_defence_away': {0: 1330, 1: 1050, 2: 1180, 3: 1130, 4: 1050},
     'strength_defence_home': {0: 1280, 1: 1030, 2: 1110, 3: 1030, 4: 1050},
     'strength_overall_away': {0: 1270, 1: 1080, 2: 1120, 3: 1120, 4: 1110},
     'strength_overall_home': {0: 1230, 1: 1040, 2: 1090, 3: 1050, 4: 1050},
     'team_division': {0: None, 1: None, 2: None, 3: None, 4: None},
     'unavailable': {0: False, 1: False, 2: False, 3: False, 4: False},
     'win': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}}

    """
    '''

    __tablename__ = "pl_teams_lookup"

    id = Column('id', Integer, primary_key=True)
    draw = Column('draw', Integer)
    form = Column('form', String)
    code = Column('code', Integer)
    loss = Column('loss', Integer)
    name = Column('name', String)
    played = Column('played', Integer)
    points = Column('points', Integer)
    position = Column('position', Integer)
    short_name = Column('short_name', String)
    strength = Column('strength', Integer)
    strength_attack_away = Column('strength_attack_away', Integer)
    strength_attack_home = Column('strength_attack_home', Integer)
    strength_defence_away = Column('strength_defence_away', Integer)
    strength_defence_home = Column('strength_defence_home', Integer)
    strength_overall_away = Column('strength_overall_away', Integer)
    strength_overall_home = Column('strength_overall_home', Integer)
    team_division = Column('team_division', String)
    unavailable = Column('unavailable', Boolean)
    win = Column('win', Integer)
    pulse_id = Column('pulse_id', Integer)
    player = relationship("PLPlayersLookup")
    team = relationship("FPLFixtureList")

    def __repr__(self):
        return "<PLTeam ({name})>".format(name=self.name)


class PLPlayersLookup(Base):
    '''
    Database model for PL players lookup table

    ### Players lookup info df
    """
    {'cost_change_start': {0: -3, 1: -1, 2: -3, 3: -4, 4: -1},
     'dreamteam_count': {0: 0, 1: 0, 2: 0, 3: 1, 4: 1},
     'element_type': {0: 2, 1: 2, 2: 2, 3: 2, 4: 2},
     'first_name': {0: 'Shkodran',
                    1: 'Héctor',
                    2: 'Sead',
                    3: 'Ainsley',
                    4: 'Sokratis'},
     'id': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5},
     'now_cost': {0: 52, 1: 54, 2: 52, 3: 46, 4: 49},
     'second_name': {0: 'Mustafi',
                     1: 'Bellerín',
                     2: 'Kolasinac',
                     3: 'Maitland-Niles',
                     4: 'Papastathopoulos'},
     'selected_by_percent': {0: '0.3', 1: '0.2', 2: '0.5', 3: '2.6', 4: '1.4'},
     'team': {0: 1, 1: 1, 2: 1, 3: 1, 4: 1},
     'web_name': {0: 'Mustafi',
                  1: 'Bellerín',
                  2: 'Kolasinac',
                  3: 'Maitland-Niles',
                  4: 'Sokratis'}}

    """
    '''

    __tablename__ = "pl_players_lookup"

    id = Column('id', Integer, primary_key=True)
    cost_change_start = Column('cost_change_start', Integer)
    dreamteam_count = Column('dreamteam_count', Integer)
    element_type = Column('element_type', Integer)
    first_name = Column('first_name', String)
    second_name = Column('second_name', String)
    now_cost = Column('now_cost', Integer)
    selected_by_percent = Column('selected_by_percent', Float)
    team = Column('team', Integer, ForeignKey("pl_teams_lookup.id"))
    web_name = Column('web_name', String)

    def __repr__(self):
        return "<PLPlayer ({first} {second})>".format(
            first=self.first_name,
            second=self.second_name
        )


class PLPlayersHistory(Base):
    '''
    Database model for PL players history table

    ### Players history df
    """
    'assists': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'bonus': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'bps': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'clean_sheets': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'creativity': {0: '0.0', 1: '0.0', 2: '0.0', 3: '0.0', 4: '0.0'},
     'element': {0: 1, 1: 1, 2: 1, 3: 1, 4: 1},
     'first_name': {0: 'Shkodran',
                    1: 'Shkodran',
                    2: 'Shkodran',
                    3: 'Shkodran',
                    4: 'Shkodran'},
     'fixture': {0: 10, 1: 11, 2: 24, 3: 31, 4: 49},
     'goals_conceded': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'goals_scored': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'ict_index': {0: '0.0', 1: '0.0', 2: '0.0', 3: '0.0', 4: '0.0'},
     'influence': {0: '0.0', 1: '0.0', 2: '0.0', 3: '0.0', 4: '0.0'},
     'kickoff_time': {0: '2019-08-11T13:00:00Z',
                      1: '2019-08-17T11:30:00Z',
                      2: '2019-08-24T16:30:00Z',
                      3: '2019-09-01T15:30:00Z',
                      4: '2019-09-15T15:30:00Z'},
     'minutes': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'opponent_team': {0: 13, 1: 5, 2: 10, 3: 17, 4: 18},
     'own_goals': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'penalties_missed': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'penalties_saved': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'red_cards': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'round': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5},
     'saves': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'second_name': {0: 'Mustafi',
                     1: 'Mustafi',
                     2: 'Mustafi',
                     3: 'Mustafi',
                     4: 'Mustafi'},
     'selected': {0: 33117, 1: 36709, 2: 30975, 3: 28096, 4: 26902},
     'team_a_score': {0: 1, 1: 1, 2: 1, 3: 2, 4: 2},
     'team_h_score': {0: 0, 1: 2, 2: 3, 3: 2, 4: 2},
     'threat': {0: '0.0', 1: '0.0', 2: '0.0', 3: '0.0', 4: '0.0'},
     'total_points': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
     'transfers_balance': {0: 0, 1: -5280, 2: -6882, 3: -3872, 4: -2073},
     'transfers_in': {0: 0, 1: 2868, 2: 534, 3: 346, 4: 581},
     'transfers_out': {0: 0, 1: 8148, 2: 7416, 3: 4218, 4: 2654},
     'value': {0: 55, 1: 55, 2: 54, 3: 54, 4: 53},
     'was_home': {0: False, 1: True, 2: False, 3: True, 4: False},
     'web_name': {0: 'Mustafi',
                  1: 'Mustafi',
                  2: 'Mustafi',
                  3: 'Mustafi',
                  4: 'Mustafi'},
     'yellow_cards': {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}}
    """
    '''

    __tablename__ = "pl_players_history"

    element = Column('element', Integer, primary_key=True)
    fixture = Column('fixture', Integer, primary_key=True)
    opponent_team = Column('opponent_team', Integer)
    total_points = Column('total_points', Integer)
    was_home = Column('was_home', Boolean)
    kickoff_time = Column('kickoff_time', String)
    team_h_score = Column('team_h_score', Integer)
    team_a_score = Column('team_a_score', Integer)
    round = Column('round', Integer)
    minutes = Column('minutes', Integer)
    goals_scored = Column('goals_scored', Integer)
    assists = Column('assists', Integer)
    clean_sheets = Column('clean_sheets', Integer)
    goals_conceded = Column('goals_conceded', Integer)
    own_goals = Column('own_goals', Integer)
    penalties_saved = Column('penalties_saved', Integer)
    penalties_missed = Column('penalties_missed', Integer)
    yellow_cards = Column('yellow_cards', Integer)
    red_cards = Column('red_cards', Integer)
    saves = Column('saves', Integer)
    bonus = Column('bonus', Integer)
    bps = Column('bps', Integer)
    influence = Column('influence', Integer)
    creativity = Column('creativity', Integer)
    threat = Column('threat', Integer)
    ict_index = Column('ict_index', Integer)
    value = Column('value', Integer)
    transfers_balance = Column('transfers_balance', Integer)
    selected = Column('selected', Integer)
    transfers_in = Column('transfers_in', Integer)
    transfers_out = Column('transfers_out', Integer)
    first_name = Column('first_name', String)
    second_name = Column('second_name', String)
    web_name = Column('web_name', String)

    def __repr__(self):
        return "<PLPlayerHistory (name={name} fixture={fixture})>".format(
            name=self.name,
            fixture=self.fixture
        )


class UserAutomaticSubstitutions(Base):
    '''
    Database model for user automatic substitutions table

    ### Users automatic substitutions df
    """
        entry  element_in  element_out  event  user_id
    0  874055          38          457      2   874055
    1  874055         458          234      5   874055
    2  874055         458          214      6   874055
    3  874055         381          204     11   874055
    4  874055         381          204     12   874055
    """
    '''

    __tablename__ = "users_automatic_substitutions"

    entry = Column('entry', Integer, ForeignKey("league_participants.entry"), primary_key=True)
    element_in = Column('element_in', Integer, primary_key=True)
    element_out = Column('element_out', Integer, primary_key=True)
    event = Column('event', Integer, primary_key=True)
    user_id = Column('user_id', Integer)


class UserTransferHistory(Base):
    '''
    Database model for user transfer history table

    ### Users transfer history df
    """
           element_in  element_in_cost  element_out  element_out_cost   entry  event                         time
    0         182               74          181                70  874055     21  2019-12-29T18:27:23.351327Z
    1         233               91          502                58  874055     20  2019-12-28T08:51:10.836618Z
    2         493               44          182                71  874055     20  2019-12-28T08:51:10.832417Z
    3         502               58          233                91  874055     20  2019-12-28T08:50:03.642081Z
    4         181               70          493                44  874055     20  2019-12-28T08:50:03.639889Z
    """
    '''

    __tablename__ = "users_transfers_history"

    element_in = Column('element_in', Integer, primary_key=True)
    element_in_cost = Column('element_in_cost', Integer)
    element_out = Column('element_out', Integer, primary_key=True)
    element_out_cost = Column('element_out_cost', Integer)
    entry = Column('entry', Integer, ForeignKey("league_participants.entry"), primary_key=True)
    event = Column('event', Integer, primary_key=True)
    time = Column('time', String, primary_key=True)

    def __repr__(self):
        return "<UserTransfer (name={entry} gameweek={event})>".format(
            entry=self.entry,
            event=self.event
        )


class UserPickHistory(Base):
    '''
    Database model for user pick history table

    ### Users pick history df
    """
       element  position  multiplier  is_captain  is_vice_captain  user_id  week
    0       93         1           1       False            False   874055     1
    1       38         2           1       False            False   874055     1
    2      182         3           1       False            False   874055     1
    3      141         4           1       False            False   874055     1
    4      239         5           1       False            False   874055     1
    """
    '''

    __tablename__ = "users_pick_history"

    element = Column('element', Integer, primary_key=True)
    position = Column('position', Integer)
    multiplier = Column('multiplier', Integer)
    is_captain = Column('is_captain', Boolean)
    is_vice_captain = Column('is_vice_captain', Boolean)
    user_id = Column('user_id', Integer, ForeignKey("league_participants.entry"), primary_key=True)
    week = Column('week', Integer, primary_key=True)

    def __repr__(self):
        return "<UserPick (user={user} week={week} element={element})>".format(
            user=self.user_id,
            week=self.week,
            element=self.element
        )


class UserChipHistory(Base):
    '''
    Databse model for user chip history table

    ### Users chip history df
    """
               name                         time  event  user_id
    0  wildcard  2019-12-26T19:00:56.617241Z   20.0   874055
    1  wildcard  2019-09-22T19:49:06.557377Z    7.0   301326
    2  wildcard  2019-12-21T07:24:30.180544Z   18.0  3088686
    3  wildcard  2019-08-19T11:07:09.193852Z    3.0  2638402
    4  wildcard  2019-09-04T23:18:35.110390Z    5.0  4894775
    """
    '''

    __tablename__ = "users_chip_history"

    name = Column('name', String)
    time = Column('time', String)
    event = Column('event', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey("league_participants.entry"), primary_key=True)

    def __repr__(self):
        return "<UserChip (user={user} event={event})>".format(
            user=self.user_id,
            event=self.event
        )


class UserGameweekHistory(Base):
    '''
    Database model for users gameweek performance history table

    ### Users gameweek history df
    """
    {'bank': {0: 10, 1: 10, 2: 4, 3: 18, 4: 18},
     'event': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5},
     'event_transfers': {0: 0, 1: 0, 2: 3, 3: 1, 4: 0},
     'event_transfers_cost': {0: 0, 1: 0, 2: 4, 3: 0, 4: 0},
     'overall_rank': {0: 397369, 1: 47507, 2: 68141, 3: 66366, 4: 65457},
     'points': {0: 88, 1: 63, 2: 55, 3: 62, 4: 57},
     'points_on_bench': {0: 6, 1: 2, 2: 7, 3: 3, 4: 1},
     'rank': {0: 397365, 1: 186089, 2: 1465800, 3: 2225267, 4: 2245562},
     'rank_sort': {0: 410955, 1: 188650, 2: 1467759, 3: 2231284, 4: 2256695},
     'total_points': {0: 88, 1: 151, 2: 202, 3: 264, 4: 321},
     'user_id': {0: 874055, 1: 874055, 2: 874055, 3: 874055, 4: 874055},
     'value': {0: 1000, 1: 1002, 2: 1002, 3: 1006, 4: 1011}}
    """
    '''

    __tablename__ = "users_gameweek_history"

    event = Column('event', Integer, primary_key=True)
    points = Column('points', Integer)
    total_points = Column('total_points', Integer)
    rank = Column('rank', Integer)
    rank_sort = Column('rank_sort', Integer)
    overall_rank = Column('overall_rank', Integer)
    bank = Column('bank', Integer)
    value = Column('value', Integer)
    event_transfers = Column('event_transfers', Integer)
    event_transfers_cost = Column('event_transfers_cost', Integer)
    points_on_bench = Column('points_on_bench', Integer)
    user_id = Column('user_id', Integer, ForeignKey("league_participants.entry"), primary_key=True)

    def __repr__(self):
        return "<UserHistory (user={user} week={event})>".format(
            user=self.user_id,
            week=self.event
        )


class FPLFixtureList(Base):
    '''
    Database model for FPL fixture list

    ### FPL fixture list
    """
    {'code': {0: 1059702, 1: 1059709, 2: 1059703, 3: 1059704, 4: 1059705},
     'event': {0: 1, 1: 1, 2: 1, 3: 1, 4: 1},
     'finished': {0: True, 1: True, 2: True, 3: True, 4: True},
     'finished_provisional': {0: True, 1: True, 2: True, 3: True, 4: True},
     'id': {0: 1, 1: 8, 2: 2, 3: 3, 4: 4},
     'kickoff_time': {0: '2019-08-09T19:00:00Z',
                      1: '2019-08-10T11:30:00Z',
                      2: '2019-08-10T14:00:00Z',
                      3: '2019-08-10T14:00:00Z',
                      4: '2019-08-10T14:00:00Z'},
     'minutes': {0: 90, 1: 90, 2: 90, 3: 90, 4: 90},
     'provisional_start_time': {0: False, 1: False, 2: False, 3: False, 4: False},
     'started': {0: True, 1: True, 2: True, 3: True, 4: True},
     'team_a': {0: 14, 1: 11, 2: 15, 3: 16, 4: 8},
     'team_a_difficulty': {0: 5, 1: 2, 2: 3, 3: 3, 4: 2},
     'team_a_score': {0: 1.0, 1: 5.0, 2: 1.0, 3: 0.0, 4: 0.0},
     'team_h': {0: 10, 1: 19, 2: 3, 3: 5, 4: 7},
     'team_h_difficulty': {0: 2, 1: 4, 2: 3, 3: 2, 4: 2},
     'team_h_score': {0: 4.0, 1: 0.0, 2: 1.0, 3: 3.0, 4: 0.0}}
    """
    '''

    __tablename__ = "fpl_fixture_list"

    code = Column('code', Integer)
    event = Column('event', Integer)
    finished = Column('finished', Boolean)
    finished_provisional = Column('finished_provisional', Boolean)
    id = Column('id', Integer, primary_key=True)
    kickoff_time = Column('kickoff_time', String)
    minutes = Column('minutes', Integer)
    provisional_start_time = Column('provisional_start_time', Boolean)
    started = Column('started', Boolean)
    team_a = Column('team_a', Integer, ForeignKey("pl_teams_lookup.id"))
    team_a_score = Column('team_a_score', Integer)
    team_h = Column('team_h', Integer, ForeignKey("pl_teams_lookup.id"))
    team_h_score = Column('team_h_score', Integer)
    team_h_difficulty = Column('team_h_difficulty', Integer)
    team_a_difficulty = Column('team_a_difficulty', Integer)


################# VIEWS ###################


stmt_users_pick_history = select(
    [c.label(c.name) for c in UserPickHistory.__table__.c] +
    [c.label(c.name) for c in LeagueParticipants.__table__.c if c.name in ('player_name', 'entry_name')] +
    [c.label(c.name) for c in PLPlayersLookup.__table__.c if
     c.name in ('element_type', 'first_name', 'second_name', 'web_name')] +
    [PLTeamsLookup.__table__.c.name.label('team_name'),
     PLTeamsLookup.__table__.c.short_name.label('team_short_name')] +
    [c.label(c.name) for c in PLPlayersHistory.__table__.c if c.name not in ('element','first_name', 'second_name', 'web_name')]
). \
    select_from(
    UserPickHistory.__table__.join(
        LeagueParticipants,
        UserPickHistory.__table__.c.user_id == LeagueParticipants.__table__.c.entry
    ).join(
        PLPlayersLookup,
        UserPickHistory.__table__.c.element == PLPlayersLookup.__table__.c.id
    ).join(
        PLTeamsLookup,
        PLPlayersLookup.__table__.c.team == PLTeamsLookup.__table__.c.id
    ).join(
        PLPlayersHistory,
        and_(
            UserPickHistory.__table__.c.element == PLPlayersHistory.__table__.c.element,
            UserPickHistory.__table__.c.week == PLPlayersHistory.__table__.c.round
        )
    )
)

# attaches the view to the metadata using the select statement
view_users_pick_history = create_view('users_pick_history_V', stmt_users_pick_history, Base.metadata, cascade_on_drop=False)


# provides an ORM interface to the view
class UserPickHistory_V(Base):
    __table__ = view_users_pick_history


stmt_user_chip_history = select(
    [c.label(c.name) for c in UserChipHistory.__table__.c] +
    [c.label(c.name) for c in LeagueParticipants.__table__.c if c.name in ['player_name', 'entry_name']]
). \
    select_from(
    UserChipHistory.__table__.join(LeagueParticipants,
                                   UserChipHistory.__table__.c.user_id == LeagueParticipants.__table__.c.entry)

)

# attaches the view to the metadata using the select statement
view_users_chip_history = create_view('users_chip_history_V', stmt_user_chip_history, Base.metadata, cascade_on_drop=False)


# provides an ORM interface to the view
class UserChipHistory_V(Base):
    __table__ = view_users_chip_history
