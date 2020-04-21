from fpl import FPL, utils
import aiohttp
import asyncio
import logging
import pprint
import pdb

import retrieve_fpl_data as ret_fpl
import manage_db

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename='testing_version.log',
                    filemode='w',
                    level=logging.DEBUG)

LEAGUE_ID = 151956
ALEFANTOS_ID = 393978
PLAYER_ID = 302  # Oliver Norwood
# Credentials need to be hardcoded here before running the script.
# TODO: Input credentials through argparse
CREDENTIALS = {'email': '<your_email@provider.com>', 'password': '<fpl password - does not have to be string>'}

DB_ENGINE_LOC = 'sqlite:///test.db'

# Initialize class regardning data management
fpl_data = ret_fpl.ManageFplData()


async def retrieve_data_from_fpl():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(**CREDENTIALS)

        ### Get the current gameweek
        logging.info('Getting current week')
        fpl_data.current_gameweek = await utils.get_current_gameweek(session)
        logging.info('Current week: {cw}'.format(cw=fpl_data.current_gameweek))

        logging.info('Get specific league')
        ### Get a specific league
        league = await fpl.get_classic_league(LEAGUE_ID, return_json=True)
        logging.info('League info downloaded')

        logging.info('Store specific league info in class')
        # Store data into class
        fpl_data.read_league_info(league)
        logging.info('League info stored')

        ### Get the info of all players
        # 'history_past' dictionary refers to past seasons performance for a player
        # 'history' holds a dictionary for each of the past weeks
        logging.info('Get info of all players')
        players = await fpl.get_players(include_summary=True,
                                        return_json=True)
        logging.info('Info of all players downloaded')

        logging.info('Store info of all players in class')
        # Store data into class
        fpl_data.read_players_info(players)
        logging.info('Info of all players stored')

        ### List of available premierl league teams in FPL. Class Team
        # We can use attributes from the teams to create a lookup table, i.e id, name, short_name
        logging.info('Get info of PL teams')
        teams = await fpl.get_teams(return_json=True)
        logging.info('Info of PL teams downloaded')

        logging.info('Store info of PL teams in class')
        # Store data into class
        fpl_data.read_pl_teams_info(teams)
        logging.info('Info of PL teams stored')

        ### Get a specific user
        user = await fpl.get_user(user_id=ALEFANTOS_ID)
        # user_gameweek_history = await user.get_gameweek_history()
        # user_chip_history = await user.get_chips_history()
        # user_picks = await user.get_picks()
        # user_subs = await user.get_automatic_substitutions()
        user_transfers = await user.get_transfers()

        ### Get information about the users of this league
        logging.info('Get info about league users')
        user_ids = fpl_data.user_ids_in_league
        logging.info('League users info downloaded')

        logging.info('Store info about league users')
        all_users_dict = {'gameweek_history': {},
                          'chip_history': {},
                          'picks_history': {},
                          'substitutions_history': {},
                          'transfers_history': {}
                          }
        for user_id in user_ids:
            user = await fpl.get_user(user_id=user_id)
            all_users_dict['gameweek_history'][user_id] = await user.get_gameweek_history()
            all_users_dict['chip_history'][user_id] = await user.get_chips_history()
            all_users_dict['picks_history'][user_id] = await user.get_picks()
            all_users_dict['substitutions_history'][user_id] = await user.get_automatic_substitutions()
            all_users_dict['transfers_history'][user_id] = await user.get_transfers()

        fpl_data.read_users_info(all_users_dict)
        logging.info('League users info stored')

        ### Get all the fixtures
        logging.info('Get info of all fixtures')
        fixtures = await fpl.get_fixtures(return_json=True)
        logging.info('Info of all fixtures downloaded')

        logging.info('Store info of all fixtures')
        # Store data into class
        fpl_data.read_fixtures_info(fixtures)
        logging.info('Info of all fixtures stored')

    """
    ### Left for debugging purposes
    league_admin_details = fpl_data.league_admin_details
    league_participants_df = fpl_data.league_participants_df.head()
    pl_teams_lookup_info = fpl_data.pl_teams_lookup_info_df.head()
    players_lookup_info = fpl_data.players_lookup_info_df.head()
    players_history_df = fpl_data.players_history_df.head()
    users_automatic_substitutions = fpl_data.users_automatic_substitutions_history.head()
    users_transfers_history = fpl_data.users_transfers_history.head()
    users_picks_history = fpl_data.users_picks_history.head()
    users_chip_history = fpl_data.users_chip_history.head()
    users_gameweek_history = fpl_data.users_gameweek_history.head()
    fpl_fixture_list = fpl_data.fpl_fixture_list_df.head()

    #pdb.set_trace()
    """


if __name__ == '__main__':

    # Download FPL data
    loop = asyncio.get_event_loop()
    loop.run_until_complete(retrieve_data_from_fpl())
    loop.close()

    # Manage Database

    db_ops = manage_db.Database(DB_ENGINE_LOC)
    engine = db_ops.engine

    # Create Tables (if required) and Load Data
    db_ops.create_objects_in_database_from_scratch()

    table_to_data_dict = {
        'league_participants': fpl_data.league_participants_df,
        'pl_teams_lookup': fpl_data.pl_teams_lookup_info_df,
        'pl_players_lookup': fpl_data.players_lookup_info_df,
        'pl_players_history': fpl_data.players_history_df,
        'users_automatic_substitutions': fpl_data.users_automatic_substitutions_history,
        'users_transfers_history': fpl_data.users_transfers_history,
        'users_pick_history': fpl_data.users_picks_history,
        'users_chip_history': fpl_data.users_chip_history,
        'users_gameweek_history': fpl_data.users_gameweek_history,
        'fpl_fixture_list': fpl_data.fpl_fixture_list_df
    }

    for table_name, df in table_to_data_dict.items():
        logging.debug('Inserting data in {t}...'.format(t=table_name))
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        logging.debug('Data insertion finished')
