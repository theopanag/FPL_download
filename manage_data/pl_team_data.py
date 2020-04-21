

class TeamData():
    """ Manage premier league team data """

    def __init__(self):
        pass

    def read_pl_teams_info(self, teams):
        # Get the information of all players
        assert teams, '"teams" variable is NULL'
        self._teams = teams

    @property
    def pl_teams_lookup_info_df(self):
        return pd.io.json.json_normalize(
            data=self._teams
        )