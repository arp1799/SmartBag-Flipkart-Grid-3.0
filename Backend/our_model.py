
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from catboost import CatBoostClassifier, Pool
import xgboost as xgb

from f1optimization_faron import get_best_prediction

from sklearn.tree import DecisionTreeClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score , log_loss

from datetime import datetime
from tqdm import tqdm
import pickle

def random_split(test_size = 0.1):

  train_y = train_data['reordered'].values.tolist()
  train_x = train_data.drop(['user_id', 'product_id', 'order_id', 'reordered'], axis = 1)

  X_train, X_val, y_train, y_val = train_test_split(train_x, train_y, stratify=train_y, test_size=0.1, random_state = 42)

  return (X_train, y_train),(X_val, y_val)





def train_catboost(X_train, X_test, y_train, y_test, save = True, file_name = None):
    

    start_time = datetime.now()
    print("Training Started :")

    c_model = CatBoostClassifier(task_type = "GPU",verbose=True,depth = 13, iterations= 100,learning_rate= 0.02,scale_pos_weight= 1.0)
    c_model.fit(X_train,y_train)
    print("Training Completed ")
    end_time = datetime.now()
    difference = end_time - start_time
    time = divmod(difference.total_seconds() , 3600)
    print("Total Time : {} hours {} seconds".format(time[0], time[1]))
    
    predict_y = c_model.predict_proba(X_test)
    print("The Test log loss is:",log_loss(y_test, predict_y, labels=[0,1], eps=1e-15))
    
    predict_y = predict_y[:,-1]
    
    if save:
        # save
        pickle.dump(c_model, open(file_name, "wb"))


    return c_model, predict_y



def fun_train():
  global train_data, test_data

  data = pd.HDFStore("HDF\\Data_v2.h5")

  train_data = data['train']
  test_data  = data['test']
  train_data = train_data[['user_id', 'product_id', 'u_p_order_rate', 'u_p_reorder_rate',        'u_p_avg_position', 'u_p_orders_since_last', 'max_streak',        'user_reorder_rate', 'user_unique_products', 'user_total_products',        'user_avg_cart_size', 'user_avg_days_between_orders',        'user_reordered_products_ratio', 'product_reorder_rate',        'avg_pos_incart', 'p_reduced_feat_1', 'p_reduced_feat_2',        'p_reduced_feat_3', 'department_id', 'days_since_prior_order',        'days_since_prior_reorder_rate', 'reordered', 'order_id']]
  test_data = test_data[['user_id', 'product_id', 'u_p_order_rate', 'u_p_reorder_rate',        'u_p_avg_position', 'u_p_orders_since_last', 'max_streak',        'user_reorder_rate', 'user_unique_products', 'user_total_products',        'user_avg_cart_size', 'user_avg_days_between_orders',        'user_reordered_products_ratio', 'product_reorder_rate',        'avg_pos_incart', 'p_reduced_feat_1', 'p_reduced_feat_2',        'p_reduced_feat_3', 'department_id', 'days_since_prior_order',        'days_since_prior_reorder_rate', 'order_id']]

  (X_train, y_train),(X_val, y_val) = random_split(test_size = 0.1)
  c_model, predict_y = train_catboost(X_train, X_val, y_train, y_val, save = True, file_name = 'Pickle\\catboost_v3.pkl' )
  
  data.close()
