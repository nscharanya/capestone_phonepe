import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import requests
import json
from PIL import Image

# DataFrame Creation
mydb = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                password = "Charanya@09",
                                database = "phonepe_data",
                                port = 5432
                                )
cursor = mydb.cursor()

# aggregated_insurance_df
cursor.execute("select* from aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()

Aggregated_insurance = pd.DataFrame(table1, columns = ("States","Years","Quarters","Transaction_type","Transaction_count","Transaction_amount"))

# aggregated_transaction_df
cursor.execute("select* from aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()

Aggregated_transaction = pd.DataFrame(table2, columns = ("States","Years","Quarters","Transaction_type","Transaction_count","Transaction_amount"))

# aggregated_user_df
cursor.execute("select* from aggregated_user")
mydb.commit()
table3 = cursor.fetchall()

Aggregated_user = pd.DataFrame(table3, columns = ("States","Years","Quarters","Brands","Transaction_count","Percentage"))

# map_insurance_df
cursor.execute("select* from map_insurance")
mydb.commit()
table4 = cursor.fetchall()

Map_insurance = pd.DataFrame(table4, columns = ("States","Years","Quarters","Districts","Transaction_count","Transaction_amount"))

# map_transaction_df
cursor.execute("select* from map_transaction")
mydb.commit()
table5 = cursor.fetchall()

Map_transaction = pd.DataFrame(table5, columns = ("States","Years","Quarters","Districts","Transaction_count","Transaction_amount"))

# map_user_df
cursor.execute("select* from map_user")
mydb.commit()
table6 = cursor.fetchall()

Map_user = pd.DataFrame(table6, columns = ("States","Years","Quarters","Districts","RegisteredUsers","AppOpens"))

# top_insurance_df
cursor.execute("select* from top_insurance")
mydb.commit()
table7 = cursor.fetchall()

Top_insurance = pd.DataFrame(table7, columns = ("States","Years","Quarters","Pincodes","Transaction_count","Transaction_amount"))

# top_transaction_df
cursor.execute("select* from top_transaction")
mydb.commit()
table8 = cursor.fetchall()

Top_transaction = pd.DataFrame(table8, columns = ("States","Years","Quarters","Pincodes","Transaction_count","Transaction_amount"))

# top_user_df
cursor.execute("select* from top_user")
mydb.commit()
table9 = cursor.fetchall()

Top_user = pd.DataFrame(table9, columns = ("States","Years","Quarters","Pincodes","RegisteredUsers"))


# Aggregated_Insurance, Transaction Year_wise data
def Aggre_tran_co_am_ye(df, year):
    tramcoye = df[df["Years"] == year]  # Returns a new df where year = 2021
    tramcoye.reset_index(drop=True, inplace=True)  # Drops old index and Resets index for this particular df
    tramcoyegr = tramcoye.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()  # Returns sum of Transaction_count for each state
    tramcoyegr.reset_index(inplace=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig_amount = px.scatter(tramcoyegr, x="States", y="Transaction_amount", color="States", symbol="States",
                                title=f"{year} TRANSACTION AMOUNT", opacity=0.8, size="Transaction_amount",
                                size_max=40, height=650, width=600)
        st.plotly_chart(fig_amount)  # To show the charts in the streamlit page itself
    with col2:
        fig_count = px.scatter(tramcoyegr, x="States", y="Transaction_count", color="States", symbol="States",
                               title=f"{year} TRANSACTION COUNT", opacity=0.8, size="Transaction_count",
                               size_max=40, height=650, width=600 )
        st.plotly_chart(fig_count)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_names = []
    for feature in data1["features"]:
        state_names.append((feature['properties']['ST_NM']))
    state_names.sort()

    col1, col2 = st.columns([3, 2])

    with col1:
        fig_india_1 = px.choropleth(tramcoyegr, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale = "Spectral",
                                    range_color = (tramcoyegr["Transaction_amount"].min(), tramcoyegr["Transaction_amount"].max()), # Based upon the values present in the dataframe the color range varies
                                    hover_name = "States", title = f"{year} TRANSACTION AMOUNT", fitbounds = "locations",
                                    height = 650, width = 600)
        fig_india_1.update_geos(visible = False)  # to remove background world lines present around india
        st.plotly_chart(fig_india_1)
    
    with col2:

        fig_india_2 = px.choropleth(tramcoyegr, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color = "Transaction_count", color_continuous_scale = "Spectral",
                                    range_color = (tramcoyegr["Transaction_count"].min(), tramcoyegr["Transaction_count"].max()), # Based upon the values present in the dataframe the color range varies
                                    hover_name = "States", title = f"{year} TRANSACTION COUNT", fitbounds = "locations",
                                    height = 650, width = 600)
        fig_india_2.update_geos(visible = False)  # to remove background world lines present around india
        st.plotly_chart(fig_india_2)
    return tramcoye

# Aggregated_Insurance Quarter_wise data
def Aggre_tran_co_am_ye_quar(df, quarter):
    tramcoye = df[df["Quarters"] == quarter]  # Returns a new df where year = 2021
    tramcoye.reset_index(drop = True, inplace = True)       # Drops old index and Resets index for this particular df
    tramcoyegr = tramcoye.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()  # Returns sum of Transaction_count for each state
    tramcoyegr.reset_index(inplace = True)
    col1, col2 = st.columns([3,2])
    with col1:
        fig_amount = px.scatter(tramcoyegr, x="States", y="Transaction_amount", title=f"{tramcoye['Years'].min()} Year, Quarter- {quarter} TRANSACTION AMOUNT",
                                color="Transaction_amount", color_continuous_scale="Spectral", hover_name="States",
                                height=650, width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.scatter(tramcoyegr, x="States", y="Transaction_count", title=f"{tramcoye['Years'].min()} Year, Quarter- {quarter}  TRANSACTION COUNT",
                               color="Transaction_count", color_continuous_scale="Rainbow", hover_name="States",
                               height=650, width=600)
        st.plotly_chart(fig_count)


    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_names = []
    for feature in data1["features"]:
        state_names.append((feature['properties']['ST_NM']))

    state_names.sort()

    col1, col2 = st.columns([3,2])
    with col1:
        fig_india_1 = px.choropleth(tramcoyegr, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color = "Transaction_amount", color_continuous_scale = "Spectral",
                                    range_color = (tramcoyegr["Transaction_amount"].min(), tramcoyegr["Transaction_amount"].max()), # Based upon the values present in the dataframe the color range varies
                                    hover_name = "States", title = f"{tramcoye['Years'].min()} Year, Quarter- {quarter} TRANSACTION AMOUNT", fitbounds = "locations",
                                    height = 650, width = 600)
        fig_india_1.update_geos(visible = False)  # to remove background world lines present around india
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2 = px.choropleth(tramcoyegr, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color = "Transaction_count", color_continuous_scale = "Spectral",
                                    range_color = (tramcoyegr["Transaction_count"].min(), tramcoyegr["Transaction_count"].max()), # Based upon the values present in the dataframe the color range varies
                                    hover_name = "States", title = f"{tramcoye['Years'].min()} Year, Quarter- {quarter} TRANSACTION COUNT", fitbounds = "locations",
                                    height = 650, width = 600)
        fig_india_2.update_geos(visible = False)  # to remove background world lines present around india
        st.plotly_chart(fig_india_2)
    return tramcoye

# Aggregated_transaction data and visualizations based on States 
def Aggre_transaction_tran_co_am_ye_st(df, state):
    tramcoye = df[df["States"] == state]  
    tramcoye.reset_index(drop=True, inplace=True) 
    tramcoyegr = tramcoye.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()  
    tramcoyegr.reset_index(inplace=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        fig_sunburst_1 = px.sunburst(data_frame=tramcoyegr, path=["Transaction_type"], values="Transaction_amount",
                                     title=f"TRANSACTION AMOUNT OF {state.upper()}", color="Transaction_type",
                                     color_discrete_map={"Financial Services": "blue",
                                                        "Merchant payments": "orange",
                                                        "Others": "red",
                                                        "Peer-to-peer payments": "green",
                                                        "Recharge & bill payments": "yellow"},
                                     width=600, height=600)
        st.plotly_chart(fig_sunburst_1)

    with col2:
        fig_sunburst_2 = px.sunburst(data_frame=tramcoyegr, path=["Transaction_type"], values="Transaction_count",
                                     title=f"TRANSACTION COUNT OF {state.upper()}", color="Transaction_type",
                                     color_discrete_map={"Financial Services": "blue",
                                                         "Merchant payments": "orange",
                                                         "Others": "red",
                                                         "Peer-to-peer payments": "green",
                                                         "Recharge & bill payments": "yellow"},
                                     width=600, height=600)
        st.plotly_chart(fig_sunburst_2)

# Aggregated_user data and visualizations based on Brands (Years)
def Aggre_user_br_tran_count_ye(df, year):
    aggusye = df[df["Years"]== year]
    aggusye.reset_index(drop = True, inplace = True) 

    aggusyegr = pd.DataFrame(aggusye.groupby("Brands")["Transaction_count"].sum()) # grouping Transaction_count and Percentage based on Brands
    aggusyegr.reset_index(inplace = True) 

    fig_bar_1 = px.bar(aggusyegr, x = "Brands", y = "Transaction_count", title = f"TRANSACTION COUNT BASED ON BRANDS OF YEAR {year}",
                    width = 1000, color_discrete_sequence = px.colors.sequential.Plasma, hover_name = "Brands")
    st.plotly_chart(fig_bar_1)

    return aggusye
    
# Aggregated_user data and visualizations based on Brands (Quarters)
def Aggre_user_br_tran_count_ye_qu(df, quarter):
    aggusyequ = df[df["Quarters"]== quarter]
    aggusyequ.reset_index(drop = True, inplace = True) 

    aggusyequgr = pd.DataFrame(aggusyequ.groupby("Brands")["Transaction_count"].sum())
    aggusyequgr.reset_index(inplace = True)

    fig_bar_1 = px.bar(aggusyequgr, x = "Brands", y = "Transaction_count", title = f"TRANSACTION COUNT BASED ON BRANDS OF {df['Years'].min()} - QUARTER-{quarter}",
                        width = 1000, color_discrete_sequence = px.colors.sequential.Turbo)
    st.plotly_chart(fig_bar_1)
    
    return aggusyequ

# Aggregated_user data and visualizations based on Brands (Quarters, States)
def Aggre_user_br_tran_count_ye_qu_st(df, state):
    aggusyequst = df[df["States"] == state]
    aggusyequst.reset_index(drop = True, inplace = True)

    fig_line_1 = px.line(aggusyequst, x = "Brands", y = "Transaction_count", hover_data = "Percentage",
                        title = f"{state.upper()}'s TRANSACTION COUNT AND PERCENTAGE BASED ON BRANDS", width = 1000)
    st.plotly_chart(fig_line_1)


# Map_insurance data and visualizations based on Districts 
def Map_insurance_tran_co_am_ye_st_dist(df, state):
    tramcoye = df[df["States"] == state]
    tramcoye.reset_index(drop=True, inplace=True) 
    tramcoyegr = tramcoye.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    tramcoyegr.reset_index(inplace=True)
    fig_treemap_amount = px.treemap(tramcoyegr,
                                    path=["Districts"],  # Specify the hierarchy levels
                                    values="Transaction_amount",  # Size of each rectangle based on transaction amount
                                    title=f"{state.upper()} DISTRICT-WISE TRANSACTION AMOUNT",
                                    color="Transaction_amount",  # Color of rectangles based on transaction amount
                                    color_continuous_scale="Viridis",  # Gradient color scheme
                    
                                    labels={"Transaction_amount": "Transaction Amount"})
    st.plotly_chart(fig_treemap_amount, use_container_width=True)
    # Treemap chart for transaction count
    fig_treemap_count = px.treemap(tramcoyegr,
                                    path=["Districts"],  # Specify the hierarchy levels
                                    values="Transaction_count",  # Size of each rectangle based on transaction count
                                    title=f"{state.upper()} DISTRICT-WISE TRANSACTION COUNT",
                                    color="Transaction_count",  # Color of rectangles based on transaction count
                                    color_continuous_scale="Viridis",  # Gradient color scheme
                                    
                                    labels={"Transaction_count": "Transaction Count"})
    st.plotly_chart(fig_treemap_count, use_container_width=True)

# Map_user data and visualizations based on Registered_Users and App_Opens (Year, States)
def map_user_ru_apop_ye_st(df, year):
    mapusye = df[df["Years"] == year]
    mapusye.reset_index(drop=True, inplace=True) 
    mapusyegr = pd.DataFrame(mapusye.groupby("States")[["RegisteredUsers", "AppOpens"]].sum())
    mapusyegr.reset_index(inplace=True) 

    fig_area = px.area(mapusyegr, x="States", y=["RegisteredUsers", "AppOpens"],
                       title=f"REGISTERED_USERS AND APP_OPENS OF YEAR {year}", 
                       width=850, height=800, color_discrete_sequence=px.colors.sequential.Plasma)
    st.plotly_chart(fig_area)

    return mapusye

# Map_user data and visualizations based on Registered_Users and App_Opens (Year, States)
def map_user_ru_apop_ye_qu_st(df, quarter):
    mapusyequ = df[df["Quarters"] == quarter]
    mapusyequ.reset_index(drop=True, inplace=True) 
    mapusyequgr = pd.DataFrame(mapusyequ.groupby("States")[["RegisteredUsers", "AppOpens"]].sum())
    mapusyequgr.reset_index(inplace=True) 

    fig_area = px.area(mapusyequgr, x="States", y=["RegisteredUsers", "AppOpens"],
                       title=f"REGISTERED_USERS AND APP_OPENS OF {df['Years'].min()} - QUARTER {quarter}",
                       width=850, height=800, color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_area)

    return mapusyequ

# Map_user data and visualizations based on Registered_Users and App_Opens (States)
def map_user_ru_apop_st(df, state):
    Map_usyequst = Map_usyequ[Map_usyequ["States"]== "Andaman & Nicobar"]
    Map_usyequst.reset_index(drop = True, inplace = True) 
    
    fig_map_user_bar_1 = px.bar(Map_usyequst, x = "RegisteredUsers", y = "Districts", orientation = "h",
                                title = "REGISTERED_USERS BASED ON DISTRICTS", height = 800, 
                                color_discrete_sequence = px.colors.sequential.GnBu_r)
    st.plotly_chart(fig_map_user_bar_1)

    fig_map_user_bar_2 = px.bar(Map_usyequst, x = "AppOpens", y = "Districts", orientation = "h",
                                title = "APP_OPENS BASED ON DISTRICTS", height = 800, 
                                color_discrete_sequence = px.colors.sequential.Redor_r)
    st.plotly_chart(fig_map_user_bar_2)

# Transaction_insurance data and visualizations based on Transaction_amount, Quarters & Pincodes (States)
def top_insu_pintramyequst(df, states):
    Topinsu_yest = df[df["States"]== states]
    Topinsu_yest.reset_index(drop=True, inplace=True) 

    col1, col2 = st.columns([3, 2])
    with col1:
        fig_top_insu_area = px.area(Topinsu_yest, x="Quarters", y="Transaction_count", color="Pincodes",
                                    title="TRANSACTION COUNT AREA PLOT", height=650, width=600,
                                    hover_data=["Transaction_count", "Pincodes"])
        st.plotly_chart(fig_top_insu_area)
    
    with col2:
        fig_top_insu_area = px.area(Topinsu_yest, x="Quarters", y="Transaction_amount", color="Pincodes",
                                    title="TRANSACTION AMOUNT AREA PLOT", height=650, width=600,
                                    hover_data=["Transaction_amount", "Pincodes"])
        st.plotly_chart(fig_top_insu_area)

def top_user_ru_ye (df, year):
    topusye = df[df["Years"]== year]
    topusye.reset_index(drop = True, inplace = True) 

    topusyegr = pd.DataFrame(topusye.groupby(["States", "Quarters"])["RegisteredUsers"].sum()) # grouping Transaction_count and Percentage based on Brands
    topusyegr.reset_index(inplace = True) 

    fig_top_bar_plot_1 = px.bar(topusyegr, x = "States", y = "RegisteredUsers", width = 1000, height = 800,
                                color = "Quarters", color_discrete_sequence = px.colors.sequential.Brwnyl,
                                hover_name = "States", title = f"{year} REGISTERED USERS BASED ON STATES")
    st.plotly_chart(fig_top_bar_plot_1)

    return topusye   

# Top_user data and visualizations based on Registered_users and  States 
def top_user_ru_ye_st (df, states):
    Topusruyest = df[df["States"]== states]
    Topusruyest.reset_index(drop = True, inplace = True) 

    fig_top_bar_plot_2 = px.bar(Topusruyest, x = "Quarters", y = "RegisteredUsers", 
                                title = "REGISTERED USERS AND PINCODES BASED ON STATES AND QUARTERS", width = 1000,
                                height = 800, hover_data = "Pincodes", color="RegisteredUsers", color_continuous_scale="magenta")
    st.plotly_chart(fig_top_bar_plot_2)

def top_chart_transaction_amount(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Charanya@09",
                            database="phonepe_data",
                            port=5432)
    cursor = mydb.cursor()

    # Plot 1: Line Plot
    query1 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()
    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_amount"))
    col1, col2 = st.columns([3,2])
    with col1:
        fig_amount_1 = px.line(df_1, x="states", y="transaction_amount", title="Top 10 Transaction Amounts",
                               hover_name="states", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_amount_1)

    # Plot 2: Scatter Plot
    query2 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount 
                LIMIT 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_amount"))
    with col2:
        fig_amount_2 = px.scatter(df_2, x="states", y="transaction_amount", title="Last 10 Transaction Amounts",
                                  hover_name="states", color="states", height=500)
        st.plotly_chart(fig_amount_2)

    # Plot 3: Bar Plot
    query3 = f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()
    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3 = px.bar(df_3, y="states", x="transaction_amount", title="Average Transaction Amount",
                              hover_name="states", orientation="h", color_discrete_sequence=px.colors.qualitative.Bold,
                              height = 800, width = 1000)
    st.plotly_chart(fig_amount_3)

def top_chart_transaction_count(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Charanya@09",
                            database="phonepe_data",
                            port=5432)
    cursor = mydb.cursor()

    # Plot 1: Line Plot
    query1 = f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()
    df_1 = pd.DataFrame(table_1, columns=("states", "transaction_count"))
    col1, col2= st.columns([3,2])
    with col1:
        fig_line_1 = px.line(df_1, x="states", y="transaction_count", title="Top 10 Transaction Counts (Line Plot)",
                             hover_name="states", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_line_1)

    # Plot 2: Scatter Plot
    query2 = f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    df_2 = pd.DataFrame(table_2, columns=("states", "transaction_count"))
    with col2:
        fig_scatter_2 = px.scatter(df_2, x="states", y="transaction_count", title="Last 10 Transaction Counts (Scatter Plot)",
                                   hover_name="states", color="states", height = 800, width = 1000)
        st.plotly_chart(fig_scatter_2)

    # Plot 3: Bar Chart
    query3 = f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()
    df_3 = pd.DataFrame(table_3, columns=("states", "transaction_count"))
    fig_amount_3 = px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT",
                          hover_name="states", orientation="h", color_discrete_sequence=px.colors.sequential.Bluyl_r,
                          height=800, width=1000)
    st.plotly_chart(fig_amount_3)


def top_chart_registered_user(table_name, state):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Charanya@09",
                            database="phonepe_data",
                            port=5432)
    cursor = mydb.cursor()

    # Plot 1: Line Plot
    query1 = f'''SELECT districts, SUM(registeredusers) AS registered_user
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY registered_user DESC
                 LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()
    df_1 = pd.DataFrame(table_1, columns=("districts", "registeredusers"))

    col1, col2 = st.columns([3,2])
    with col1:
        fig_line_1 = px.line(df_1, x="districts", y="registeredusers", title="Top 10 Registered Users (Line Plot)",
                             hover_name="districts", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_line_1)

    # Plot 2: Scatter Plot
    query2 = f'''SELECT districts, SUM(registeredusers) AS registered_user
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY registered_user
                 LIMIT 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    df_2 = pd.DataFrame(table_2, columns=("districts", "registeredusers"))
    with col2:
        fig_scatter_2 = px.scatter(df_2, x="districts", y="registeredusers",
                                   title="Last 10 Registered Users (Scatter Plot)", hover_name="districts",
                                   color_discrete_sequence=px.colors.qualitative.Pastel2)
        st.plotly_chart(fig_scatter_2)

    # Plot 3: Bar Chart
    query3 = f'''SELECT districts, AVG(registeredusers) AS registered_user
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY registered_user;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()
    df_3 = pd.DataFrame(table_3, columns=("districts", "registeredusers"))
    
    fig_bar_3 = px.bar(df_3, y="districts", x="registeredusers",
                        title="Average Registered Users (Bar Chart)", hover_name="districts",
                        color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig_bar_3)

def top_chart_app_opens(table_name, state):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Charanya@09",
                            database="phonepe_data",
                            port=5432)
    cursor = mydb.cursor()

    # Plot 1: Line Plot
    query1 = f'''SELECT districts, SUM(appopens) AS appopens
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY appopens DESC
                 LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()
    df_1 = pd.DataFrame(table_1, columns=("districts", "appopens"))
    col1, col2 = st.columns([3,2])
    with col1:
        fig_line_1 = px.line(df_1, x="districts", y="appopens", title="Top 10 App Opens (Line Plot)",
                             hover_name="districts", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_line_1)

    # Plot 2: Scatter Plot
    query2 = f'''SELECT districts, SUM(appopens) AS appopens
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY appopens
                 LIMIT 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    df_2 = pd.DataFrame(table_2, columns=("districts", "appopens"))
    with col2:
        fig_scatter_2 = px.scatter(df_2, x="districts", y="appopens",
                                   title="Last 10 App Opens (Scatter Plot)", hover_name="districts",
                                   color_discrete_sequence=px.colors.qualitative.Pastel2)
        st.plotly_chart(fig_scatter_2)

    # Plot 3: Area Plot
    query3 = f'''SELECT districts, AVG(appopens) AS appopens
                 FROM {table_name}
                 WHERE states = '{state}'
                 GROUP BY districts
                 ORDER BY appopens;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()
    df_3 = pd.DataFrame(table_3, columns=("districts", "appopens"))
    
    fig_area_3 = px.area(df_3, x="districts", y="appopens",
                            title="Average App Opens (Area Plot)", hover_name="districts",
                            color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig_area_3)


def top_chart_registered_users(table_name):
    mydb = psycopg2.connect(host="localhost",
                            user="postgres",
                            password="Charanya@09",
                            database="phonepe_data",
                            port=5432)
    cursor = mydb.cursor()

    # plot_1: Bar chart
    query1 = f'''select states, sum(registeredusers) as registered_users
                 from {table_name}
                 group by states
                 order by registered_users desc
                 limit 10; '''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()
    df_1 = pd.DataFrame(table_1, columns=("states", "registeredusers"))
    col1, col2 = st.columns([3, 2])
    with col1:
        fig_amount_1 = px.bar(df_1, x="states", y="registeredusers", title="TOP 10 OF REGISTERED USERS", hover_name="states",
                              color_discrete_sequence=px.colors.sequential.Cividis, height=650, width=600)
        st.plotly_chart(fig_amount_1)

    # plot_2: Line chart (replacing one bar chart)
    query2 = f'''select states, sum(registeredusers) as registered_users
                 from {table_name}
                 group by states
                 order by registered_users
                 limit 10; '''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()
    df_2 = pd.DataFrame(table_2, columns=("states", "registeredusers"))
    with col2:
        fig_amount_2 = px.line(df_2, x="states", y="registeredusers", title="LAST 10 OF REGISTERED USERS", hover_name="states",
                               color_discrete_sequence=px.colors.sequential.Plasma_r, height=650, width=600)
        st.plotly_chart(fig_amount_2)

    # plot_3: Bar chart (Average of registered users)
    query3 = f'''select states, avg(registeredusers) as registered_users
                 from {table_name}
                 group by states
                 order by registered_users; '''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()
    df_3 = pd.DataFrame(table_3, columns=("states", "registeredusers"))
    fig_amount_3 = px.bar(df_3, y="states", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name="states", orientation="h",
                          color_discrete_sequence=px.colors.sequential.Bluyl_r, height=800, width=1000)
    st.plotly_chart(fig_amount_3)

# streamlit part

# Set page layout to wide
st.set_page_config(layout="wide")

# Sidebar navigation
with st.sidebar:
    st.title("Main Menu")
    select = st.selectbox("Select Option", ["HOME", "DATA EXPLORATION", "TOP CHARTS"])

# Main content

if select == "HOME":
    st.title("Welcome to PhonePe")
    st.markdown("India's Best Transaction App")
    st.image(Image.open("PhonePe_Logo.jpg"), use_column_width=True)

    st.header("Key Features")
    st.markdown(
        """
        - **Link Credit/Debit Cards**: Securely link your cards for seamless transactions.
        - **Check Bank Balance**: Easily monitor your bank balance within the app.
        - **Secure PIN Authorization**: Keep your transactions secure with PIN authorization.
        - **Instant Money Transfer**: Send and receive money instantly.
        """
    )
    st.markdown("Make your transactions hassle-free with PhonePe!")
    st.markdown("[Download the App Now](https://www.phonepe.com/app-download/)", unsafe_allow_html=True)

    st.header("Why Choose PhonePe?")
    st.markdown(
        """
        - **Easy Transactions**: Conveniently make payments and transfers.
        - **All-in-One App**: Manage all your payments in one place.
        - **No Wallet Top-Up Required**: Direct bank-to-bank transactions.
        - **Multiple Payment Modes**: Choose from various payment options.
        - **PhonePe Merchants**: Enjoy exclusive deals with PhonePe partners.
        - **Earn Great Rewards**: Get rewarded for every transaction.
        """
    )
    st.image(Image.open("phonepe.jpg"), use_column_width=True)

elif select == "DATA EXPLORATION":
    st.write("-----------------------------------------")
    st.title("DATA EXPLORATION")
    st.write("-----------------------------------------")
    with st.sidebar:
    # Add tabs for different data exploration methods
        options = ["Aggregated Analysis", "Map Analysis", "Top Analysis"]
        option_selected = st.selectbox("Select Option", options)
        st.write("You selected:", option_selected) 

    if option_selected == "Aggregated Analysis":   
        st.header("Aggregated Analysis")
        with st.sidebar:
            method_1 = st.radio("Select The Method", ["Aggregated Insurance", "Aggregated Transaction", "Aggregated User"])
    
        if method_1 == "Aggregated Insurance":
            st.write("You selected Aggregated Insurance")

            col1, col2 = st.columns([3,2])

            with col1:
                years = st.selectbox("Select the Year", Aggregated_insurance["Years"].unique())
                #years = st.slider("Select the Year", Aggregated_insurance["Years"].min(),Aggregated_insurance["Years"].max(), Aggregated_insurance["Years"].min())
                # Storing the df returned by transaction_count_amount_year function in Agg_insu_tramcoye variable
            Agg_insu_tramcoye = Aggre_tran_co_am_ye(Aggregated_insurance, years)

            col1, col2 = st.columns([3,2])

            with col1:
                # Select quarter from the Agg_insu_tramcoye df which will have only the selected year
                quarters = st.selectbox("Select the Quarter", sorted(Aggregated_insurance["Quarters"].unique()))
            Aggre_tran_co_am_ye_quar(Agg_insu_tramcoye, quarters)

        elif method_1 == "Aggregated Transaction":
                
            col1, col2 = st.columns([3,2])

            with col1:
                years = st.selectbox("Select the Year", Aggregated_transaction["Years"].unique())
                # Storing the df returned by transaction_count_amount_year function in Agg_tran_tramcoye variable
            Agg_tran_tramcoye = Aggre_tran_co_am_ye(Aggregated_transaction, years)
                
            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select the State", Agg_tran_tramcoye["States"].unique())
            Aggre_transaction_tran_co_am_ye_st(Agg_tran_tramcoye, states)

            col1, col2 = st.columns([3,2])
            with col1:
                quarters = st.selectbox("Select the Quarter", sorted(Agg_tran_tramcoye["Quarters"].unique()))
            Agg_tran_tramcoye_qu = Aggre_tran_co_am_ye_quar(Agg_tran_tramcoye, quarters)

            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select the State for View", Agg_tran_tramcoye["States"].unique())
            Aggre_transaction_tran_co_am_ye_st(Agg_tran_tramcoye_qu, states)

        elif method_1 == "Aggregated User":
            col1, col2 = st.columns([3,2])

            with col1:
                years = st.selectbox("Select the Year", Aggregated_user["Years"].unique())
                # Storing the df returned by transaction_count_amount_year function in Agg_tran_tramcoye variable
            Agg_user_brtrcoye = Aggre_user_br_tran_count_ye(Aggregated_user, years)

            col1, col2 = st.columns([3,2])
            with col1:
                quarters = st.selectbox("Select the Quarter", sorted(Agg_user_brtrcoye["Quarters"].unique()))
            Agg_user_brtrcoyequ = Aggre_user_br_tran_count_ye_qu(Agg_user_brtrcoye, quarters)

            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select the State", Agg_user_brtrcoyequ["States"].unique())
            Aggre_user_br_tran_count_ye_qu_st(Agg_user_brtrcoyequ, states)
    
    elif option_selected == "Map Analysis": 
        st.header("Map Analysis")
        with st.sidebar:
            method_2 = st.radio("Select The Method", ["Map Insurance","Map Transaction","Map User"])
        if method_2 == "Map Insurance":

            col1, col2 = st.columns([3,2])

            with col1:
                years = st.selectbox("Select the Year", Map_insurance["Years"].unique())
            # Storing the df returned by transaction_count_amount_year function in Agg_tran_tramcoye variable
            Map_insu_tramcoye = Aggre_tran_co_am_ye(Map_insurance, years)   

            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select the State", Map_insu_tramcoye["States"].unique())
            Map_insurance_tran_co_am_ye_st_dist(Map_insu_tramcoye, states)

            col1, col2 = st.columns([3,2])
            with col1:
                quarters = st.selectbox("Select the Quarter", sorted(Map_insu_tramcoye["Quarters"].unique()))
            Map_insu_tramcoye_qu = Aggre_tran_co_am_ye_quar(Map_insu_tramcoye, quarters)

            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select the State", Map_insu_tramcoye_qu["States"].unique())
            Map_insurance_tran_co_am_ye_st_dist(Map_insu_tramcoye_qu, states)


        elif method_2 == "Map Transaction":

            col1, col2 = st.columns([3,2])

            with col1:
                years = st.selectbox("Select the Year", Map_transaction["Years"].unique())
            # Storing the df returned by transaction_count_amount_year function in Agg_tran_tramcoye variable
            Map_tran_tramcoye = Aggre_tran_co_am_ye(Map_transaction, years)   

            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select the State", Map_tran_tramcoye["States"].unique())
            Map_insurance_tran_co_am_ye_st_dist(Map_tran_tramcoye, states)

            col1, col2 = st.columns([3,2])
            with col1:
                quarters = st.selectbox("Select the Quarter", sorted(Map_tran_tramcoye["Quarters"].unique()))
            Map_tran_tramcoye_qu = Aggre_tran_co_am_ye_quar(Map_tran_tramcoye, quarters)

            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select one State", Map_tran_tramcoye_qu["States"].unique())
            Map_insurance_tran_co_am_ye_st_dist(Map_tran_tramcoye_qu, states)

        elif method_2 == "Map User":
            col1, col2 = st.columns([3,2])

            with col1:
                years = st.selectbox("Select the Year", Map_user["Years"].unique())
            # Storing the df returned by transaction_count_amount_year function in Agg_tran_tramcoye variable
            Map_usye = map_user_ru_apop_ye_st(Map_user, years)   

            col1, col2 = st.columns([3,2])
            with col1:
                quarters = st.selectbox("Select the Quarter", sorted(Map_usye["Quarters"].unique()))
            Map_usyequ = map_user_ru_apop_ye_qu_st(Map_usye, quarters)

            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select the State", Map_usyequ["States"].unique())
            map_user_ru_apop_st(Map_usyequ, states)



    
    elif option_selected == "Top Analysis":
        st.header("Top Analysis")
        with st.sidebar:
            method_3 = st.radio("Select The Method",["Top Insurance","Top Transaction","Top User"])    # selectbox
        if method_3 == "Top Insurance":
            col1, col2 = st.columns([3,2])

            with col1:
                years = st.selectbox("Select the Year", Top_insurance["Years"].unique())
            # Storing the df returned by transaction_count_amount_year function in Agg_tran_tramcoye variable
            Top_insu_tramcoye = Aggre_tran_co_am_ye(Top_insurance, years)   

            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select the State for Viewing the Charts", Top_insu_tramcoye["States"].unique())
            top_insu_pintramyequst(Top_insu_tramcoye, states)

            col1, col2 = st.columns([3,2])
            with col1:
                quarters = st.slider("Select the Quarter for Viewing the Charts", Top_insu_tramcoye["Quarters"].min(), Top_insu_tramcoye["Quarters"].max(), Top_insu_tramcoye["Quarters"].min())
            Top_insu_tramcoye_qu = Aggre_tran_co_am_ye_quar(Top_insu_tramcoye, quarters) 


        elif method_3 == "Top Transaction":
            col1, col2 = st.columns([3,2])

            with col1:
                years = st.selectbox("Select the Year", Top_transaction["Years"].unique())
            # Storing the df returned by transaction_count_amount_year function in Agg_tran_tramcoye variable
            Top_tran_tramcoye = Aggre_tran_co_am_ye(Top_transaction, years)   

            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select the State", Top_tran_tramcoye["States"].unique())
            top_insu_pintramyequst(Top_tran_tramcoye, states)

            col1, col2 = st.columns([3,2])
            with col1:
                quarters = st.selectbox("Select the Quarter", sorted(Top_tran_tramcoye["Quarters"].unique()))
            Top_tran_tramcoye_qu = Aggre_tran_co_am_ye_quar(Top_tran_tramcoye, quarters) 

        elif method_3 == "Top User":
            col1, col2 = st.columns([3,2])
            with col1:
                years = st.selectbox("Select the Year", Top_user["Years"].unique())
            # Storing the df returned by transaction_count_amount_year function in Agg_tran_tramcoye variable
            Top_usyequst  = top_user_ru_ye(Top_user, years)  

            col1, col2 = st.columns([3,2])
            with col1:
                states = st.selectbox("Select the State", Top_usyequst["States"].unique())
            top_user_ru_ye_st(Top_usyequst, states)


elif select == "TOP CHARTS":
    question = st.selectbox("Select the Question", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered Users of Map User",
                                                    "9. App Opens of Map User",
                                                    "10. Registered Users of Top User"])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Aggregated_insurance")
    
    elif question == "2. Transaction Amount and Count of Map Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Map_insurance")
    
    elif question == "3. Transaction Amount and Count of Top Insurance":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Map_transaction")
    
    elif question == "6. Transaction Amount and Count of Top Transaction":
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Top_transaction")
    
    elif question == "7. Transaction Count of Aggregated User":
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Aggregated_user")

    elif question == "8. Registered Users of Map User":
        states = st.selectbox("Select the state to view the Top Charts", Map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("Map_user", states)
    
    elif question == "9. App Opens of Map User":
        states = st.selectbox("Select the state to view the Top Charts", Map_user["States"].unique())
        st.subheader("APP OPENS")
        top_chart_app_opens("Map_user", states)
    
    elif question == "10. Registered Users of Top User":
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("Top_user")
    
