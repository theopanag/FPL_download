

class LeagueData():
    """ Manage data regarding fpl league information """
    def __init__(self):
        pass

    def read_league_info(self, league):
        # Get the league information from fpl
        assert league, '"league" variable is Null'
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