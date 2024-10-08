import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from queries import df_sales

# Initialize the Dash app
app = dash.Dash(__name__)

# Create layout for the app
app.layout = html.Div([
    html.Div([
        html.H1(id='dashboard-title', className='dashboard-title'),  # Dynamic title with ID
    ], className='header-container'),  # Container for the header

    html.Div(className='controls-container', children=[
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in [2023, 2024]],  # Limit to 2023 and 2024
            value=2023,  # Default to 2023
            clearable=False,
            className='year-dropdown'  # Specific class for year dropdown
        ),
        html.Div(className='metric-box', children=[
            dcc.RadioItems(
                id='metric-radio',
                options=[
                    {'label': 'Sales', 'value': 'Sales_USD'},
                    {'label': 'Quantity', 'value': 'Quantity'},
                    {'label': 'Gross Profit', 'value': 'Gross_Profit'}
                ],
                value='Sales_USD',  # Default to Sales
                labelStyle={'display': 'block'},  # Stack items vertically
            )
        ]),
        html.Div(id='ytd-info', className='ytd-info'),  # YTD info with class
    ]),  # Removed the 'className' from here

    html.Div(className='graph-container', children=[
        dcc.Graph(id='waterfall-chart', className='waterfall-graph'),  # Specific class for waterfall chart
        dcc.Graph(id='line-stacked-chart', className='line-stacked-graph')  # Specific class for line and stacked chart
    ]),
])

# Calculate Gross Profit dynamically: Gross Profit = Sales - COGS
df_sales['Gross_Profit'] = df_sales['Sales_USD'] - df_sales['COGS_USD']

# Callback to update YTD, PYTD, GP%, and dynamic title
@app.callback(
    Output('ytd-info', 'children'),
    Output('dashboard-title', 'children'),  # Added output for dynamic title
    Input('year-dropdown', 'value'),
    Input('metric-radio', 'value')
)
def update_ytd_info(selected_year, selected_metric):
    filtered_df = df_sales[df_sales['Date_time'].dt.year == selected_year]

    # Calculate YTD based on selected metric
    if selected_metric == 'Sales_USD':
        ytd = filtered_df['Sales_USD'].sum()  # Total Sales
    elif selected_metric == 'Quantity':
        ytd = filtered_df['Quantity'].sum()  # Total Quantity
    elif selected_metric == 'Gross_Profit':
        ytd = filtered_df['Gross_Profit'].sum()  # Gross Profit

    # Calculate PYTD (previous year to date) for selected metric
    if selected_metric == 'Sales_USD':
        pytd = df_sales[df_sales['Date_time'].dt.year == selected_year - 1]['Sales_USD'].sum()  # Previous Year Sales
    elif selected_metric == 'Quantity':
        pytd = df_sales[df_sales['Date_time'].dt.year == selected_year - 1]['Quantity'].sum()  # Previous Year Quantity
    elif selected_metric == 'Gross_Profit':
        pytd = df_sales[df_sales['Date_time'].dt.year == selected_year - 1]['Gross_Profit'].sum()  # Previous Year Gross Profit

    ytd_vs_pytd = ytd - pytd  # YTD vs PYTD calculation

    # GP% Calculation (always displayed)
    total_sales_ytd = filtered_df['Sales_USD'].sum()
    gp_percentage = (filtered_df['Gross_Profit'].sum() / total_sales_ytd * 100) if total_sales_ytd > 0 else 0
    gp_text = f"GP%: {gp_percentage:.2f}%"
    dynamic_title = f"Plant Co. {get_metric_label(selected_metric)} Performance {selected_year}"  # Dynamic title


    return f"YTD: {ytd:,.2f}, PYTD: {pytd:,.2f}, YTD vs PYTD: {ytd_vs_pytd:,.2f} {gp_text}", dynamic_title  # Return title as output

# Function to map the metric to a user-friendly name
def get_metric_label(metric_value):
    if metric_value == 'Sales_USD':
        return 'Sales'
    elif metric_value == 'Quantity':
        return 'Quantity'
    elif metric_value == 'Gross_Profit':
        return 'Gross Profit'
    return metric_value

# Callback to update waterfall chart based on selected year and metric
# Callback to update waterfall chart based on selected year and metric
@app.callback(
    Output('waterfall-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('metric-radio', 'value')
)
def update_waterfall_chart(selected_year, selected_metric):
    filtered_df = df_sales[df_sales['Date_time'].dt.year == selected_year]

    # Grouping by month for waterfall chart
    grouped_df = filtered_df.groupby(filtered_df['Date_time'].dt.month)[selected_metric].sum().reset_index()
    grouped_df.columns = ['Month', selected_metric]

    # Calculate YTD vs PYTD
    ytd = grouped_df[selected_metric].sum()
    pytd = df_sales[df_sales['Date_time'].dt.year == selected_year - 1].groupby(df_sales['Date_time'].dt.month)[selected_metric].sum().reset_index()
    pytd.columns = ['Month', 'PYTD']

    # Merge YTD and PYTD data
    merged_df = pd.merge(grouped_df, pytd, on='Month', how='left')
    merged_df['YTD_vs_PYTD'] = merged_df[selected_metric] - merged_df['PYTD'].fillna(0)

    # Adding the text value with thousands separator
    merged_df['text_value'] = merged_df['YTD_vs_PYTD'].apply(lambda x: f"{x:,.2f}")

    # Get the metric label for the chart title
    metric_label = get_metric_label(selected_metric)

    # Waterfall chart
    figure = {
        'data': [
            {
                'x': merged_df['Month'],
                'y': merged_df['YTD_vs_PYTD'],
                'type': 'waterfall',
                'name': f'{metric_label} YTD vs PYTD',
                'text': merged_df['text_value'],
                'textposition': 'outside',  # Set all text positions to outside
            },
        ],
        'layout': {
            'title': f'{metric_label} YTD vs PYTD | Month',  # Update the title with a user-friendly metric name
            'xaxis': {
                'title': 'Month',
                'tickvals': list(range(1, 13)),
                'ticktext': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            },
            'yaxis': {'title': f'{metric_label} YTD vs PYTD'},
        }
    }
    return figure

# Callback to update line and stacked column chart based on selected year and metric
@app.callback(
    Output('line-stacked-chart', 'figure'),
    Input('year-dropdown', 'value'),
    Input('metric-radio', 'value')
)
def update_line_stacked_chart(selected_year, selected_metric):
    # Filter sales data for the selected year
    filtered_df = df_sales[df_sales['Date_time'].dt.year == selected_year]

    # Grouping by month for YTD values
    ytd_df = filtered_df.groupby(filtered_df['Date_time'].dt.month).agg({
        'Sales_USD': 'sum',
        'Quantity': 'sum',
        'Gross_Profit': 'sum'
    }).reset_index()

    ytd_df.columns = ['Month', 'YTD_Sales', 'YTD_Quantity', 'YTD_Gross_Profit']

    # Calculate PYTD values for the previous year
    pytd_df = df_sales[df_sales['Date_time'].dt.year == selected_year - 1].groupby(df_sales['Date_time'].dt.month).agg({
        'Sales_USD': 'sum',
        'Quantity': 'sum',
        'Gross_Profit': 'sum'
    }).reset_index()

    pytd_df.columns = ['Month', 'PYTD_Sales', 'PYTD_Quantity', 'PYTD_Gross_Profit']

    # Debugging: Print columns of the PYTD DataFrame
    print("PYTD DataFrame Columns:", pytd_df.columns)
    print("PYTD DataFrame:", pytd_df)

    # Merging YTD and PYTD DataFrames
    merged_df = pd.merge(ytd_df, pytd_df, on='Month', how='outer')

    # Debugging: Print merged DataFrame columns and data
    print("Merged DataFrame Columns:", merged_df.columns)
    print("Merged DataFrame:", merged_df)

    # If selected year is 2024, filter based on YTD data availability
    if selected_year == 2024:
        # Get the months that have YTD data
        months_with_data = merged_df[~merged_df[['YTD_Sales', 'YTD_Quantity', 'YTD_Gross_Profit']].isnull().all(axis=1)]['Month']
        merged_df = merged_df[merged_df['Month'].isin(months_with_data)]

    # Create metric labels
    ytd_metric_label = get_metric_label(selected_metric)
    pytd_metric_label = f'PYTD {ytd_metric_label}'

    # Create the line and stacked column chart
    figure = {
        'data': [
            {
                'x': merged_df['Month'],
                'y': merged_df.get(f'PYTD_{ytd_metric_label.replace(" ", "_")}', []),  # Using .get() to avoid KeyError
                'type': 'scatter',
                'mode': 'lines+markers',
                'name': pytd_metric_label,
                'yaxis': 'y2'
            },
            {
                'x': merged_df['Month'],
                'y': merged_df.get(f'YTD_{ytd_metric_label.replace(" ", "_")}', []),  # Using .get() to avoid KeyError
                'type': 'bar',
                'name': ytd_metric_label,
                'marker': {'color': 'blue'},
                'text': merged_df.get(f'YTD_{ytd_metric_label.replace(" ", "_")}', []).apply(lambda x: f"{x:,.2f}"),
                'textposition': 'outside'
            },
        ],
        'layout': {
            'title': f'{ytd_metric_label} & {pytd_metric_label} | Month',
            'xaxis': {
                'title': 'Month',
                'tickvals': list(range(1, 13)),
                'ticktext': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
            },
            'yaxis': {
                'title': ytd_metric_label,
                'side': 'left'
            },
            'yaxis2': {
                'title': pytd_metric_label,
                'overlaying': 'y',
                'side': 'right'
            },
        }
    }
    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
