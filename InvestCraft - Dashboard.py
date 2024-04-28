
import pkg_resources
import pip
installedPackages = {pkg.key for pkg in pkg_resources.working_set}
required = {'dash', 'dash-core-components', 'dash-html-components', 'dash-daq', 'cvxopt' }
missing = required - installedPackages


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash_daq as daq
from pickle import load
import cvxopt as opt
from cvxopt import blas, solvers

# ### Load the data of the investors/individuals

# df.head()
investors = pd.read_csv('InputData.csv', index_col = 0 )
investors.head(1)

# ### Load the market data and clean the data


assets = pd.read_csv('SP500Data.csv',index_col=0)
missing_fractions = assets.isnull().mean().sort_values(ascending=False)

missing_fractions.head(10)

drop_list = sorted(list(missing_fractions[missing_fractions > 0.3].index))

assets.drop(labels=drop_list, axis=1, inplace=True)
assets.shape
# Fill the missing values with the last value available in the dataset. 
assets=assets.fillna(method='ffill')
assets.head(2)


options=np.array(assets.columns)
# str(options)
options = []

for tic in assets.columns:
    #{'label': 'user sees', 'value': 'script sees'}
    mydict = {}
    mydict['label'] = tic #Apple Co. AAPL
    mydict['value'] = tic
    options.append(mydict)

# <a id='2'></a>
# ## 2. Code for the dashboard Interface


app = dash.Dash(__name__, external_stylesheets=['https://pcloud.codeestro.com/assets/css/tailwind.min.css'])


app.layout = html.Div([
    html.Div(className="bg-gray-100", children=[ 
        html.Section(className="flex flex-col md:flex-row h-screen items-center", children=[
            html.Div(className="bg-white w-full md:max-w-md lg:max-w-full md:mx-auto md:mx-0 md:w-1/2 xl:w-1/3 h-screen px-6 lg:px-16 xl:px-12 flex items-center justify-center", children=[
                html.Div(className="w-full h-100", children=[
                    html.H1(className="text-3xl md:text-4xl font-bold", children="InvestCraft - Dashboard"),
                    html.H2(className="text-2xl md:text-3xl font-bold leading-tight mt-12", children="Step 1: Enter Investor Characteristics"),
                    html.Div(className="mt-6", children=[
                        html.Div([
                            html.Label(className="block text-gray-700", children="Age:"),
                            dcc.Slider(
                                min=25,
                                max=70,
                                value=25,
                                className="w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none",
                                id="Age"
                            ),
                        ]),
                        html.Div([
                            html.Label(className="block text-gray-700", children="NetWorth:"),
                            dcc.Slider(
                                min=-1000000,
                                max=3000000,
                                value=10000,
                                marks={-1000000: '-₹1M', 0: '0', 500000: '₹500K', 1000000: '₹1M', 2000000: '₹2M'},
                                className="w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none",
                                id="Nwcat"
                            ),
                        ]),
                        html.Div([
                            html.Label(className="block text-gray-700", children="Income:"),
                            dcc.Slider(
                                min=-1000000,
                                max=3000000,
                                value=100000,
                                marks={-1000000: '-₹1M', 0: '0', 500000: '₹500K', 1000000: '₹1M', 2000000: '₹2M'},
                                className="w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none",
                                id="Inccl"
                            ),
                        ]),
                        html.Div([
                            html.Label(className="block text-gray-700", children="Education Level:"),
                            dcc.Slider(
                                min=1,
                                max=4,
                                value=2,
                                marks={1: 'No school', 2: 'High school', 3: 'College', 4: 'PHD'},
                                className="w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none",
                                id="Edu"
                            ),
                        ]),
                        html.Div([
                            html.Label(className="block text-gray-700", children="Married:"),
                            dcc.Slider(
                                min=1,
                                max=2,
                                value=1,
                                marks={1: 'Unmarried', 2: 'Married'},
                                className="w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none",
                                id="Married"
                            ),
                        ]),
                        html.Div([
                            html.Label(className="block text-gray-700", children="Kids:"),
                            dcc.Slider(
                                min=investors['KIDS07'].min(),
                                max=investors['KIDS07'].max(),
                                marks=[{'label': j, 'value': j} for j in investors['KIDS07'].unique()],
                                value=3,
                                className="w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none",
                                id="Kids"
                            ),
                        ]),
                        html.Div([
                            html.Label(className="block text-gray-700", children="Occupation:"),
                            dcc.Slider(
                                min=investors['OCCAT107'].min(),
                                max=investors['OCCAT107'].max(),
                                marks={1: 'Managerial', 2: 'Professional', 3: 'Sales', 4: 'Unemployed'},
                                value=3,
                                className="w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none",
                                id="Occ"
                            ),
                        ]),
                        html.Div([
                            html.Label(className="block text-gray-700", children="Willingness to take Risk:"),
                            dcc.Slider(
                                min=investors['RISK07'].min(),
                                max=investors['RISK07'].max(),
                                marks={1: 'Low', 2: 'Medium', 3: 'High', 4: 'Extreme'},
                                value=3,
                                className="w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none",
                                id="Risk"
                            ),
                        ]),
                        html.Button(
                            className="w-full block bg-blue-500 hover:bg-blue-400 focus:bg-blue-400 text-white font-semibold rounded-lg px-4 py-3 mt-6",
                            children="Calculate Risk Tolerance",
                            id="investor_char_button",
                            n_clicks=0
                        )
                    ])
                ])
            ]),
            html.Div(className="hidden lg:block w-full md:w-1/2 xl:w-2/3 h-screen", children=[
                html.Div(className="bg-white w-full md:max-w-md lg:max-w-full md:mx-auto h-screen px-6 lg:px-16 xl:px-12 flex items-center justify-center", children=[
                    html.Div(className="w-full h-100", children=[
                        html.H2(className="text-2xl md:text-3xl font-bold leading-tight mt-12", children="Step 2: Asset Allocation and Portfolio Performance"),
                        html.Div(className="mt-6", children=[
                            html.Div([
                                html.Label(className="block text-gray-700", children="Risk Tolerance (scale of 100):"),
                                dcc.Input(
                                    type="text",
                                    className="w-full px-4 py-3 rounded-lg bg-gray-200 mt-2 border focus:border-blue-500 focus:bg-white focus:outline-none",
                                    autoFocus=True,
                                    required=True,
                                    id="risk-tolerance-text",
                                    disabled=True
                                ),
                            ]),
                            html.Div([
                                html.Label(className="block text-gray-700", children="Select the assets for the portfolio:"),
                                dcc.Dropdown(
                                    id="ticker_symbol",
                                    options=options,
                                    value=['GOOGL', 'FB', 'LNT', 'IBM', 'AMZN', 'MSI'],
                                    multi=True,
                                    # style={'fontSize': 24, 'width': 75}
                                ),
                                html.Button(
                                    className="w-full block bg-blue-500 hover:bg-blue-400 focus:bg-blue-400 text-white font-semibold rounded-lg px-4 py-3 mt-6",
                                    children="Submit",
                                    id="submit-asset_alloc_button",
                                    n_clicks=0
                                )
                            ]),
                            html.Div([
                                dcc.Graph(
                                    id='Asset-Allocation',
                                    style={'width': '100%', 'height': '100%'}
                                ), 
                            ], style={'width': '50%', 'vertical-align': 'top', 'display': 'inline-block', \
                                      'font-family': 'calibri', 'horizontal-align': 'right'}),
                            html.Div([
                                dcc.Graph(
                                    id='Performance',
                                    style={'width': '100%', 'height': '100%'}
                                )
                            ], style={'width': '50%', 'vertical-align': 'top', 'display': 'inline-block', \
                                      'font-family': 'calibri', 'horizontal-align': 'right'})
                        ])
                    ])
                ])
            ])
        ])
    ])
])
    

# <a id='3'></a>
# ## 3. Code for the underlying functions within the interface
# 
# The steps performed are as follows: 
# 
# 1) Loading the regression model for predicting risk tolerance
# 
# 2) Using markovitz mean variance analysis for asset allocation
# 
# 3) Producing chart for the asset allocation and portfolio performance
# 
# #### Click the url produced by this code to see the dashboard


def predict_riskTolerance(X_input):

    filename = 'finalized_model.sav'
    loaded_model = load(open(filename, 'rb'))
    # estimate accuracy on validation set
    predictions = loaded_model.predict(X_input)
    return predictions

#Asset allocation given the Return, variance
def get_asset_allocation(riskTolerance,stock_ticker):
    #ipdb.set_trace()
    assets_selected = assets.loc[:,stock_ticker]
    return_vec = np.array(assets_selected.pct_change().dropna(axis=0)).T
    n = len(return_vec)
    returns = np.asmatrix(return_vec)
    mus = 1-riskTolerance
    
    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(return_vec))
    pbar = opt.matrix(np.mean(return_vec, axis=1))
    # Create constraint matrices
    G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
    h = opt.matrix(0.0, (n ,1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)
    # Calculate efficient frontier weights using quadratic programming
    portfolios = solvers.qp(mus*S, -pbar, G, h, A, b)
    w=portfolios['x'].T
    print (w)
    Alloc =  pd.DataFrame(data = np.array(portfolios['x']),index = assets_selected.columns)

    # Calculate efficient frontier weights using quadratic programming
    portfolios = solvers.qp(mus*S, -pbar, G, h, A, b)
    returns_final=(np.array(assets_selected) * np.array(w))
    returns_sum = np.sum(returns_final,axis =1)
    returns_sum_pd = pd.DataFrame(returns_sum, index = assets.index )
    returns_sum_pd = returns_sum_pd - returns_sum_pd.iloc[0,:] + 100   
    return Alloc,returns_sum_pd



#Callback for the graph
#This function takes all the inputs and computes the cluster and the risk tolerance


@app.callback(
     [Output('risk-tolerance-text', 'value')],
    [Input('investor_char_button', 'n_clicks'),
    Input('Age', 'value'),Input('Nwcat', 'value'),
    Input('Inccl', 'value'), Input('Risk', 'value'),
    Input('Edu', 'value'),Input('Married', 'value'),
    Input('Kids', 'value'),Input('Occ', 'value')])
#get the x and y axis details 

def update_risk_tolerance(n_clicks,Age,Nwcat,Inccl,Risk,Edu,Married,Kids,Occ):
      
    #ipdb.set_trace()
    
    RiskTolerance = 0
    if n_clicks != None:    
        X_input = [[Age,Edu,Married,Kids,Occ,Inccl, Risk,Nwcat]]
        RiskTolerance= predict_riskTolerance(X_input)
    #print(RiskAversion)
    #Using linear regression to get the risk tolerance within the cluster.    
    return list([round(float(RiskTolerance*100),2)])

@app.callback([Output('Asset-Allocation', 'figure'),
              Output('Performance', 'figure')],
            [Input('submit-asset_alloc_button', 'n_clicks'),
            Input('risk-tolerance-text', 'value')], 
            [State('ticker_symbol', 'value')
            ])
def update_asset_allocationChart(n_clicks, risk_tolerance, stock_ticker):
    
    Allocated, InvestmentReturn = get_asset_allocation(risk_tolerance,stock_ticker)  
    
    return [{'data' : [go.Bar(
                        x=Allocated.index,
                        y=Allocated.iloc[:,0],
                        marker=dict(color='red'),
                    ),
                    ],
            'layout': {'title':" Asset allocation - Mean-Variance Allocation"}

       },
            {'data' : [go.Scatter(
                        x=InvestmentReturn.index,
                        y=InvestmentReturn.iloc[:,0],
                        name = 'OEE (%)',
                        marker=dict(color='red'),
                    ),
                    ],
            'layout': {'title':"Portfolio value of ₹100 investment"}

       }]

if __name__ == '__main__':
    app.run_server()