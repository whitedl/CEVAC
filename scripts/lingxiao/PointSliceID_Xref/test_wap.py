# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 10:53:54 2019

@author: suppe
"""

import numpy as np
import pandas as pd
import sys
import bsql
import getopt

check_query_names = "SELECT WAP_Name FROM CEVAC_WAP_IDS; "
check_query_data = "SELECT WAP_ID, BuildingSName FROM CEVAC_WAP_IDS; "
query_res_n = bsql.Query(check_query_names)
query_res_d = bsql.Query(check_query_data)
    
total_wap_name = query_res_n.json_list
wap_name_list = np.reshape(total_wap_name, len(total_wap_name))
total_data = query_res_d.json_list
    
for i in range(len(wap_name_list)):    
    wap_name_list[i] = ''.join((wap_name_list[i].split()))
    
WAP_IDS_DICT = dict(zip(wap_name_list, total_data))

check_query_building = "SELECT DISTINCT BuildingSName FROM CEVAC_WAP_IDS; "
query_res_b = bsql.Query(check_query_building).json_list
BUILDING_LIST = np.reshape(query_res_b, len(query_res_b))

check_query_metric = "SELECT distinct Metric FROM CEVAC_TABLES; "
query_res_m = bsql.Query(check_query_metric).json_list
METRIC_LIST = np.reshape(query_res_m, len(query_res_m))


def wap_xref(filename):
    global WAP_IDS_DICT
    global BUILDING_LIST
    
    df = pd.read_csv(filename, header=0)
    df = df.dropna(axis=0, how='all')
    print(df.columns)
    
    '''
    meta_col_name = ['NAME', 'ROOM','FLOOR','ALIAS']
    total_header = ['WAP_Name','Room','Floor','Alias']
    test_header = []
    for i in range(len(df.columns)):
        if meta_col_name[i] not in df.columns[i].upper():
            print(meta_col_name[i], df.columns[i].upper())
        else:
            test_header.append(total_header[i])
    print(test_header)
    '''
    
    core_df = ['WAP_Name','Room','Floor','Alias']
    
    if (len(df.columns)==4):
        df.columns = core_df
    else:
        print('unexpected columns')
        sys.exit()
    
    print(df.columns)
    
    null_df = pd.DataFrame(columns = core_df)
    df = pd.concat([df,null_df],ignore_index=True,sort=False)
    
    df.name = filename.split('/')[-1][:-4].upper()
    build_name = (df.name).split('_')[1]
    metric_name = (df.name).split('_')[2]
    print(metric_name)
    print(df.name)
    
    #print(df.head)
    
    df['WAP_ID'] = None
    
    
    df['WAP_ID'] = None
    
    for i in range(len(df)):
        temp_wap_name = df['WAP_Name'][i]
        temp_wap_id = int(WAP_IDS_DICT[temp_wap_name][0])
        df['WAP_ID'][i] = temp_wap_id
    
    print(df.head)
    
    if (metric_name=='WAP'):
        head_str = f"IF OBJECT_ID('{df.name}') IS NOT NULL DROP TABLE '{df.name}';\n \
GO\n \
USE [WFIC-CEVAC]\n CREATE TABLE [dbo].[{df.name}](\n \
[WAP_ID] INT PRIMARY KEY, [WAP_Name] NVARCHAR (100) NOT NULL, [Room] NVARCHAR (50) NOT NULL, \
[Floor] NVARCHAR (50) NOT NULL, [Alias] NVARCHAR (50) NOT NULL \
)\n \
GO\n \
"
        print (head_str)
    '''
    print('------------------')
    i=30
    insert_str = ['INSERT INTO ', df.name ,' (WAP_Name,Room,Floor,Alias) VALUES (\n',\
                  "'",str((df.iloc[i]['WAP_Name'])),"'",',',\
                  "'",str(df.iloc[i]['Room']),"'",',',\
                  "'",str(df.iloc[i]['Floor']),"'",',',\
                  "'",str(df.iloc[i]['Alias']),"'",\
                  ');',\
    '\nGO\n']
    
    print(''.join(insert_str))
    '''
    new_filename = ('create_'+df.name).upper()+'.sql'
    with open(new_filename,'w') as sql_f:
        sql_f.write(head_str)
            
        for i in range(len(df)):
            insert_str_test = f"INSERT INTO CEVAC_WATT_WAP_XREF (WAP_ID,WAP_Name,Room,Floor,Alias) \
VALUES ({df.iloc[i]['WAP_ID']},'{str((df.iloc[i]['WAP_Name']))}','{str(df.iloc[i]['Room'])}', \
'{str(df.iloc[i]['Floor'])}','{' '.join(str(df.iloc[i]['Alias']).split())}');\n \
GO\n"
            sql_f.write(insert_str_test)
        sql_f.close()
    print("---------------")
    print(insert_str_test)


def init_func(filename):
    metric = (filename.split('/')[-1][:-4].upper()).split('_')[2]
    if (metric=='WAP'):
        wap_xref(filename)
        print("all done")
    else:
        print(metric)

def get_attr(filename):
    global WAP_IDS_DICT
    global BUILDING_LIST
    global METRIC_LIST
    
    metric = 'NULL'
    building_name = 'NULL'
    
    meta_list = (filename.split('/')[-1][:-4].upper()).split('_')
    
    '''
    for i in range(len(meta_list)):
        if (meta_list[i] in METRIC_LIST):
            metric = meta_list[i]
            building_name = '_'.join(meta_list[1:i])
            break
    '''
#use command line to solve this
    xref_index = meta_list.index('XREF')
    
    for i in range(1,xref_index):
        if ('_'.join(meta_list[xref_index-i:xref_index]) in METRIC_LIST):
            metric = '_'.join(meta_list[xref_index-i:xref_index])
            building_name = '_'.join(meta_list[1:xref_index-i])
            break
            
    if (metric == 'NULL'):
        print("Wrong metric name in filename: ", metric)
        sys.exit()
    elif (building_name not in BUILDING_LIST):
        print("Wrong building name in file: ", building_name)
        sys.exit()
    
    return {'metric': metric, 'building_name': building_name}

def check_attr(filename, metric_web, building_web):
    print("Start checking attributes ...")
    check_dict = get_attr(filename)
    if (metric_web != check_dict['metric']):
        print("The metric you choose doesn't match your filename, please check.")
        sys.exit()
    elif (building_web != check_dict['building_name']):
        print("The building name you choose doesn't match your filename, please check.")
        sys.exit()
    return 1

def main(argv):
    filename = ''
    metric = ''
    building = ''
    age = ''
    
    try:
        opts, args = getopt.getopt(argv, "f:m:b:a:", ["filename=", "metric=", "building=", "age="])

    except getopt.GetoptError:
        print("Error: csv_process.py -f <filename> -m <metric> -b <building> -a <age>")
        print(" or: csv_process.py --filename=<filename> --metric=<metric> --building=<building> --age=<age>")
        sys.exit(2)

    for opt, arg in opts:
        if (opt in ('-f', '--filename')):
            filename = arg.upper()
        elif (opt in ('-m', '--metric')):
            metric = arg.upper()
        elif (opt in ('-b', '--building')):
            building = arg.upper()
        elif (opt in ('-a', 'age')):
            age = arg.upper()
    
    print("input_filename: ", filename)
    print("input_metric: ", metric)
    print("input_buiding: ", building)
    #filename = str(sys.argv[1])
    #metric = (filename.split('/')[-1][:-4].upper()).split('_')[2]
    if(check_attr(filename, metric, building)):
        print("Metric $ Builiding check pass")

if __name__ == '__main__':
    main(sys.argv[1:])

