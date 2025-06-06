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
        'Toy Story', 'Jumanji', 'Heat', 'Casino', 'Braveheart', 'Seven', 'Apollo 13', 'Pocahontas',
        'Die Hard with a Vengeance', 'Clueless', 'Batman Forever', '12 Monkeys', 'The Usual Suspects',
        'Leaving Las Vegas', 'Sense and Sensibility', 'GoldenEye', 'The Bridges of Madison County',
        'Waterworld', 'Dead Man Walking', 'The American President', 'Get Shorty', 'Babe', 'Crimson Tide',
        'Desperado', 'Dangerous Minds', 'While You Were Sleeping', 'Bad Boys', 'Judge Dredd', 'Species',
        'The Quick and the Dead', 'The Net', 'Outbreak', 'The Basketball Diaries', 'Hackers', 'Kids',
        'Tommy Boy', 'Mortal Kombat', 'Rob Roy', 'La Haine', 'Billy Madison', 'Friday', 'Now and Then',
        'A Walk in the Clouds', 'Father of the Bride Part II', 'Balto', 'Sudden Death', 'Cutthroat Island',
        'Nixon', 'It Takes Two', 'Grumpier Old Men'
    ],
    'genres': [
        'Animation|Adventure|Comedy|Family', 'Adventure|Family|Fantasy', 'Action|Crime|Drama', 'Crime|Drama',
        'Biography|Drama|History', 'Crime|Drama|Mystery', 'Adventure|Drama|History', 'Animation|Adventure|Drama',
        'Action|Thriller', 'Comedy|Romance', 'Action|Adventure', 'Sci-Fi|Thriller', 'Crime|Drama|Mystery',
        'Drama|Romance', 'Drama|Romance', 'Action|Adventure|Thriller', 'Drama|Romance', 'Action|Adventure|Sci-Fi',
        'Biography|Crime|Drama', 'Comedy|Drama|Romance', 'Comedy|Crime', 'Comedy|Drama|Family', 'Action|Thriller',
        'Action|Thriller', 'Drama', 'Comedy|Drama|Romance', 'Action|Comedy|Crime', 'Action|Sci-Fi', 'Horror|Sci-Fi',
        'Action|Thriller|Western', 'Action|Crime|Drama', 'Action|Drama|Sci-Fi', 'Biography|Crime|Drama', 'Crime|Drama',
        'Drama', 'Comedy', 'Action|Adventure|Fantasy', 'Action|Biography|Drama', 'Crime|Drama', 'Comedy',
        'Comedy|Drama', 'Comedy|Drama', 'Drama|Romance', 'Comedy', 'Animation|Adventure|Drama', 'Action|Thriller',
        'Action|Adventure', 'Biography|Drama', 'Comedy|Family', 'Comedy|Romance'
    ],
    'averageRating': [
        8.3, 7.5, 8.2, 8.2, 8.4, 8.6, 7.6, 6.7, 7.6, 6.9, 5.4, 8.0, 8.5,
        7.5, 7.6, 7.1, 7.6, 6.3, 7.5, 6.8, 6.9, 6.9, 7.3, 7.2, 6.5, 6.8,
        6.9, 5.5, 5.8, 6.4, 5.5, 6.6, 7.3, 6.2, 7.6, 7.1, 6.1, 7.0, 8.1,
        6.4, 7.2, 6.8, 6.7, 5.7, 7.1, 6.4, 5.7, 7.1, 5.8, 6.7
    ],
    'releaseDate': [
        '1995-11-22', '1995-12-15', '1995-12-15', '1995-11-22', '1995-05-24', '1995-09-22', '1995-06-30',
        '1995-06-16', '1995-05-19', '1995-07-19', '1995-06-16', '1995-12-29', '1995-08-16', '1995-10-27',
        '1995-12-13', '1995-11-17', '1995-06-02', '1995-07-28', '1995-12-29', '1995-11-17', '1995-10-20',
        '1995-08-04', '1995-05-12', '1995-08-25', '1995-08-11', '1995-04-21', '1995-04-21', '1995-06-30',
        '1995-07-07', '1995-02-10', '1995-07-28', '1995-03-10', '1995-04-21', '1995-09-15', '1995-09-27',
        '1995-03-31', '1995-08-18', '1995-04-07', '1995-05-31', '1995-02-10', '1995-04-26', '1995-10-20',
        '1995-08-11', '1995-12-08', '1995-12-22', '1995-12-22', '1995-12-22', '1995-12-22', '1995-11-17',
        '1995-11-22'
    ]
}

movies_final = pd.DataFrame(data)
movies_final['releaseDate'] = pd.to_datetime(movies_final['releaseDate'])
movies_final['releaseDate'] = movies_final['releaseDate'].dt.strftime('%Y-%m-%d')

movies_final['genres'] = movies_final['genres'].str.split('|')
movies_exploded = movies_final.explode('genres')
movies_final['genres'] = movies_final['genres'].apply(lambda x: ', '.join(x))

genre_ratings = movies_exploded.groupby('genres')['averageRating'].mean().reset_index()
top_genre = genre_ratings.sort_values(by='averageRating', ascending=False).iloc[0]
bottom_genre = genre_ratings.sort_values(by='averageRating').iloc[0]

fig_bar = px.bar(
    genre_ratings.sort_values(by='averageRating', ascending=False),
    x='genres',
    y='averageRating',
    title='Movie Ratings by Genre'
)

fig_scatter = px.scatter(movies_exploded, x='genres', y='averageRating', title='Comparing Movies Based on Ratings and Genres')

fig_line = px.line(movies_final.sort_values('releaseDate'), x='releaseDate', y='averageRating', title='Trends in Movie Ratings Over Time')

genre_counts = movies_exploded['genres'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
fig_pie = px.pie(genre_counts, names='Genre', values='Count', title='Genre Distribution (by count)')

genre_counts = movies_exploded['genres'].value_counts().reset_index()
genre_counts.columns = ['genres', 'movieCount']

fig_count = px.bar(
    genre_counts.head(5),
    x='genres',
    y='movieCount',
    title='Top 5 Genres by Number of Movies',
    color='movieCount',
    text='movieCount'
)

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

                html.Div(id='search-results')
            ])
        ]),
        dcc.Tab(label='Analysis', children=[
            html.Div([
                dcc.Graph(id='genre-ratings-bar-chart', figure=fig_bar),
                dcc.Graph(id='scatter-plot', figure=fig_scatter),
                dcc.Graph(id='line-chart', figure=fig_line),
                dcc.Graph(id='genre-pie-chart', figure=fig_pie),
                dcc.Graph(id='genre-count-chart', figure=fig_count),
                html.Div([
                    html.H4("Genre Analysis Summary"),
                    html.P(f"Highest rated genre: {top_genre['genres']} with an average rating of {top_genre['averageRating']:.2f}"),
                    html.P(f"Lowest rated genre: {bottom_genre['genres']} with an average rating of {bottom_genre['averageRating']:.2f}")
                ], style={
                    'marginTop': '20px',
                    'padding': '10px',
                    'border': '1px solid #ccc',
                    'borderRadius': '5px'
                }),
                        
                html.H2("Movie Table"),
                dash_table.DataTable(
                    id='movie-table',
                    columns=[
                        {'name': 'Title', 'id': 'title'},
                        {'name': 'Genres', 'id': 'genres'},
                        {'name': 'Rating', 'id': 'averageRating'},
                        {'name': 'Release Date', 'id': 'releaseDate'}
                    ],
                    data=movies_final.sort_values(by='averageRating', ascending=False).to_dict('records'),
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
    sorted_df = movies_final.sort_values(by='averageRating', ascending=False)
    if selected_rows is None or len(selected_rows) == 0:
        return html.P("Click a row in the table to see movie details.")

    row = sorted_df.iloc[selected_rows[0]]
    return html.Div([
        html.H3(f"{row['title']}"),
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
