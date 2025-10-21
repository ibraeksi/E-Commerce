import numpy as np
import pandas as pd

def calculate_total_IT_costs(num_sellers, num_items):
    return 3157.27*np.sqrt(num_sellers) + 978.23*np.sqrt(num_items)

def seller_revenue(df):
    """
    Calculates seller economics to identify which sellers to remove from marketplace
    df = Dataframe with orders
    """
    # Compute sales with dates
    df["date_first_sale"] = df["order_approved"]
    df["date_last_sale"] = df["order_approved"]
    df['review_cost'] = df.review_score.map({1: 100,2: 50,3: 40,4: 0,5: 0})
    seller_group = df.groupby('seller_id').agg({"date_first_sale": 'min',"date_last_sale": 'max'})
    seller_group['months_on_olist'] = round((seller_group['date_last_sale'] - seller_group['date_first_sale']) / np.timedelta64(30, 'D'))
    sales_group = df.groupby(['seller_id']).agg({'price': 'sum', 'review_cost': 'sum', 'order_id': 'count'}).rename(columns={'price': 'sales', 'review_cost': 'cost_of_reviews', 'order_id': 'quantity'})
    df_sales = df.merge(seller_group, on='seller_id').merge(sales_group, on='seller_id')

    # Add seller economics (revenues, profits)
    olist_monthly_fee = 80
    olist_sales_cut = 0.1

    df_sales['revenues'] = df_sales['months_on_olist'] * olist_monthly_fee + olist_sales_cut * df_sales['sales']
    df_sales['profits'] = df_sales['revenues'] - df_sales['cost_of_reviews']

    df_sales = df_sales.sort_values('profits').reset_index(drop=True)

    # Get only unique sellers rows for plotting
    plot_df = df_sales.drop_duplicates(subset=['seller_id'], keep='first').reset_index(drop=True)

    profit_dict = {'num_sellers':[], 'num_items': [], 'total_revenues': [], 'IT Costs': [],
                'Total Profits': [], 'Net Profits': []}
    for i in range(len(plot_df)):
        temp = plot_df[i:].reset_index(drop=True)

        profit_dict['num_sellers'].append(len(temp))
        profit_dict['num_items'].append(temp['quantity'].sum())
        profit_dict['total_revenues'].append(temp['revenues'].sum())

        total_IT_costs = calculate_total_IT_costs(len(temp), temp['quantity'].sum())
        profit_dict['IT Costs'].append(total_IT_costs/1000000)

        profit_dict['Total Profits'].append(temp['profits'].sum()/1000000)
        profit_dict['Net Profits'].append(temp['profits'].sum()/1000000 - total_IT_costs/1000000)

    varied_num_sellers_df = pd.DataFrame(profit_dict)

    return plot_df, varied_num_sellers_df
