
import pandas as pd
import pickle
import numpy as np
from feature_eng import *
from our_model import *
from predictions import *

def fun_addi(cluster_id):


   product_mappings = pd.read_csv("Dataset\\products.csv")
   product_mappings = product_mappings[['product_id','product_name']]
   product_mappings.to_pickle("Pickle\\product_mappings.pkl")

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

   prior_train_orders = prior_order.sort_values(by=['order_id'])
   prior_train_orders = pd.merge(left = prior_train_orders, right = products,
                              left_on='product_id', right_on='product_id').sort_values(by=['order_id']).reset_index(drop=True)
   prior_train_orders = pd.merge(left = prior_train_orders, right = departments,
                              left_on='department_id', right_on='department_id').sort_values(by=['order_id']).reset_index(drop=True)
   prior_train_orders = pd.merge(left = prior_train_orders, right = orders,
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

   prior_train_orders = prior_train_orders[col_order]


   x = prior_train_orders.groupby(['product_id','order_dow','order_hour_of_day','product_name'])['product_name'].size().reset_index(name = 'count').sort_values(
      by=['order_dow','order_hour_of_day','count'], ascending = False)
   top10 = x.groupby(['order_dow','order_hour_of_day']).head(10).reset_index(drop = True)
   # print(top10)
   top10.to_pickle("Pickle\\top10_products.pkl")

   user_last_purchase = pd.DataFrame(columns = ['user_id','date'])
   user_last_purchase['user_id'] = orders['user_id'].unique()
   user_last_purchase['date'] = '2021-03-21'

   user_last_purchase.to_pickle("Pickle\\user_last_purchase.pkl")


def fun_main2(X, cluster_id):
   fun_addi(cluster_id)
   fun_FE(cluster_id)
   fun_train()
   return(get_recommendations({"user_id":X}))

