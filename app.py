from dash import dcc, html, dash_table, Input, Output, State
import dash
import pandas as pd
import plotly.express as px

# Read data from CSV
df = pd.read_csv('data.csv')
# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = 'Network Planning System (NPS)'

# Define the layout using Dash components
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Download(id="download-dataframe-csv"),
    html.Link(href='/assets/style.css', rel='stylesheet'),
    html.Link(href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css', rel='stylesheet'),
    html.Link(href='https://maxst.icons8.com/vue-static/landings/line-awesome/line-awesome/1.3.0/css/line-awesome.min.css', rel='stylesheet')
])

# Callback to render the page content
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    return html.Div([
        html.Div([
            html.Label('Menu Toggle'),
            html.Div(id='menu-toggle-container', children=[
                html.Div([
                    dcc.Checklist(
                        options=[{'label': '', 'value': 'checked'}],
                        id='menu-toggle',
                        inputStyle={'cursor': 'pointer'}
                    )
                ], style={'display': 'inline-block'})
            ]),
        ], className='toggle-container'),

        html.Div(className='sidebar', children=[
            html.Div(className='side-header', children=[
                html.H3('Layout')
            ]),
            html.Div(className='side-menu', children=[
                html.Ul(children=[
                    html.Li(children=[
                        html.A(href='index.html', className='active', children=[
                            html.Span(className='fa-solid fa-network-wired'),
                            html.Small('Network Plan')
                        ])
                    ]),
                    html.Li(children=[
                        html.A(href='#', children=[
                            html.Span(className='las la-user-alt'),
                            html.Small('Demand Flow')
                        ])
                    ]),
                    html.Li(children=[
                        html.A(href='#', children=[
                            html.Span(className='las la-envelope'),
                            html.Small('Performance Report')
                        ])
                    ])
                ])
            ])
        ]),
        html.Div(className='main-content', children=[
            html.Header(children=[
                html.Div(className='header-content', children=[
                    html.Label(htmlFor='menu-toggle', children=[
                        html.Span(className='las la-bars')
                    ]),
                    html.Div(className='header-menu', children=[
                        html.Div(className='notify-icon', children=[
                            html.Span(className='las la-bell'),
                            html.Span('3', className='notify')
                        ]),
                        html.Div(className='user', children=[
                            html.Span(className='fas fa-user', style={'margin-right': '8px'}),
                            html.Span('Logout')
])
                    ])
                ])
            ]),
            html.Main(children=[
                html.Div(className='page-header', children=[
                    html.H1('Network Planning System (NPS)')
                ]),
                html.Div(className='page-content', children=[
                    html.Div(className='analytics', children=[
                        dcc.Dropdown(
                            id='family-code',
                            options=[
                                {'label': 'Select a vendor', 'value': ''},
                                {'label': 'ABC', 'value': 'ABC'},
                                {'label': 'XYZ', 'value': 'XYZ'}
                            ],
                            placeholder='Select a vendor'
                        ),
                        dcc.Dropdown(
                            id='family-code',
                            options=[
                                {'label': 'Select a family code', 'value': ''},
                                {'label': 'Family 1', 'value': 'Family 1'},
                                {'label': 'Family 2', 'value': 'Family 2'}
                            ],
                            placeholder='Select a family code'
                        ),
                        dcc.Dropdown(
                            id='site',
                            options=[
                                {'label': 'Select a site', 'value': ''},
                                {'label': 'Site A', 'value': 'Site A'},
                                {'label': 'Site B', 'value': 'Site B'}
                            ],
                            placeholder='Select a site'
                        )
                    ]),
                    html.Div(className='records table-responsive', children=[
                        html.Div(className='record-header', children=[
                            html.Div(className='add', children=[
                                html.A(href='#', children=[
                                    html.Span('Summary')
                                ])
                            ]),
                            html.Div(className='browse', children=[
                                html.A(href='#', children=[
                                    html.Span('Transfers')
                                ])
                            ])
                        ]),
                        html.Div(id='dynamic-content', children=[
                            dash_table.DataTable(
                                id='table',
                                columns=[{"name": i, "id": i, 'type': 'text'} for i in df.columns],
                                data=df.to_dict('records'),
                                page_size=5,
                                style_table={'overflowX': 'auto'},
                                style_cell={'textAlign': 'center'}
                            ),
                            html.Div(className='action-buttons', children=[
                                html.Div(className='line', children=[
                                    html.Button('Download as CSV', id='download-csv-btn', className='download-btn-table')
                            ]),
                            dcc.Graph(
                                id='quantity-graph'
                            ),
                            
                               
                                html.Div(className='line', children=[
                                    html.Div(className='date-input', children=[
                                        dcc.Input(type='text', placeholder='Date (MM/DD/YY)')
                                    ]),
                                    html.Button('Generate SAP Files', className='generate-btn')
                                ])
                            ])
                        ])
                    ])
                ])
            ])
        ]),
        html.Footer(className='footer', children=[
            html.P('© 2024 Network Planning System. All rights reserved.')
        ])
    ])

# Callback to dynamically generate graph
@app.callback(
    Output('quantity-graph', 'figure'),
    Input('table', 'data')
)
def update_graph(data):
    df = pd.DataFrame(data)
    # Debugging: Print the dataframe to the console
    print(df)

    fig = px.bar(df, x='Week Date', y='Quantity', 
                  title='Week Date and Quantity',
                  labels={'Week Date': 'Week Date', 'value': 'Count'},
                  template=None)
    fig.update_traces(marker=dict(
        color='rgba(60, 179, 113, 0.2)',
        line=dict(color='rgba(60, 179, 113, 1)', width=1.5)
    ))
    # Update layout for better visualization
    fig.update_layout(
        xaxis_title='Week Date',
        yaxis_title='Count',
        legend_title='Metrics',
        legend=dict(x=0.1, y=1.1, orientation='h'),
         xaxis=dict(
            tickformat='%Y-%m-%d',
            tickmode='array',
            tickvals=df['Week Date']
        ),
        hovermode='x unified',
        plot_bgcolor='#E9edf2',
        paper_bgcolor='#E9edf2'
    )
    
    return fig
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("download-csv-btn", "n_clicks"),
    State("table", "data"),
    prevent_initial_call=False,
)
def download_csv(n_clicks, table_data):
    if n_clicks is not None and n_clicks > 0:
        df = pd.DataFrame(table_data)
        csv_string = df.to_csv(index=False, encoding='utf-8-sig')
        return dcc.send_data_frame(df.to_csv, filename="table.csv")
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
