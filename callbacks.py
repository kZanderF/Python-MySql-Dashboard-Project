from dash.dependencies import Input, Output
from queries import fetch_sales_data, fetch_gp_data, fetch_quantity_data, fetch_profit_data, fetch_ytd_vs_pytd

def register_callbacks(app, conn):
    
    @app.callback(
        [Output('sales-graph', 'figure'),
         Output('gp-graph', 'figure'),
         Output('quantity-graph', 'figure'),
         Output('profit-graph', 'figure'),
         Output('ytd-pytd-graph', 'figure')],
        [Input('product-filter', 'value'),
         Input('country-filter', 'value'),
         Input('date-picker', 'start_date'),
         Input('date-picker', 'end_date')]
    )
    def update_graphs(products, countries, start_date, end_date):
        df_sales = fetch_sales_data(conn, products, countries, start_date, end_date)
        df_gp = fetch_gp_data(conn, products, countries, start_date, end_date)
        df_quantity = fetch_quantity_data(conn, products, countries, start_date, end_date)
        df_profit = fetch_profit_data(conn, products, countries, start_date, end_date)
        df_ytd_pytd = fetch_ytd_vs_pytd(conn, products, countries, start_date, end_date)

        sales_figure = {
            'data': [{'x': df_sales['Date_Time'], 'y': df_sales['Sales_USD'], 'type': 'bar', 'name': 'Sales'}],
            'layout': {'title': 'Sales Over Time'}
        }
        
        gp_figure = {
            'data': [{'x': df_gp['Date_Time'], 'y': df_gp['GP%'], 'type': 'line', 'name': 'GP%'}],
            'layout': {'title': 'Gross Profit Percentage'}
        }

        quantity_figure = {
            'data': [{'x': df_quantity['Date_Time'], 'y': df_quantity['Quantity'], 'type': 'bar', 'name': 'Quantity'}],
            'layout': {'title': 'Quantity Sold'}
        }

        profit_figure = {
            'data': [{'x': df_profit['Date_Time'], 'y': df_profit['Profit'], 'type': 'bar', 'name': 'Profit'}],
            'layout': {'title': 'Profit Over Time'}
        }

        ytd_pytd_figure = {
            'data': [{'x': df_ytd_pytd['Year'], 'y': df_ytd_pytd['Sales'], 'type': 'bar', 'name': 'YTD vs PYTD'}],
            'layout': {'title': 'YTD vs PYTD Sales'}
        }

        return sales_figure, gp_figure, quantity_figure, profit_figure, ytd_pytd_figure
