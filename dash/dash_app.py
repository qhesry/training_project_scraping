import dash 
from dash import dcc
from dash import html
import plotly.graph_objs as go
import requests
import pandas as pd

app = dash.Dash(__name__)

# Configuration du serveur
server = app.server

# URL de l'API FastAPI
base_url = "http://localhost:8000"

# Options pour la liste déroulante
vpn_options = [
    {'label': 'CyberGhost VPN', 'value': 'CyberGhost VPN'},
    {'label': 'NordVPN', 'value': 'NordVPN'}
]

# Requête l'API FastAPI et renvoie les données dans un DataFrame
def query_data(endpoint):
    url = f"{base_url}{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except ValueError:
            print("API Reponse is not in JSON format")
    else:
        print(f"API request have failed : {response.status_code}")

# Callback pour mettre à jour les données en fonction de la sélection de l'utilisateur
@app.callback(
    [dash.dependencies.Output('average-rating', 'children'),
     dash.dependencies.Output('total-reviews', 'children'),
     dash.dependencies.Output('rating-distribution', 'figure'),
     dash.dependencies.Output('top-title-terms', 'figure'),
     dash.dependencies.Output('average-sentiment', 'children'),
     dash.dependencies.Output('average-accuracy', 'children')],
    [dash.dependencies.Input('vpn-select', 'value')]
)
def update_data(vpn):
    # Indicateur 1 : Moyenne des notes de chaque entreprise
    endpoint = f"/average-rating-by-company/{vpn}"
    average_rating = query_data(endpoint)['average_rating']

    # Indicateur 2 : Nombre total de reviews pour chaque entreprise
    endpoint = f"/total-reviews-by-company/{vpn}"
    total_reviews = query_data(endpoint)['total_reviews']

    # Indicateur 3 : Distribution des notes par entreprise
    endpoint = f"/rating-distribution-by-company/{vpn}"
    distribution = query_data(endpoint)["rating_distribution"]

    # Indicateur 4 : Les termes les plus fréquents dans les titres et le contenu des reviews
    endpoint = f"/top-terms/{vpn}"
    top_terms_data = query_data(endpoint)
    top_title_terms = top_terms_data["top_title_terms"]

    # Indicateur 5 : Score de sentiment moyen pour chaque entreprise
    endpoint = f"/average-sentiment-by-company/{vpn}"
    average_sentiment = query_data(endpoint)['average_sentiment']

    # Indicateur 6 : Score d'exactitude moyen pour chaque entreprise
    endpoint = f"/average-accuracy-by-company/{vpn}"
    average_accuracy = query_data(endpoint)['average_accuracy']

    # Graphique 1 : Distribution des notes
    x = sorted(distribution.keys())
    y = [distribution[key] for key in x]
    fig1 = go.Figure([go.Bar(x=x, y=y, marker_color="royalblue")])

    # Graphique 2 : Les termes les plus fréquents dans les titres
    
    fig2 = go.Figure([go.Bar(x=[x[0] for x in top_title_terms], y=[y[1] for y in top_title_terms], marker_color="crimson")])

    return average_rating, total_reviews, fig1, fig2, average_sentiment, average_accuracy

# Layout
app.layout = html.Div([
    html.H1("Indicateurs pour CyberGhost VPN et NordVPN"),
    html.Div([
        dcc.Dropdown(
            id='vpn-select',
            options=vpn_options,
            value='CyberGhost VPN',
            clearable=False,
            style={
                'width': '200px',
                'margin-bottom': '10px'
            }
        ),
    ]),
    html.Div([
        html.Span('Note moyenne : ', style={'margin-right':'5px', 'font-size': '1.5rem'}),
        html.Span(id='average-rating'),
    ]),
    html.Div([
        html.Span('Nombre total de reviews : ', style={'margin-right':'5px', 'font-size': '1.5rem'}),
        html.Span(id='total-reviews'),
    ], style={'margin-top': '20px'}),
    html.Div([
        html.H2('Distribution des notes'),
        dcc.Graph(id='rating-distribution', config={'displayModeBar': False}),
    ], style={'margin-top': '20px'}),
    html.Div([
        html.H2('Les termes les plus fréquents dans les titres'),
        dcc.Graph(id='top-title-terms', config={'displayModeBar': False}),
    ], style={'margin-top': '20px'}),
    html.Div([
        html.Span('Score de sentiment moyen : ', style={'font-size': '1.5rem'}),
        html.Span(id='average-sentiment'),
    ], style={'margin-top': '20px'}),
    html.Div([
        html.Span('Score d\'exactitude moyen : ', style={'font-size': '1.5rem'}),
        html.Span(id='average-accuracy'),
    ], style={'margin-top': '20px'}),
], style={'margin': '20px'})

if __name__ == '__main__':
    app.run_server(debug=True)