import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import time
from datetime import datetime
import pickle
import warnings

from file_generate import *
from Clustering import *

def fun_main(user_id):
    cluster_id = 0

    warnings.filterwarnings('ignore')

    departments = pd.read_csv("Dataset\\departments.csv")
    previous_orders_data = pd.read_csv("Dataset\\previous_orders_data.csv")
    training_orders_data = pd.read_csv("Dataset\\training_orders_data.csv")
    orders = pd.read_csv("Dataset\\orders.csv")
    products = pd.read_csv("Dataset\\products.csv")

    x = orders['user_id'].unique()

    if user_id not in x:
        cluster_id = -1
        print("cluster_id =>", cluster_id)

    products_desc = pd.merge(products, departments, on = 'department_id', how = 'left')

    products_desc[products_desc['department']=='missing']

    products_desc[products_desc['department']=='snacks']


    pickle.dump(products_desc, open("Pickle\\products_desc.p", "wb"))


    merged_order_products = pd.merge(training_orders_data, previous_orders_data, how = 'outer')


    products_per_order = merged_order_products.groupby('order_id').count()


    order_products_desc = pd.merge(merged_order_products, products_desc, on = 'product_id')


    merged_orders = pd.merge(orders, order_products_desc, on = 'order_id')

    test = orders[orders['eval_set']=='test']

    pickle.dump(merged_orders, open("Pickle\\merged_orders.p", "wb"))

    return cluster_id

def call(x):
    
    print("USER_ID: ", x)
    
    cluster_id = fun_main(x)

    if cluster_id != -1:
        cluster_id = fun_clustering(x)
    return(fun_main2(x,cluster_id))

# call(4)