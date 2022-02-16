from dash import Dash, dcc, html, Input, Output
import altair as alt
import pandas as pd

url = 'https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv'
gm = pd.read_csv(url, parse_dates=['year'])
gm2 = gm[(gm['year'] >= '1961-01-01') & (gm['year'] <= '1965-01-01')]
gm3 = gm2[['income', 'children_per_woman', 'life_expectancy', 'co2_per_capita', 'region', 'year']]

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
        html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),

        html.P('Select x-axis', className = 'fix_label', style = {'color': 'black'}),
        dcc.Dropdown(
            id='xcol_widget',
            value='income',  # REQUIRED to show the plot on the first page load
            options=[{'label': col, 'value': col} for col in gm3.columns]),
        ], className = "create_container2 four columns")

# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    [Input('xcol_widget', 'value')]
    )

def plot_altair(xcol_widget, df=gm3.copy()):
    chart = alt.Chart(df).mark_point().encode(
        x=xcol_widget,
        y='life_expectancy',
        tooltip='life_expectancy').interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)