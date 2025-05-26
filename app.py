import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)
server = app.server

data = {
    'title': [
        'Toy Story', 'Jumanji', 'Grumpier Old Men', 'Waiting to Exhale', 'Father of the Bride Part II',
        'Heat', 'Sabrina', 'Tom and Huck', 'Sudden Death', 'GoldenEye'
    ],
    'genres': [
        'Adventure|Animation|Children|Comedy|Fantasy', 'Adventure|Children|Fantasy', 'Comedy|Romance',
        'Comedy|Drama|Romance', 'Comedy', 'Action|Crime|Thriller', 'Comedy|Romance', 'Adventure|Children',
        'Action', 'Action|Adventure|Thriller'
    ],
    'averageRating': [8.3, 7.5, 6.7, 6.2, 5.7, 8.2, 6.3, 5.5, 6.4, 7.1],
    'releaseDate': [
        '1995-11-22', '1995-12-15', '1995-12-22', '1995-12-22', '1995-12-08',
        '1995-12-15', '1995-12-15', '1995-12-22', '1995-12-22', '1995-11-17'
    ]
}
movies_final = pd.DataFrame(data)
movies_final['releaseDate'] = pd.to_datetime(movies_final['releaseDate'])
movies_final['releaseDate'] = movies_final['releaseDate'].dt.strftime('%Y-%m-%d')

movies_final['genres'] = movies_final['genres'].str.split('|')
movies_exploded = movies_final.explode('genres')
movies_final['genres'] = movies_final['genres'].apply(lambda x: ', '.join(x))

genre_ratings = movies_exploded.groupby('genres')['averageRating'].mean().reset_index()

fig_bar = px.bar(genre_ratings, x='genres', y='averageRating', title='Movie Ratings by Genre')

fig_scatter = px.scatter(movies_exploded, x='genres', y='averageRating', title='Comparing Movies Based on Ratings and Genres')

fig_line = px.line(movies_final.sort_values('releaseDate'), x='releaseDate', y='averageRating', title='Trends in Movie Ratings Over Time')

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Dashboard', children=[
            html.Div([
                html.Div([
                    html.Img(src='/assets/icon.png', style={'height': '50px', 'marginRight': '15px'}),
                    html.H1('Movie Reviewer Dashboard', style={'margin': 0})
                ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'gap': '15px', 'paddingTop': '20px'}),

                html.Div([
                    dcc.Input(
                        id='search-bar',
                        type='text',
                        placeholder='Search movies by title or genre',
                        style={'width': '80%', 'padding': '10px'}
                    ),
                    html.Button('Search', id='search-button', n_clicks=0)
                ], style={'textAlign': 'center', 'padding': '20px'}),

                html.Div([
                    dcc.Dropdown(
                        id='genre-dropdown',
                        options=[{'label': genre, 'value': genre} for genre in genre_ratings['genres'].unique()],
                        placeholder='Select genre'
                    )
                ], style={'width': '50%', 'margin': 'auto', 'padding': '20px'}),

                html.Div([
                    dcc.RangeSlider(
                        id='rating-slider',
                        min=movies_final['averageRating'].min(),
                        max=movies_final['averageRating'].max(),
                        step=0.1,
                        marks={i: str(i) for i in range(int(movies_final['averageRating'].min()), int(movies_final['averageRating'].max())+1)},
                        value=[movies_final['averageRating'].min(), movies_final['averageRating'].max()]
                    )
                ], style={'width': '50%', 'margin': 'auto', 'padding': '20px'}),

                html.Div([
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        start_date=movies_final['releaseDate'].min(),
                        end_date=movies_final['releaseDate'].max(),
                        display_format='YYYY-MM-DD'
                    )
                ], style={'textAlign': 'center', 'padding': '20px'}),

                html.Div(id='search-results'),

                dcc.Graph(id='genre-ratings-bar-chart', figure=fig_bar),
                dcc.Graph(id='scatter-plot', figure=fig_scatter),
                dcc.Graph(id='line-chart', figure=fig_line),
                
                html.H2("Movie Table"),
                dash_table.DataTable(
                    id='movie-table',
                    columns=[
                        {'name': 'Title', 'id': 'title'},
                        {'name': 'Genres', 'id': 'genres'},
                        {'name': 'Rating', 'id': 'averageRating'},
                        {'name': 'Release Date', 'id': 'releaseDate'}
                    ],
                    data=movies_final.to_dict('records'),
                    row_selectable='single',
                    selected_rows=[],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left'},
                    page_size=10
                ),
                html.Div(id='selected-movie-details', style={'marginTop': '20px'})
            ])
        ]),
        dcc.Tab(label='About', children=[
            html.Div([
                html.H3("About This Dashboard"),
                html.P("This dashboard allows users to explore, filter, and visualize movie data, including ratings, genres, and release dates."),
                html.P("It uses data from MovieLens, OMDb API, and IMDb.")
            ], style={'padding': '30px'})
        ]),
        dcc.Tab(label='Help', children=[
            html.Div([
                html.H3("How to Use This Dashboard"),
                html.Ul([
                    html.Li("Use the search bar to find movies by title or genre."),
                    html.Li("Use the dropdown and sliders to filter by genre, rating, and release date."),
                    html.Li("Explore charts to compare ratings by genre, trends over time, and more.")
                ])
            ], style={'padding': '30px'})
        ])
    ])
])

@app.callback(
    Output('selected-movie-details', 'children'),
    [Input('movie-table', 'selected_rows')]
)
def display_selected_movie(selected_rows):
    if selected_rows is None or len(selected_rows) == 0:
        return html.P("Click a row in the table to see movie details.")

    row = movies_final.iloc[selected_rows[0]]
    return html.Div([
        html.H3(f"🎬 {row['title']}"),
        html.P(f"Genres: {row['genres']}"),
        html.P(f"Average Rating: {row['averageRating']}"),
        html.P(f"Release Date: {row['releaseDate']}")
    ], style={'border': '1px solid #ccc', 'padding': '10px', 'borderRadius': '5px'})

@app.callback(
    Output('search-results', 'children'),
    [Input('search-button', 'n_clicks'), Input('genre-dropdown', 'value'), Input('rating-slider', 'value'), Input('date-picker-range', 'start_date'), Input('date-picker-range', 'end_date')],
    [dash.dependencies.State('search-bar', 'value')]
)
def update_search_results(n_clicks, selected_genre, rating_range, start_date, end_date, search_value):
    filtered_df = movies_final
    
    if search_value:
        search_value_lower = search_value.lower()
        filtered_df = filtered_df[
            filtered_df['title'].str.lower().str.contains(search_value_lower, na=False) |
            filtered_df['genres'].str.lower().str.contains(search_value_lower, na=False)
        ]
    
    if selected_genre:
        filtered_df = filtered_df[filtered_df['genres'].apply(lambda x: selected_genre in x)]
    
    if rating_range:
        filtered_df = filtered_df[(filtered_df['averageRating'] >= rating_range[0]) & (filtered_df['averageRating'] <= rating_range[1])]
    
    if start_date and end_date:
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df['releaseDate']) >= pd.to_datetime(start_date)) &
            (pd.to_datetime(filtered_df['releaseDate']) <= pd.to_datetime(end_date))
        ]
    
    results = []
    for _, row in filtered_df.iterrows():
        results.append(html.Div([
            html.H3(row['title']),
            html.P(f"Genres: {row['genres']}"),
            html.P(f"Rating: {row['averageRating']}"),
            html.P(f"Release Date: {row['releaseDate']}")
        ], style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'}))
    
    return results

if __name__ == '__main__':
    app.run_server(debug=True)
