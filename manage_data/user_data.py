
class UserData():
    """ Manage fpl league user data """

    def __init__(self, ids):
        self.user_ids = ids

    @property
    def user_ids(self):
        return self.__user_ids

    @user_ids.setter
    def user_ids_in_league(self, user_ids):
        self.__user_ids = user_ids

    def read_users_info(self, users_dict):
        # Get the information for all users
        assert users_dict, '"user" variable is NULL'
        self._user_dict = users_dict

    @property
    def users_gameweek_history(self):
        gameweek_history_df = pd.concat(
            (pd.io.json.json_normalize(data=self._user_dict['gameweek_history'][user_id]).assign(user_id=user_id)
             for user_id in self.user_ids
             ),
            ignore_index=True,
            sort=False
        )
        return gameweek_history_df

    @property
    def users_chip_history(self):
        chip_history_df = pd.concat(
            (pd.io.json.json_normalize(data=self._user_dict['chip_history'][user_id]).assign(user_id=user_id)
             for user_id in self.user_ids
             ),
            ignore_index=True,
            sort=False
        )
        return chip_history_df

    @property
    def users_picks_history(self):
        picks_history_df = pd.concat(
            (pd.io.json.json_normalize(data=self._user_dict['picks_history'][user_id].get(week)).assign(user_id=user_id)
             for user_id in self.user_ids for week in range(1, self.current_gameweek)
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
             for user_id in self.user_ids
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
             for user_id in self.user_ids
             if self._user_dict['transfers_history'][user_id]
             ),
            ignore_index=True,
            sort=False
        )
        return transfers_history_df