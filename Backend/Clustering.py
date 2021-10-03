
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import time
from datetime import datetime
import pickle
import warnings
warnings.filterwarnings('ignore')


def movecol(df, cols_to_move=[], ref_col='', place='After'):
    
    cols = df.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]
    
    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]
    
    return(df[seg1 + seg2 + seg3])



def fun_clustering(user_id):
    merged_orders = pickle.load(open("Pickle\\merged_orders.p", "rb"))


    user_info = merged_orders[['user_id', 'order_number', 'order_dow', 'order_hour_of_day', 
                               'days_since_prior_order', 'department']]

    user_data = pd.get_dummies(user_info, prefix=None, columns=['department'])




    user_data['department_soft drinks'].value_counts()


    user_data1 = user_data[user_data['user_id'] <= 65000]
    user_data2 = user_data[(user_data['user_id'] <= 135000) & (user_data['user_id'] > 65000)]
    user_data3 = user_data[user_data['user_id'] > 135000]



    grouped_user1 = user_data1.groupby('user_id').sum()


    grouped_user2 = user_data2.groupby('user_id').sum()


    grouped_user3 = user_data3.groupby('user_id').sum()


    user_data1_nodepts = user_data1.iloc[:,:5]
    user_data2_nodepts = user_data2.iloc[:,:5]
    user_data3_nodepts = user_data3.iloc[:,:5]


    group1 = user_data1_nodepts.groupby('user_id').agg({'order_number': 'max', 'order_dow': lambda x:x.value_counts().index[0], 
                                                'order_hour_of_day': 'median', 'days_since_prior_order': 'mean'})
    group2 = user_data2_nodepts.groupby('user_id').agg({'order_number': 'max', 'order_dow': lambda x:x.value_counts().index[0], 
                                                'order_hour_of_day': 'median', 'days_since_prior_order': 'mean'})
    group3 = user_data3_nodepts.groupby('user_id').agg({'order_number': 'max', 'order_dow': lambda x:x.value_counts().index[0], 
                                                'order_hour_of_day': 'median', 'days_since_prior_order': 'mean'})

    grouped_user1['num_orders'] = group1.order_number
    grouped_user2['num_orders'] = group2.order_number
    grouped_user3['num_orders'] = group3.order_number


    grouped_user1['mean_days_since'] = group1.days_since_prior_order
    grouped_user2['mean_days_since'] = group2.days_since_prior_order
    grouped_user3['mean_days_since'] = group3.days_since_prior_order


    grouped_user1['mode_order_dow'] = group1.order_dow
    grouped_user2['mode_order_dow'] = group2.order_dow
    grouped_user3['mode_order_dow'] = group3.order_dow

    grouped_user1['median_order_hour'] = group1.order_hour_of_day
    grouped_user2['median_order_hour'] = group2.order_hour_of_day
    grouped_user3['median_order_hour'] = group3.order_hour_of_day

    grouped_user1.drop(columns=['order_number', 'order_dow', 'order_hour_of_day', 'days_since_prior_order'], inplace=True)
    grouped_user2.drop(columns=['order_number', 'order_dow', 'order_hour_of_day', 'days_since_prior_order'], inplace=True)
    grouped_user3.drop(columns=['order_number', 'order_dow', 'order_hour_of_day', 'days_since_prior_order'], inplace=True)

    grouped_users = pd.concat([grouped_user1, grouped_user2, grouped_user3], axis=0)


    grouped_users = movecol(grouped_users, 
                 cols_to_move=['num_orders', 'mode_order_dow', 'median_order_hour', 'mean_days_since'], 
                 ref_col='department_air fresheners candles',
                 place='Before')

    pickle.dump(grouped_users, open("Pickle\\grouped_users.p", "wb"))
    grouped_users = pickle.load(open("Pickle\\grouped_users.p", "rb"))

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaled_users = scaler.fit_transform(grouped_users)

    from sklearn.cluster import KMeans
    random_state = 10

    k_means_5 = KMeans(n_clusters=5, random_state=random_state, algorithm='full').fit(scaled_users)
    k_means_6 = KMeans(n_clusters=6, random_state=random_state, algorithm='full').fit(scaled_users)
    k_means_7 = KMeans(n_clusters=7, random_state=random_state, algorithm='full').fit(scaled_users)
    k_means_8 = KMeans(n_clusters=8, random_state=random_state, algorithm='full').fit(scaled_users)
    k_means_9 = KMeans(n_clusters=9, random_state=random_state, algorithm='full').fit(scaled_users)

    k_list = [k_means_5,k_means_6,k_means_7,k_means_8 ]


    from sklearn.metrics import calinski_harabasz_score

    CH_score = []

    for model in k_list:
        labels = model.labels_
        CH_score.append(calinski_harabasz_score(grouped_users, labels))

    grouped_users['cluster'] = k_means_5.labels_

    pickle.dump(grouped_users, open('Pickle\\clustered_users.p', 'wb'))


    grouped_users.cluster.value_counts()

    cluster_data = grouped_users.groupby('cluster').median()

    x = list(grouped_users.index)
    y = list(grouped_users['cluster'])

    z = dict(zip(x,y))

    df = pd.DataFrame(z.items(), columns=['user_id', 'cluster_id'])
    df.to_csv("Dataset\\clusters.csv")

    # print(z)
    clid = z[user_id]
    print("cluster_id =>", clid)
    return(clid)
