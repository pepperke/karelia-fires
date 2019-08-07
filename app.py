# -*- coding: utf-8 -*-
import folium
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
from dash.dependencies import Input, Output
from branca import colormap as cm

df = gpd.read_file('cleared_data.geojson', encoding='utf8')

# / --------- dash related section ---------

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_css)

app.layout = html.Div([
    html.H2('Пожары в Карелии'),
    html.Div([
        html.Label('Выберите год'),
        dcc.Slider(
            id='year-slider',
            min=2015,
            max=2018,
            value=2015,
            marks={str(year): str(year) for year in range(2015, 2019)}
        )
    ], style={'width': '25%', 'margin': 'auto'}
    ),
    html.Div([
        html.Iframe(
            id='map',
            style={'border-style': 'none', 'width': '46%',
                   'min-height': '56vh', 'float': 'left',
                   'margin-left': '4%'}
        ),
        html.Div([
            html.Label(
                'Количество обученных добровольцев в районе ',
                style={'display': 'block'}
            ),
            dcc.Dropdown(
                id='drop-district',
                options=[
                    {'label': i, 'value': i} for i in df.name.unique()
                ],
                value=df.name.iloc[0],
                style={'width': '50%', 'margin': 'auto'}
            ),
            dcc.Graph(
                id='volunteers'
            )
        ], style={'float': 'left', 'height': '56vh', 'width': '50%'}
        )
    ], style={'margin-top': 20, 'display': 'block'}
    ),
    dcc.Graph(
        id='damage',
        style={'position': 'absolute', 'bottom': '0', 'left': '5%',
               'width': '90%', 'height': '30vh'}
    )
], style={'text-align': 'center', 'margin-top': 30}
)

# \
# / --------- folium related section ----------


def style(feature):
    val = feature['properties']['fire_count']
    return {
        'weight': 0.8,
        'color': 'black',
        'opacity': 0.6,
        'fillColor': colormap(val),
        'fillOpacity': 0.6
    }


def highlight(feature):
    return {
        'fillOpacity': 0.8,
        'weight': 1.4,
    }


colormap = cm.linear.YlOrRd_04.scale(
    df.fire_count.quantile(0.05),
    df.fire_count.quantile(0.945)
)
colormap.caption = "Количество пожаров"

tooltip = folium.GeoJsonTooltip(
    fields=["name", "population", "fire_count"],
    aliases=["Район", "Население", "Пожаров"]
)

# \


@app.callback(
    [Output('map', 'srcDoc'),
     Output('damage', 'figure')],
    [Input('year-slider', 'value')]
)
def update_graph(year):
    filtered = df[df.year == year]

    m = folium.Map(location=[64, 33], zoom_start=7)
    folium.GeoJson(
        filtered,
        style_function=style,
        highlight_function=highlight,
        tooltip=tooltip
    ).add_to(m)
    colormap.add_to(m)

    title = 'Материальный ущерб от пожаров (тыс. руб.) в {} году'.format(year)

    fig = px.bar(
        filtered,
        x='name',
        y='damage',
        color='name',
        labels={'name': 'Район', 'damage': 'Ущерб'},
        height=290
    )
    fig.update_layout(
        title_text=title,
        showlegend=False,
        plot_bgcolor='#fff',
        xaxis_title_text='',
        xaxis_tickangle=20,
        yaxis_gridcolor='#ddd',
        yaxis_title_text='Ущерб'
    )
    return m._repr_html_(), fig


@app.callback(
    Output('volunteers', 'figure'),
    [Input('drop-district', 'value')]
)
def draw_volunteers(distr):
    return {
        'data':
            [go.Scatter(
                x=df.year.unique(),
                y=df[df.name == distr].trained_volunteer_count,
                mode='lines+markers')],
        'layout':
            go.Layout(
                xaxis_tick0=2015,
                xaxis_dtick=1,
                yaxis_nticks=10
            )
    }


if __name__ == '__main__':
    app.run_server()
