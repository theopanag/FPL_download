

class PlayerData():
    """ Manage data regarding football players in fpl """

    def __init__(self):
        pass

    def read_players_info(self, players):
        # Get the information of all players
        assert players, '"players" variable is NULL'
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