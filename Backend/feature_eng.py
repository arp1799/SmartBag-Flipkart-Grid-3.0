import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import gc
import os


def generate_product_features(prior_data = None):
    
    product_features = pd.DataFrame(columns=['product_id'])

    product_features['product_id'] = prior_data['product_id'].sort_values().unique()
    
    df = pd.DataFrame({'reorder_rate': prior_data.groupby(['product_id','reordered'])['reordered'].\
                                                       count().groupby(level=0).\
                                                       apply(lambda x: x / float(x.sum()))}).reset_index()

    new_df = df[df['reordered']==1]
    new_df['reorder_rate'] = new_df['reorder_rate'] * new_df['reordered']
    
    new_df_1 = df[(df['reordered']==0) & (df['reorder_rate']==float(1.0))]
    new_df_1['reorder_rate'] = new_df_1['reorder_rate'] * new_df_1['reordered']
    new_df = new_df.append(new_df_1)
    
    new_df.drop('reordered', axis = 1, inplace = True)
    new_df.sort_values(by='product_id', inplace =  True)   
    new_df = new_df.reset_index(drop = True)
    
    product_features['product_reorder_rate'] = new_df['reorder_rate']
    
    mean_position = prior_data.groupby('product_id')['add_to_cart_order'].mean().reset_index(name = 'mean_position')
    mean_position.sort_values(by = 'product_id', inplace = True)
    product_features['avg_pos_incart'] = mean_position['mean_position']
    
    
    
    products['organic'] = products['product_name'].apply(lambda x: 'organic' in x.lower()).astype(int)
    products['isYogurt'] = products['department_id'].apply(lambda x: x==120).astype(int)

    products['isProduce'] = products['department_id'].apply(lambda x: x==138).astype(int)
    products['isFrozen'] = products['department_id'].apply(lambda x: x==135).astype(int)
    products['isdairy'] = products['department_id'].apply(lambda x: x==150).astype(int)
    products['isbreakfast'] = products['department_id'].apply(lambda x: x==148).astype(int)
    products['issnack'] = products['department_id'].apply(lambda x: x==153).astype(int)
    products['isbeverage'] = products['department_id'].apply(lambda x: x==141).astype(int)

    new_product_feat = products[['organic', 'isYogurt', 'isProduce', 'isFrozen', 'isdairy', 'isbreakfast', 'issnack', 'isbeverage']]
    
    from sklearn.decomposition import NMF
    from sklearn.preprocessing import normalize

    nmf = NMF(n_components = 3)
    model = nmf.fit(new_product_feat)
    W = model.transform(new_product_feat)
    prod_data = pd.DataFrame(normalize(W))

    prod_data.columns = ['p_reduced_feat_1', 'p_reduced_feat_2','p_reduced_feat_3']
    products.drop(['organic', 'isYogurt', 'isProduce', 'isFrozen', 'isdairy', 'isbreakfast', 'issnack', 'isbeverage'], axis = 1, inplace =True)

    product_features['p_reduced_feat_1'] = prod_data['p_reduced_feat_1']
    product_features['p_reduced_feat_2'] = prod_data['p_reduced_feat_2']
    product_features['p_reduced_feat_3'] = prod_data['p_reduced_feat_3']
    

    df = prior_data.groupby(['department']).size().reset_index(name='order_count')
    new_df = pd.merge(prior_data, df, on = 'department')
    aisle_reorder_rate = prior_data[prior_data['reordered']==1].groupby(['department']).size().reset_index(name='reorder_rate')
    df['dept_reorder_rate'] = aisle_reorder_rate['reorder_rate']/df['order_count']
    df.drop(['order_count'], axis = 1, inplace = True)
    new_df = pd.merge(new_df, df, on = 'department')
    
    new_df = new_df[['product_id','department_id']]
    new_df.drop_duplicates(keep='first', inplace = True)

    product_features = pd.merge(product_features, new_df , on='product_id', how = 'inner')
    
    del df, new_df, new_df_1, new_product_feat, model, prod_data
    return product_features

def generate_user_features(prior_data = None):

    user_features = pd.DataFrame(columns=['user_id'])
    
    user_features['user_id'] = prior_data['user_id'].sort_values().unique()
    
    
    user_reorder_rate = prior_data.groupby(["user_id","reordered"])['reordered'].count().groupby(level = 0).apply(lambda x: x / float(x.sum())).reset_index(name='reorder_rate')
    user_reorder_rate = user_reorder_rate.pivot(index ='user_id', columns ='reordered', values =['reorder_rate']) 
    user_reorder_rate = pd.DataFrame(user_reorder_rate.to_records())
    user_reorder_rate.columns = ['user_id','0', '1']
    user_reorder_rate.set_index("user_id", inplace = True)
    user_reorder_rate.fillna(0, inplace = True)
    user_reorder_rate.reset_index(inplace = True)
    user_features['user_reorder_rate'] = user_reorder_rate['1']
    
    user_features['user_unique_products'] = prior_data.groupby(["user_id"])['product_name'].nunique().reset_index(name = 'unique')['unique']
    
    user_features['user_total_products'] = prior_data.groupby(["user_id"])['product_name'].size().reset_index(name = 'count')['count']
    
    df = prior_data.groupby(["user_id","order_id"])['add_to_cart_order'].count().reset_index(name='cart_size')\
                                                                .groupby('user_id')['cart_size'].mean().reset_index()
    user_features['user_avg_cart_size'] = df['cart_size']
    
    df = prior_data.groupby(["user_id","order_id"])['days_since_prior_order'].max().reset_index(name='mean_days_between_orders')\
                                                                .groupby('user_id')['mean_days_between_orders'].mean().reset_index()
    user_features['user_avg_days_between_orders'] = df['mean_days_between_orders']
    
    
    df['user_id'] = prior_data['user_id'].sort_values().unique()
    df['user_unique_products'] = prior_data.groupby(["user_id"])['product_name'].nunique().reset_index(name = 'unique')['unique']
    df['user_reordered_products'] = prior_data[prior_data['reordered']==1].groupby(["user_id"])['product_name'].nunique().reset_index(name = 'reordered_unique')['reordered_unique']
    df.fillna(0, inplace = True)
    user_features['user_reordered_products_ratio'] = df['user_reordered_products'] / df['user_unique_products']
    
    del df
    return user_features

def max_streak(row):
    
    _max = 0
    _sum = 0
    for i in row:
        if i==1:
            _sum += 1
        else:
            if _sum > _max:
                _max = _sum
            _sum = 0 
    return _max

def generate_user_product_features(prior_data = None):
    

    user_product_features = pd.DataFrame(columns=['user_id','product_id'])
    
   
    u_p = prior_data.groupby(["user_id","product_id"]).size().reset_index()
    user_product_features["user_id"] = u_p["user_id"]
    user_product_features["product_id"] = u_p["product_id"]
    
   
    df = prior_data.groupby(["user_id","product_id"])["reordered"].size()
    df = df/prior_data.groupby(["user_id"]).size()
    df = df.reset_index(name = 'order_rate')
    df.fillna(0. , inplace = True)
    user_product_features["u_p_order_rate"] = df["order_rate"]
    

    df = prior_data[prior_data["reordered"]==1].groupby(["user_id","product_id"])["reordered"].size()
    df = df/prior_data.groupby(["user_id","product_id"]).size()
    df = df.reset_index(name = 'reorder_rate')
    df.fillna(0. , inplace = True)
    user_product_features["u_p_reorder_rate"] = df["reorder_rate"]
    
   
    
    df = prior_data.groupby(["user_id","product_id"])['add_to_cart_order'].mean().reset_index(name = 'mean_position')
    user_product_features['u_p_avg_position'] = df['mean_position']

    
   
    
    df = prior_data.groupby(["user_id","product_id"])['order_number'].max().reset_index()
    df_2 = prior_data.groupby(["user_id"])['order_number'].max().reset_index()
    new_df = pd.merge(df, df_2,  how='outer', left_on=['user_id'], right_on = ['user_id'])        
    new_df['order_diff'] = new_df['order_number_y'] - new_df['order_number_x']
    user_product_features['u_p_orders_since_last'] = new_df['order_diff']
    
    
    df = prior_data.groupby(["user_id","product_id"])['reordered'].apply(list).reset_index(name = 'max_streak')
    df['max_streak'] = df['max_streak'].apply(max_streak)
    user_product_features = pd.merge(user_product_features, df, on= ["user_id","product_id"])    
    
    del df, new_df, df_2
    return user_product_features



def hour_tocategorical(time):
    if time > 5 and time < 12:
            return 0
    elif time > 12 and time < 17:
        return 1
    elif time > 17 and time < 21:
        return 2
    else:
        return 3
    

def product_time(prior_data = None):
    
    df = prior_data.groupby(['product_id','order_hour_of_day'])["reordered"].size()
    df = df/prior_data.groupby(["product_id"]).size()
    df = df.reset_index(name = 'hour_reorder_rate')
    return df

def product_day(prior_data = None):
    df = prior_data.groupby(['product_id','order_dow'])["reordered"].size()
    df = df/prior_data.groupby(["product_id"]).size()
    df = df.reset_index(name = 'day_reorder_rate')
    return df

def product_days_since_prior(prior_data = None):
    df = prior_data.groupby(['product_id','days_since_prior_order'])["reordered"].size()
    df = df/prior_data.groupby(["product_id"]).size()
    df = df.reset_index(name = 'p_days_since_prior_order_reorder_rate')
    return df

def user_days_since_prior(prior_data = None):
    df = prior_data.groupby(['user_id','days_since_prior_order'])["reordered"].size()
    df = df/prior_data.groupby(["user_id"]).size()
    df = df.reset_index(name = 'u_days_since_prior_order_reorder_rate')
    return df

def u_p_days_since_prior(prior_data = None):
    df = prior_data.groupby(["user_id","product_id","days_since_prior_order"])["reordered"].size()
    df = df/prior_data.groupby(["user_id","product_id"]).size()
    df = df.reset_index(name = 'days_since_prior_reorder_rate')
    return df


def fun_FE(cluster_id):
    #overriding default setting of pandas
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    global products

    departments = pd.read_csv('Dataset\\departments.csv')
    prior_order = pd.read_csv('Dataset\\previous_orders_data.csv')
    train_order = pd.read_csv('Dataset\\training_orders_data.csv')
    orders = pd.read_csv('Dataset\\orders.csv')
    products = pd.read_csv('Dataset\\products.csv')
    if cluster_id != -1:
        clusters = pd.read_csv('Dataset\\clusters.csv')

        users = list(clusters[clusters['cluster_id']==cluster_id]['user_id'])
        orders = orders[orders['user_id'].isin(users)]
    orders.fillna(value = 0, inplace = True)

    prior_orders_data = prior_order.sort_values(by=['order_id'])
    prior_orders_data = pd.merge(left = prior_orders_data, right = products,
                                left_on='product_id', right_on='product_id').sort_values(by=['order_id']).reset_index(drop=True)
    prior_orders_data = pd.merge(left = prior_orders_data, right = departments,
                                left_on='department_id', right_on='department_id').sort_values(by=['order_id']).reset_index(drop=True)
    prior_orders_data = pd.merge(left = prior_orders_data, right = orders,
                                left_on='order_id', right_on='order_id').sort_values(by=['order_id']).reset_index(drop=True)

    col_order = ['user_id',
    'order_id',
    'product_id',
    'department_id',
    'add_to_cart_order',
    'reordered',
    'product_name',
    'department',
    'eval_set',
    'order_number',
    'order_dow',
    'order_hour_of_day',
    'days_since_prior_order']

    prior_orders_data = prior_orders_data[col_order]

    prior_orders_data = pd.concat([prior_order, train_order]).sort_values(by=['order_id'])
    prior_orders_data = pd.merge(left = prior_orders_data, right = products,
                                left_on='product_id', right_on='product_id').sort_values(by=['order_id']).reset_index(drop=True)
    prior_orders_data = pd.merge(left = prior_orders_data, right = departments,
                            left_on='department_id', right_on='department_id').sort_values(by=['order_id']).reset_index(drop=True)
    prior_orders_data = pd.merge(left = prior_orders_data, right = orders,
                                left_on='order_id', right_on='order_id').sort_values(by=['order_id']).reset_index(drop=True)

    prior_orders_data.groupby(["user_id","product_id"]).size().shape[0]/prior_orders_data.shape[0]

    from collections import Counter 
    x = products.product_name.values.tolist()
    x = " ".join(x).split()



    product_features = generate_product_features(prior_data = prior_orders_data )
    product_features.to_csv("CSV\\product_features_v6.csv",index=False)



    user_features = generate_user_features(prior_data = prior_orders_data)
    user_features.to_csv("CSV\\user_features_v6.csv",index=False)


    user_product_features = generate_user_product_features(prior_data = prior_orders_data)
    user_product_features.to_csv("CSV\\user_product_features_prior_data_v6.csv",index=False)



    hour_reorder_rate = product_time(prior_orders_data)
    day_reorder_rate = product_day(prior_orders_data)
    p_days_since_prior_order_reorder_rate = product_days_since_prior(prior_orders_data)
    u_days_since_prior_order_reorder_rate = user_days_since_prior(prior_orders_data)
    days_since_prior_reorder_rate = u_p_days_since_prior(prior_orders_data)

    hour_reorder_rate.to_csv("CSV\\hour_reorder_rate.csv", index = False)
    day_reorder_rate.to_csv("CSV\\day_reorder_rate.csv", index = False)
    p_days_since_prior_order_reorder_rate.to_csv("CSV\\p_days_since_prior_order_reorder_rate.csv", index = False)
    u_days_since_prior_order_reorder_rate.to_csv("CSV\\u_days_since_prior_order_reorder_rate.csv", index = False)
    days_since_prior_reorder_rate.to_csv("CSV\\days_since_prior_reorder_rate.csv", index = False)

    product_features = pd.read_csv("CSV\\product_features_v6.csv")
    user_features = pd.read_csv("CSV\\user_features_v6.csv")
    user_product_features = pd.read_csv("CSV\\user_product_features_prior_data_v6.csv")

    merged_df = pd.merge(user_product_features, user_features,  how='outer', left_on=['user_id'], right_on = ['user_id'])
    merged_df = pd.merge(merged_df, product_features,  how='outer', left_on=['product_id'], right_on = ['product_id'])
    merged_df.to_pickle("Pickle\\merged_user_product_features.pkl")

    order_details_train = orders[orders['eval_set'] == 'train']

    train_order_data = train_order.sort_values(by=['order_id'])
    train_order_data = pd.merge(left = train_order_data, right = products,
                                left_on='product_id', right_on='product_id').sort_values(by=['order_id']).reset_index(drop=True)
    train_order_data = pd.merge(left = train_order_data, right = departments,
                                left_on='department_id', right_on='department_id').sort_values(by=['order_id']).reset_index(drop=True)
    train_order_data = pd.merge(left = train_order_data, right = orders,
                                left_on='order_id', right_on='order_id').sort_values(by=['order_id']).reset_index(drop=True)

    col_order = ['user_id',
    'order_id',
    'product_id',
    'department_id',
    'add_to_cart_order',
    'reordered',
    'product_name',
    'department',
    'eval_set',
    'order_number',
    'order_dow',
    'order_hour_of_day',
    'days_since_prior_order']


    x = os.listdir('HDF')
    if(len(x)==0):
        pass
    else:
        os.remove('HDF\\'+x[0])


    train_order_data = train_order_data[col_order]

    upd_train_orders = train_order_data[['user_id','order_id','product_id','reordered']]
    last_orders = upd_train_orders.groupby(['user_id'])['order_id'].max().reset_index(name = 'new_order_id')
    order_details = train_order_data[['order_id','order_dow','order_hour_of_day','days_since_prior_order']]
    order_details = order_details.drop_duplicates()

    train_orders_merged_df = pd.merge(merged_df, upd_train_orders,  how='left', left_on=['user_id','product_id'], right_on = ['user_id','product_id'])
    train_orders_merged_df = pd.merge(train_orders_merged_df, last_orders, on = 'user_id')
    train_orders_merged_df.drop("order_id", axis = 1, inplace = True)
    train_orders_merged_df.rename(columns = {'new_order_id':'order_id'}, inplace = True) 
    train_orders_merged_df = pd.merge(train_orders_merged_df, order_details, on = 'order_id')
    train_orders_merged_df[['reordered']]= train_orders_merged_df[['reordered']].fillna(value=0.0)

    train_orders_merged_df = pd.merge(train_orders_merged_df, hour_reorder_rate, on=['product_id','order_hour_of_day'], how = 'left')
    train_orders_merged_df[['hour_reorder_rate']]= train_orders_merged_df[['hour_reorder_rate']].fillna(value=0.0)

    train_orders_merged_df = pd.merge(train_orders_merged_df, day_reorder_rate, on=['product_id','order_dow'], how = 'left')
    train_orders_merged_df[['day_reorder_rate']]= train_orders_merged_df[['day_reorder_rate']].fillna(value=0.0)

    train_orders_merged_df = pd.merge(train_orders_merged_df, p_days_since_prior_order_reorder_rate, on=['product_id','days_since_prior_order'], how = 'left')
    train_orders_merged_df[['p_days_since_prior_order_reorder_rate']]= train_orders_merged_df[['p_days_since_prior_order_reorder_rate']].fillna(value=0.0)

    train_orders_merged_df = pd.merge(train_orders_merged_df, u_days_since_prior_order_reorder_rate, on=['user_id','days_since_prior_order'], how = 'left')
    train_orders_merged_df[['u_days_since_prior_order_reorder_rate']]= train_orders_merged_df[['u_days_since_prior_order_reorder_rate']].fillna(value=0.0)

    train_orders_merged_df = pd.merge(train_orders_merged_df, days_since_prior_reorder_rate, on=["user_id","product_id",'days_since_prior_order'], how = 'left')
    train_orders_merged_df[['days_since_prior_reorder_rate']]= train_orders_merged_df[['days_since_prior_reorder_rate']].fillna(value=0.0)

    train_orders_merged_df = train_orders_merged_df[['user_id', 'product_id', 'u_p_order_rate', 'u_p_reorder_rate', 'u_p_avg_position', 'u_p_orders_since_last', 'max_streak', 'user_reorder_rate', 'user_unique_products', 'user_total_products', 'user_avg_cart_size', 'user_avg_days_between_orders', 'user_reordered_products_ratio', 'product_reorder_rate', 'avg_pos_incart', 'p_reduced_feat_1', 'p_reduced_feat_2', 'p_reduced_feat_3', 'department_id', 'order_dow', 'order_hour_of_day', 'days_since_prior_order', 'hour_reorder_rate', 'day_reorder_rate', 'p_days_since_prior_order_reorder_rate', 'u_days_since_prior_order_reorder_rate', 'days_since_prior_reorder_rate', 'order_id','reordered']]

    train_orders_merged_df['order_hour_of_day'] = train_orders_merged_df['order_hour_of_day'].apply(hour_tocategorical)

    train_orders_merged_df['user_id'] = train_orders_merged_df['user_id'].astype('int32')
    train_orders_merged_df['product_id'] = train_orders_merged_df['product_id'].astype('uint16')
    train_orders_merged_df['u_p_order_rate'] = train_orders_merged_df['u_p_order_rate'].astype('float16')
    train_orders_merged_df['u_p_reorder_rate'] = train_orders_merged_df['u_p_reorder_rate'].astype('float16')
    train_orders_merged_df['u_p_avg_position'] = train_orders_merged_df['u_p_avg_position'].astype('float16')
    train_orders_merged_df['u_p_orders_since_last'] = train_orders_merged_df['u_p_orders_since_last'].astype('int8')
    train_orders_merged_df['max_streak'] = train_orders_merged_df['max_streak'].astype('int8')
    train_orders_merged_df['user_reorder_rate'] = train_orders_merged_df['user_reorder_rate'].astype('float16')
    train_orders_merged_df['user_unique_products'] = train_orders_merged_df['user_unique_products'].astype('int16')
    train_orders_merged_df['user_total_products'] = train_orders_merged_df['user_total_products'].astype('int16')
    train_orders_merged_df['user_avg_cart_size'] = train_orders_merged_df['user_avg_cart_size'].astype('float16')
    train_orders_merged_df['user_avg_days_between_orders'] = train_orders_merged_df['user_avg_days_between_orders'].astype('float16')
    train_orders_merged_df['user_reordered_products_ratio'] = train_orders_merged_df['user_reordered_products_ratio'].astype('float16')
    train_orders_merged_df['product_reorder_rate'] = train_orders_merged_df['product_reorder_rate'].astype('float16')
    train_orders_merged_df['avg_pos_incart'] = train_orders_merged_df['avg_pos_incart'].astype('float16')
    train_orders_merged_df['p_reduced_feat_1'] = train_orders_merged_df['p_reduced_feat_1'].astype('float16')
    train_orders_merged_df['p_reduced_feat_2'] = train_orders_merged_df['p_reduced_feat_2'].astype('float16')
    train_orders_merged_df['p_reduced_feat_3'] = train_orders_merged_df['p_reduced_feat_3'].astype('float16')
    train_orders_merged_df['department_id'] = train_orders_merged_df['department_id'].astype('uint8')
    train_orders_merged_df['order_dow'] = train_orders_merged_df['order_dow'].astype('uint8')
    train_orders_merged_df['order_hour_of_day'] = train_orders_merged_df['order_hour_of_day'].astype('uint8')
    train_orders_merged_df['days_since_prior_order'] = train_orders_merged_df['days_since_prior_order'].astype('uint8')
    train_orders_merged_df['hour_reorder_rate'] = train_orders_merged_df['hour_reorder_rate'].astype('float32')
    train_orders_merged_df['day_reorder_rate'] = train_orders_merged_df['day_reorder_rate'].astype('float32')
    train_orders_merged_df['p_days_since_prior_order_reorder_rate'] = train_orders_merged_df['p_days_since_prior_order_reorder_rate'].astype('float32')
    train_orders_merged_df['u_days_since_prior_order_reorder_rate'] = train_orders_merged_df['u_days_since_prior_order_reorder_rate'].astype('float32')
    train_orders_merged_df['days_since_prior_reorder_rate'] = train_orders_merged_df['days_since_prior_reorder_rate'].astype('float32')
    train_orders_merged_df['order_id'] = train_orders_merged_df['order_id'].astype('int32')

    train_orders_merged_df.to_hdf("HDF\\Data_v2.h5", "train", append=True) #0.73GB -> hdf5 doesnt reset the updated dtypes
    train_orders_merged_df.to_pickle("Pickle\\train_orders_merged_df_v6.pkl") #0.7GB  -> same here
    train_orders_merged_df.to_csv("CSV\\train_orders_merged_df_v6.csv",index=False) #1.5 GB -> to_csv resets to default dtypes

    order_details_test = orders[orders['eval_set'] == 'test']
    order_details_test.drop(['eval_set'], axis = 1, inplace = True)

    test_orders_merge_df = pd.merge(order_details_test, user_product_features, on = ['user_id'], how = 'outer')
    test_orders_merge_df.dropna(inplace =True)
    test_orders_merge_df = pd.merge(test_orders_merge_df, user_features, on = ['user_id'])
    test_orders_merge_df = pd.merge(test_orders_merge_df, product_features, on = ['product_id'])

    test_orders_merge_df = pd.merge(test_orders_merge_df, hour_reorder_rate, on=['product_id','order_hour_of_day'], how = 'left')
    test_orders_merge_df[['hour_reorder_rate']]= test_orders_merge_df[['hour_reorder_rate']].fillna(value=0.0)

    test_orders_merge_df = pd.merge(test_orders_merge_df, day_reorder_rate, on=['product_id','order_dow'], how = 'left')
    test_orders_merge_df[['day_reorder_rate']]= test_orders_merge_df[['day_reorder_rate']].fillna(value=0.0)

    test_orders_merge_df = pd.merge(test_orders_merge_df, p_days_since_prior_order_reorder_rate, on=['product_id','days_since_prior_order'], how = 'left')
    test_orders_merge_df[['p_days_since_prior_order_reorder_rate']]= test_orders_merge_df[['p_days_since_prior_order_reorder_rate']].fillna(value=0.0)

    test_orders_merge_df = pd.merge(test_orders_merge_df, u_days_since_prior_order_reorder_rate, on=['user_id','days_since_prior_order'], how = 'left')
    test_orders_merge_df[['u_days_since_prior_order_reorder_rate']]= test_orders_merge_df[['u_days_since_prior_order_reorder_rate']].fillna(value=0.0)

    test_orders_merge_df = pd.merge(test_orders_merge_df, days_since_prior_reorder_rate, on=["user_id","product_id",'days_since_prior_order'], how = 'left')
    test_orders_merge_df[['days_since_prior_reorder_rate']]= test_orders_merge_df[['days_since_prior_reorder_rate']].fillna(value=0.0)

    test_orders_merge_df['order_hour_of_day'] = test_orders_merge_df['order_hour_of_day'].apply(hour_tocategorical)

    test_orders_merge_df = test_orders_merge_df[['user_id', 'product_id', 'u_p_order_rate', 'u_p_reorder_rate', 'u_p_avg_position', 'u_p_orders_since_last', 'max_streak', 'user_reorder_rate', 'user_unique_products', 'user_total_products', 'user_avg_cart_size', 'user_avg_days_between_orders', 'user_reordered_products_ratio', 'product_reorder_rate', 'avg_pos_incart', 'p_reduced_feat_1', 'p_reduced_feat_2', 'p_reduced_feat_3', 'department_id', 'order_dow', 'order_hour_of_day', 'days_since_prior_order', 'hour_reorder_rate', 'day_reorder_rate', 'p_days_since_prior_order_reorder_rate', 'u_days_since_prior_order_reorder_rate', 'days_since_prior_reorder_rate', 'order_id']]

    test_orders_merge_df['user_id'] = test_orders_merge_df['user_id'].astype('int32')
    test_orders_merge_df['product_id'] = test_orders_merge_df['product_id'].astype('uint16')
    test_orders_merge_df['u_p_order_rate'] = test_orders_merge_df['u_p_order_rate'].astype('float16')
    test_orders_merge_df['u_p_reorder_rate'] = test_orders_merge_df['u_p_reorder_rate'].astype('float16')
    test_orders_merge_df['u_p_avg_position'] = test_orders_merge_df['u_p_avg_position'].astype('float16')
    test_orders_merge_df['u_p_orders_since_last'] = test_orders_merge_df['u_p_orders_since_last'].astype('int8')
    test_orders_merge_df['max_streak'] = test_orders_merge_df['max_streak'].astype('int8')
    test_orders_merge_df['user_reorder_rate'] = test_orders_merge_df['user_reorder_rate'].astype('float16')
    test_orders_merge_df['user_unique_products'] = test_orders_merge_df['user_unique_products'].astype('int16')
    test_orders_merge_df['user_total_products'] = test_orders_merge_df['user_total_products'].astype('int16')
    test_orders_merge_df['user_avg_cart_size'] = test_orders_merge_df['user_avg_cart_size'].astype('float16')
    test_orders_merge_df['user_avg_days_between_orders'] = test_orders_merge_df['user_avg_days_between_orders'].astype('float16')
    test_orders_merge_df['user_reordered_products_ratio'] = test_orders_merge_df['user_reordered_products_ratio'].astype('float16')
    test_orders_merge_df['product_reorder_rate'] = test_orders_merge_df['product_reorder_rate'].astype('float16')
    test_orders_merge_df['avg_pos_incart'] = test_orders_merge_df['avg_pos_incart'].astype('float16')
    test_orders_merge_df['p_reduced_feat_1'] = test_orders_merge_df['p_reduced_feat_1'].astype('float16')
    test_orders_merge_df['p_reduced_feat_2'] = test_orders_merge_df['p_reduced_feat_2'].astype('float16')
    test_orders_merge_df['p_reduced_feat_3'] = test_orders_merge_df['p_reduced_feat_3'].astype('float16')
    test_orders_merge_df['department_id'] = test_orders_merge_df['department_id'].astype('uint8')
    test_orders_merge_df['order_dow'] = test_orders_merge_df['order_dow'].astype('uint8')
    test_orders_merge_df['order_hour_of_day'] = test_orders_merge_df['order_hour_of_day'].astype('uint8')
    test_orders_merge_df['days_since_prior_order'] = test_orders_merge_df['days_since_prior_order'].astype('uint8')
    test_orders_merge_df['hour_reorder_rate'] = test_orders_merge_df['hour_reorder_rate'].astype('float16')
    test_orders_merge_df['day_reorder_rate'] = test_orders_merge_df['day_reorder_rate'].astype('float16')
    test_orders_merge_df['p_days_since_prior_order_reorder_rate'] = test_orders_merge_df['p_days_since_prior_order_reorder_rate'].astype('float32')
    test_orders_merge_df['u_days_since_prior_order_reorder_rate'] = test_orders_merge_df['u_days_since_prior_order_reorder_rate'].astype('float32')
    test_orders_merge_df['days_since_prior_reorder_rate'] = test_orders_merge_df['days_since_prior_reorder_rate'].astype('float32')
    test_orders_merge_df['order_id'] = test_orders_merge_df['order_id'].astype('int32')

   

    test_orders_merge_df.to_hdf("HDF\\Data_v2.h5", "test", append=True) #1.08GB
    test_orders_merge_df.to_pickle("Pickle\\test_orders_merge_df_v6.pkl") #0.35GB
    test_orders_merge_df.to_csv("CSV\\test_orders_merge_df_v6.csv",index=False) #0.79 GB

    df = pd.read_csv("CSV\\train_orders_merged_df_v6.csv")

    x = os.listdir("CSV")
    for i in x:
        if(i[-3:]=='csv'):
            z = pd.read_csv("CSV\\"+i)
            z.to_pickle('Pickle\\'+i[:-3]+'pkl')
