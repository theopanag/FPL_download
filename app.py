# dash libs
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# pydata stack
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

from fpl_test import DB_ENGINE_LOC

import pdb

# set params
conn = create_engine(DB_ENGINE_LOC)


###########################
# Data Manipulation / Model
###########################

def fetch_data(q):
    """
    Fetch data from database
    :param q: SQL query for data selection
    :return: pd.DataFrame with corresponding information
    """
    df = pd.read_sql(
        sql=q,
        con=conn
    )
    return df


sql_query = "SELECT * FROM users_pick_history_V"

df = fetch_data(sql_query)

#########################
# Dashboard Layout / View
#########################

ELEMENT_TYPE_DICT = {
    "Goalkeeper": 1,
    "Defense": 2,
    "Midfield": 3,
    "Attack": 4
}

REVERSE_ELEMENT_TYPE_DICT = {v:k for k, v in ELEMENT_TYPE_DICT.items()}
DEFAULT_ELEMENT_TYPE = 2

# Set up Dashboard and create layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    # Page Header
    html.Div(
        html.H1("Initial Version of FPL Mini League explorer")
    ),
    # Subheader?
    html.Div(
        "Dash web application example"
    ),
    # Radio items with options regarding Goalkeeper, Defense, Midfield, Attack
    dcc.RadioItems(
        id="area_selection",
        options=[{"label": k, "value": v} for k, v in ELEMENT_TYPE_DICT.items()],
        value='{}'.format(DEFAULT_ELEMENT_TYPE)
    ),
    # Dropdown menu to select the bars to be highlighted
    dcc.Dropdown(
        id="highlight_selection",
        options=[{"label": k, "value": k} for k in df.entry_name.unique()],
        multi=True
    ),
    # Barplot creating the results
    dcc.Graph(
        id="barplot_average_score_per_player&gameweek"
    )

])


#############################################
# Interaction Between Components / Controller
#############################################

@app.callback(
    Output('barplot_average_score_per_player&gameweek', 'figure'),
    [Input('area_selection', 'value'),
     Input("highlight_selection", "value")]
)
def update_figure(selected_area_value, highlight_selection):
    filtered_df = df.loc[
        (df.element_type.isin([selected_area_value, ])) & (df.multiplier != 0), ["entry_name", "total_points"]
    ]
    avg_score_df = filtered_df.groupby(by="entry_name").mean().reset_index().rename(
        columns={"total_points": "avg_points"}
    ).sort_values(by=["avg_points", "entry_name"], ascending=[False, True]).reset_index()
    colors = ['lightskyblue', ] * avg_score_df.shape[0]
    # pdb.set_trace()
    if highlight_selection:
        for bar in highlight_selection:
            colors[avg_score_df.loc[avg_score_df.entry_name == bar].index[0]] = "crimson"

    data = [
        {
            "x": avg_score_df.entry_name,
            "y": avg_score_df.avg_points,
            "text": avg_score_df.avg_points,
            "type": "bar",
            "marker": {"color": colors},
            "orientation": "v",
            "texttemplate": '%{text:.3s}',
            "textposition": 'inside'
        }
    ]
    layout = {
        "title": {"text": "Average points from a player in {}".format(REVERSE_ELEMENT_TYPE_DICT.get(
            selected_area_value,REVERSE_ELEMENT_TYPE_DICT.get(DEFAULT_ELEMENT_TYPE)
        )),
                  "yanchor": "top",
                  "font": {"size": 26}},
        "xaxis": {"title": "Team name", "titlefont": {"size": 18}},
        "yaxis": {"title": "Average points", "titlefont": {"size": 18}},
        "margin": {'l': 100, 'b': 200, 't': 10, 'r': 200},
        "hovermode": 'closest',
        "height": 450
    }

    return {
        'data': data,
        'layout': layout
    }


# start Flask server
if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='localhost',
        port=8050
    )
