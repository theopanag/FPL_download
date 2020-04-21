import pandas as pd
import logging

class ManageFplData():
    """A class managing the data we keep from FPL"""

    def __init__(self):
        pass

    @property
    def current_gameweek(self):
        return self.__current_gameweek

    @current_gameweek.setter
    def current_gameweek(self, current_gameweek):
        # Assuming there are 38 gameweeks in a season of FPL
        if current_gameweek in range(39):
            self.__current_gameweek = current_gameweek
        else:
            self.__current_gameweek = 38

    ###### LEAGUE INFORMATION ########

    def read_league_info(self, league):
        # Get the league information from fpl
        assert league, '"league" variable is Null'
        logging.debug('Storing league information...')
        self._league_dict = league

    @property
    def league_admin_details(self):
        # Return the admin information of the current league
        return self._league_dict['league']

    @property
    def league_participants(self):
        # Return the participants details of the current league
        return self._league_dict['standings']['results']

    @property
    def league_participants_df(self):
        # Structure the participants information in a pandas DataFrame
        return pd.io.json.json_normalize(
            self.league_participants
        )

    ###### FOOTBALL PLAYERS INFORMATION ########

    def read_players_info(self, players):
        # Get the information of all players
        assert players, '"players" variable is NULL'
        logging.debug('Storing all players info...')
        self._players = players

    @property
    def players_info(self):
        return self._players

    @property
    def players_lookup_info_df(self):
        # Return info for players for current round
        return pd.io.json.json_normalize(
            data=self.players_info
        ).loc[:,
               ['id',
                'first_name',
                'second_name',
                'web_name',
                'now_cost',
                'cost_change_start',
                'dreamteam_count',
                'element_type',
                'selected_by_percent',
                'team'
                ]
               ]

    @property
    def players_history_df(self):
        # Return info of past match performance for all players
        return pd.io.json.json_normalize(
            data=self.players_info,
            record_path='history',
            meta=['first_name',
                  'second_name',
                  'web_name',
                  ]
        )

    ###### PREMIER LEAGUE TEAM INFORMATION ########

    def read_pl_teams_info(self, teams):
        # Get the information of all teams
        assert teams, '"teams" variable is NULL'
        logging.debug('Storing PL teams info...')
        self._teams = teams

    @property
    def pl_teams_lookup_info_df(self):
        return pd.io.json.json_normalize(
            data=self._teams
        )

    ######## FPL FIXTURES ########

    def read_fixtures_info(self, fixtures):
        # Get the information of all fixtures
        assert fixtures, '"fixtures" variable is NULL'
        logging.debug('Storing all fixtures...')
        self._fixtures = fixtures

    @property
    def fpl_fixture_list_df(self):
        return pd.io.json.json_normalize(
            data=self._fixtures,
            max_level=0
        ).drop(columns='stats')

    ####### LEAGUE USER INFORMATION ########

    @property
    def user_ids_in_league(self):
        return self.league_participants_df.entry.unique()

    def read_users_info(self, users_dict):
        # Get the information for all users
        assert users_dict, '"user" variable is NULL'
        logging.debug('Storing users info...')
        self._user_dict = users_dict

    @property
    def users_gameweek_history(self):
        gameweek_history_df = pd.concat(
            (pd.io.json.json_normalize(data=self._user_dict['gameweek_history'][user_id]).assign(user_id=user_id)
             for user_id in self.user_ids_in_league
             ),
            ignore_index=True,
            sort=False
        )
        return gameweek_history_df

    @property
    def users_chip_history(self):
        chip_history_df = pd.concat(
            (pd.io.json.json_normalize(data=self._user_dict['chip_history'][user_id]).assign(user_id=user_id)
             for user_id in self.user_ids_in_league
             ),
            ignore_index=True,
            sort=False
        )
        return chip_history_df

    @property
    def users_picks_history(self):
        picks_history_df = pd.concat(
            (pd.io.json.json_normalize(data=self._user_dict['picks_history'][user_id].get(week)).assign(user_id=user_id,
                                                                                                        week=week)
             for user_id in self.user_ids_in_league for week in range(1, self.current_gameweek)
             if self._user_dict['picks_history'][user_id].get(week)
             ),
            ignore_index=True,
            sort=False
        )
        return picks_history_df

    @property
    def users_automatic_substitutions_history(self):
        subs_history_df = pd.concat(
            (pd.io.json.json_normalize(data=self._user_dict['substitutions_history'][user_id]).assign(user_id=user_id)
             for user_id in self.user_ids_in_league
             if self._user_dict['substitutions_history'][user_id]
             ),
            ignore_index=True,
            sort=False
        )
        return subs_history_df

    @property
    def users_transfers_history(self):
        transfers_history_df = pd.concat(
            (pd.io.json.json_normalize(data=self._user_dict['transfers_history'][user_id]) # .assign(user_id=user_id)
             for user_id in self.user_ids_in_league
             if self._user_dict['transfers_history'][user_id]
             ),
            ignore_index=True,
            sort=False
        )
        return transfers_history_df