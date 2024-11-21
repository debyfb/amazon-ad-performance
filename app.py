import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Config
st.set_page_config(
    page_title="Analysis of Amazon Advertising Performance",
    layout="wide",
    page_icon=":chart_with_upwards_trend:"
)

# Import Dataframe
df = pd.read_csv('week_data_cleaned.csv')
df = df.dropna()

st.title("Analysis of Amazon Advertising Performance")
st.markdown('''
            Analysis of Amazon Advertising Performance Metrics offers a detailed analysis of the 
            efficiency and impact of advertising campaigns conducted by sellers on Amazon. By analyzing 
            Amazon advertising performance metrics, users can gain valuable insights into the effectiveness 
            of advertising strategy.
            ''')


tab1, tab2 = st.tabs(["Trend Analysis", "Search Query Analysis"])

with tab1:
    st.subheader("Time Series")
    
    metrics_options = ['Impression (total count)', 'Click (total count)', 'Cart Add (total count)', 'Purchase (total count)']
    selected_metrics = st.multiselect('Select Performance Metrics', metrics_options, default=['Impression (total count)', 'Click (total count)', 'Cart Add (total count)', 'Purchase (total count)'])

    if not selected_metrics:
        st.warning("Please select at least one metric to display")
        
    else:
        df['week_number'] = df['week_number'].astype(int)        
        metric_data = []
        
        metric_columns = {
            'Impression (total count)': 'imp_total_count',
            'Click (total count)': 'clk_total_count',
            'Cart Add (total count)': 'cart_total_count',
            'Purchase (total count)': 'pur_total_count'
        }
        
        metric_titles = {
            'Impression (total count)': 'Impression Count',
            'Click (total count)': 'Click Count',
            'Cart Add (total count)': 'Cart Add Count',
            'Purchase (total count)': 'Purchase Count'
        }
        
        for metric in selected_metrics:
            column_name = metric_columns[metric]
            mean_by_week = df.groupby('week')[column_name].mean().reset_index()
            mean_by_week['Metric'] = metric_titles[metric]
            mean_by_week['Value'] = mean_by_week[column_name]
            metric_data.append(mean_by_week[['week', 'Metric', 'Value']])
        
        combined_data = pd.concat(metric_data)
        
        line_chart = alt.Chart(combined_data).mark_line().encode(
            x=alt.X('week:O', title="Week", sort=df['week_number'].unique().tolist()),
            y=alt.Y('Value:Q', title="Value"),
            color=alt.Color('Metric:N', title="Metric", scale=alt.Scale(scheme='darkmulti'),),
            tooltip=[
                alt.Tooltip('week:O', title='Week'),
                alt.Tooltip('Metric:N', title="Metric"),
                alt.Tooltip('Value:Q', title="Value")
            ]
        ).interactive()

        points = alt.Chart(combined_data).mark_point(size=60, filled=True).encode(
            x=alt.X('week:O'),
            y=alt.Y('Value:Q'),
            color=alt.Color('Metric:N', title="Metric", scale=alt.Scale(scheme='darkmulti'),),  # Match the line color
            tooltip=[
                alt.Tooltip('week:O', title='Week'),
                alt.Tooltip('Metric:N', title="Metric"),
                alt.Tooltip('Value:Q', title="Value")
            ]
        )

        # Combine the charts into a layered chart
        line_chart_with_dots = alt.layer(line_chart, points).properties(
            width=900,
            height=600
        )

        st.altair_chart(line_chart_with_dots)
            
    st.subheader("Relationship Between Click Rate, Purchase Rate, and Cart Add Rate")

    df['pur_purchase_rate'] = pd.to_numeric(df['pur_purchase_rate'], errors='coerce')
    df['cart_add_rate'] = pd.to_numeric(df['cart_add_rate'], errors='coerce')
    df['clk_click_rate'] = pd.to_numeric(df['clk_click_rate'], errors='coerce')

    col1a, col2a = st.columns(2)
    with col1a:
        scatter_plot = alt.Chart(df).mark_point(size=80, color='#197d8c', filled=True, opacity=0.7).encode(
            x=alt.X('pur_purchase_rate:Q', title='Purchase Rate'),
            y=alt.Y('cart_add_rate:Q', title='Cart Add Rate'),
            tooltip=[
                alt.Tooltip('search_query:N', title="Search Query"),
                alt.Tooltip('pur_purchase_rate:Q', title="Purchase Rate"),
                alt.Tooltip('cart_add_rate:Q', title="Cart Add Rate")
                ]
        ).properties(
            title='Purchase Rate vs Cart Add Rate',
            width=455,
            height=400
        ).interactive()
        
        st.altair_chart(scatter_plot)

    with col2a:
        scatter_plot2 = alt.Chart(df).mark_point(size=80, color='#197d8c', filled=True, opacity=0.7).encode(
            x=alt.X('clk_click_rate:Q', title='Click Rate'),
            y=alt.Y('cart_add_rate:Q', title='Cart Add Rate'),
            tooltip=[
                alt.Tooltip('search_query:N', title="Search Query"),
                alt.Tooltip('clk_click_rate:Q', title="Click Rate"),
                alt.Tooltip('cart_add_rate:Q', title="Cart Add Rate")
                ]
        ).properties(
            title='Click Rate vs Cart Add Rate',
            width=455,
            height=400
        ).interactive()

        st.altair_chart(scatter_plot2)

    with st.expander("See Glossary"):
        st.write('''
                 1. **:red[Week]**: Week period in which data was collected.
                 2. **:red[Search query]**: Specific keywords or phrases used by customers when searching for products on Amazon.
                 3. **:red[Impression total count]**: The total number of times the advertisement was displayed to customers in search results or on product pages.
                 4. **:red[Click total count]**: The total number of times customers clicked on the advertisement.
                 5. **:red[Cart total count]**: The total number of times customers added a product to their cart after clicking on the advertisement.
                 6. **:red[Purchase total count]**: The total number of times customers made a purchase after clicking on the advertisement.
                 7. **:red[Click rate]**: The percentage of times the advertisement was clicked on relative to the number of times it was displayed.
                 8. **:red[Cart add rate]**: The percentage of times the advertisement resulted in a product being added to a customer's cart.
                 9. **:red[Purchase rate]**: The percentage of times the advertisement resulted in a customer making a purchase.
                 ''')

with tab2:
    st.subheader("Search Query Performance")
    all_weeks = sorted(df['week'].unique().tolist())
    week_options = ['All'] + all_weeks

    col1, col2 = st.columns([2, 2])

    with col1:
        selected_week = st.selectbox('Select Week:', week_options, key='week_select_1')

    with col2:
        search_query = st.text_input("Search in **search query**:", "")

    column_names = {
        'week': 'Week',
        'search_query': 'Search Query',
        'imp_total_count': 'Impression Count',
        'clk_total_count': 'Click Count',
        'cart_total_count': 'Cart Add Count',
        'pur_total_count': 'Purchase Count'
    }
    selected_columns = ['week','search_query','imp_total_count','clk_total_count','cart_total_count','pur_total_count']

    if selected_week == 'All':
        filtered_df = df[selected_columns]
    else:
        filtered_df = df[df['week'] == selected_week][selected_columns]

    if search_query:
        filtered_df = filtered_df[
            filtered_df['search_query'].str.contains(search_query, case=False, na=False)
        ]

    total_impressions = filtered_df['imp_total_count'].sum()
    total_cart_adds = filtered_df['cart_total_count'].sum()
    total_purchases = filtered_df['pur_total_count'].sum()

    filtered_df = filtered_df.rename(columns=column_names)

    st.write(f"Showing {len(filtered_df)} rows")

    st.dataframe(
        filtered_df,
        width=900,
        height=400
    )

    col1a, col2a, col3a = st.columns(3)
    with col1a:
        st.markdown("**Total of Impression Count**")
        st.markdown(f"**:orange[{total_impressions:,}]**")
    with col2a:
        st.markdown("**Total of Cart Add Count**")
        st.markdown(f":orange[**{total_cart_adds:,}**]")
    with col3a:
        st.markdown("**Total of Purchase Count**")
        st.markdown(f":orange[**{total_purchases:,}**]")

    st.subheader("Identifying Popular Search Query")

    # Add a second week selection that defaults to the first selected week
    col1b, col2b = st.columns([2, 2])
    
    with col1b:
        selected_week2 = st.selectbox('Select Week:', week_options, index=week_options.index(selected_week), key='week_select_2')

    with col2b:
        search_query2 = st.text_input("Search in *search query*:", key='search_query_2')

    column_names2 = {
        'week': 'Week',
        'search_query': 'Search Query',
        'search_quey_volume': 'Search Query Volume'
    }

    # Create filtered_df2 based on selected_week2
    if selected_week2 == 'All':
        filtered_df2 = df[['week', 'search_query', 'search_quey_volume']]
    else:
        filtered_df2 = df[df['week'] == selected_week2][['week', 'search_query', 'search_quey_volume']]

    if search_query2:
        filtered_df2 = filtered_df2[
            filtered_df2['search_query'].str.contains(search_query2, case=False, na=False)
        ]

    total_search_query_volume = filtered_df2['search_quey_volume'].sum()

    filtered_df2 = filtered_df2.rename(columns=column_names2)

    st.write(f"Showing {len(filtered_df2)} rows")

    st.dataframe(
        filtered_df2,
        width=900,
        height=400
    )

    st.markdown("**Total of Search Query Volume**")
    st.markdown(f"**:orange[{total_search_query_volume:,}]**")

    with st.expander("See Glossary"):        
        st.write('''
                 1. **:red[Week]**: week period in which data was collected.
                 2. **:red[Search Query]**: Specific keywords or phrases used by customers when searching for products on Amazon.
                 3. **:red[Search Query Volume]**: The number of times a particular search query was used by customers during the given time period.
                 4. **:red[Impression total count]**: The total number of times the advertisement was displayed to customers in search results or on product pages.
                 5. **:red[Click total count]**: The total number of times customers clicked on the advertisement.
                 6. **:red[Cart total count]**: The total number of times customers added a product to their cart after clicking on the advertisement.
                 7. **:red[Purchase total count]**: The total number of times customers made a purchase after clicking on the advertisement.
                 ''')
