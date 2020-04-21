

class FixtureData():
    """ Manage fpl fixtures data """

    def __init__(self):
        pass

    def read_fixtures_info(self, fixtures):
        # Get the information of all fixtures
        assert fixtures, '"fixtures" variable is NULL'
        self._fixtures = fixtures

    @property
    def fpl_fixture_list_df(self):
        return pd.io.json.json_normalize(
            data=self._fixtures,
            max_level=0
        ).drop(columns='stats')