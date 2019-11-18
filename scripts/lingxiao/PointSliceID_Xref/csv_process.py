#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:39:07 2019

@author: Lingxiao
"""

import sys
import getopt
import os
import shutil
import time
import numpy as np
import pandas as pd
import bsql

check_query_building = "SELECT DISTINCT BuildingSName FROM CEVAC_WAP_IDS; "
query_res_b = bsql.Query(check_query_building).json_list
BUILDING_LIST = np.reshape(query_res_b, len(query_res_b))

check_query_metric = "SELECT distinct Metric FROM CEVAC_TABLES; "
query_res_m = bsql.Query(check_query_metric).json_list
METRIC_LIST = np.reshape(query_res_m, len(query_res_m))

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

def PSID_xref(filename):
    global BUILDING_LIST
    global METRIC_LIST

    df = pd.read_csv(filename, header=0)
    df = df.dropna(axis=0, how='all')
    
    total_header = ['PointSliceID', 'Room','RoomType','ObjectName','BLG','Floor','ReadingType','Alias','Com','DeCom']
    
    #null_df = pd.DataFrame(np.full((len(df),len(total_header)), 'NULL'),columns = total_header) 
    null_df = pd.DataFrame(columns = total_header)

    df = pd.concat([df,null_df],ignore_index=True,sort=False)    
    df.name = filename.split('/')[-1][:-4].upper()    
    core_df = df[['PointSliceID','Room','RoomType','Floor','ReadingType','Alias']] 
    '''
    error_rows = []
    for i in range(len(core_df)):
        for j in core_df.iloc[i]:
            if j=='NULL':
                error_rows.append(i)
                break
    '''
    error_rows = core_df[core_df.isnull().values==True]
    
    if(len(error_rows)):
        #print('Null value in row: ',[i+1 for i in error_rows])
        print('Null value in row: ')
        print(error_rows)
        sys.exit()
        
    if(len(df[df.duplicated('PointSliceID')])):
        print('duplicated value in PointsliceID: ')
        print(core_df[df.duplicated('PointSliceID')])
        sys.exit()

    '''    
    build_name = (df.name).split('_')[1]
    metric_name = (df.name).split('_')[2]

    check_query_building = "SELECT BuildingSName FROM CEVAC_BUILDING_INFO; "
    query_res_b = bsql.Query(check_query_building).json_list
    building_list = np.reshape(query_res_b, len(query_res_b))
    
    check_query_metric = "SELECT Metric FROM CEVAC_METRIC; "
    query_res_m = bsql.Query(check_query_metric).json_list
    metric_list = np.reshape(query_res_m, len(query_res_m))
    
    
    if build_name not in building_list:
        sys.exit('Error in Building name, please check. ')
        
    if metric_name not in metric_list:
        sys.exit('Error in Metric name, please check. ')
    '''
    
    head_str = ["IF OBJECT_ID('",df.name,"') IS NOT NULL DROP TABLE ", df.name,";\n", "GO\n", "USE [WFIC-CEVAC]\n","CREATE TABLE [dbo].[",df.name,"](\n",\
        "[PointSliceID] [int] NOT NULL,\
        [Room] [nvarchar](MAX) NULL,\
        [RoomType] [nvarchar](MAX) NULL,\
        [ObjectName] [nvarchar](MAX) NOT NULL,\
        [BLG] [nvarchar](50) NOT NULL,\
        [Floor] [nvarchar](50) NULL,\
        [ReadingType] [nvarchar](50) NOT NULL,\
        [Alias] [nvarchar](MAX) NOT NULL,\
        [Com] [datetime] NULL,\
        [DeCom] [datetime] NULL,\n",\
        "CONSTRAINT [PK_",df.name,"] PRIMARY KEY CLUSTERED",\
        "\n(\n[PointSliceID] ASC\n)\n",\
        "WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]\n)\n ON [PRIMARY]\nGO\n"
            ]

    new_file_path = "/cevac/cache/"    
    new_filename = new_file_path + ('create_'+df.name).upper()+'.sql'
    with open(new_filename,'w') as sql_f:
        sql_f.writelines(head_str)
            
        for i in range(len(df)):
            insert_str = ['INSERT INTO ', df.name ,' (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (\n',\
                "'",str(int(df.iloc[i]['PointSliceID'])),"'",',',\
                "'",str(df.iloc[i]['Room']),"'",',',\
                "'",str(df.iloc[i]['RoomType']),"'",',',\
                "'",str(df.iloc[i]['ObjectName']),"'",',',\
                "'",str(df.iloc[i]['BLG']),"'",',',\
                "'",str(df.iloc[i]['Floor']),"'",',',\
                "'",str(df.iloc[i]['ReadingType']),"'",',',\
                "'",str(df.iloc[i]['Alias']),"'",',',\
                "'",str(df.iloc[i]['Com']),"'",',',\
                "'",str(df.iloc[i]['DeCom']),"'",\
                    ');',\
                    '\nGO\n']
            for j in range(len(insert_str)):
                if insert_str[j]=="nan":
                    insert_str[j-1]=""
                    insert_str[j]='NULL'
                    insert_str[j+1]=""
            sql_f.writelines(insert_str)
            #print(''.join(insert_str))
        sql_f.close()
        
        print(len(df), "lines have been written in: ", new_filename)
        return new_filename
    
def WAP_xref(filename):
    global BUILDING_LIST
    global METRIC_LIST
    global WAP_IDS_DICT

    df = pd.read_csv(filename, header=0)
    df = df.dropna(axis=0, how='all')
    print(df.columns)
    
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

    error_rows = df[df.isnull().values==True]
    
    if(len(error_rows)):
        #print('Null value in row: ',[i+1 for i in error_rows])
        print('Null value in row: ')
        print(error_rows)
        sys.exit()
        
    if(len(df[df.duplicated('WAP_Name')])):
        print('duplicated value in WAP_Name: ')
        print(df[df.duplicated('WAP_Name')])
        sys.exit()
    
    '''
    build_name = (df.name).split('_')[1]
    metric_name = (df.name).split('_')[2]

    check_query_building = "SELECT DISTINCT BuildingSName FROM CEVAC_WAP_IDS; "
    query_res_b = bsql.Query(check_query_building).json_list
    building_list = np.reshape(query_res_b, len(query_res_b))
    
    if build_name not in building_list:
        sys.exit('Error in Building name, this building name is not included in CEVAC_WAP_IDS, please check. ')
    
    check_query_names = "SELECT WAP_Name FROM CEVAC_WAP_IDS; "
    check_query_data = "SELECT WAP_ID, BuildingSName FROM CEVAC_WAP_IDS; "
    query_res_n = bsql.Query(check_query_names)
    query_res_d = bsql.Query(check_query_data)
    
    total_wap_name = query_res_n.json_list
    wap_name_list = np.reshape(total_wap_name, len(total_wap_name))
    total_data = query_res_d.json_list
    
    for i in range(len(wap_name_list)):
        wap_name_list[i] = ''.join((wap_name_list[i].split()))
    
    WAP_IDS_dict = dict(zip(wap_name_list, total_data))
    '''
    df['WAP_ID'] = None   
    for i in range(len(df)):
        temp_wap_name = df['WAP_Name'][i]
        df['WAP_ID'][i] = WAP_IDS_DICT[temp_wap_name][0]
    
    head_str = f"IF OBJECT_ID('{df.name}') IS NOT NULL DROP TABLE {df.name};\n \
GO\n \
USE [WFIC-CEVAC]\n CREATE TABLE [dbo].[{df.name}](\n \
[WAP_ID] INT PRIMARY KEY, [WAP_Name] NVARCHAR (100) NOT NULL, [Room] NVARCHAR (50) NOT NULL, \
[Floor] NVARCHAR (50) NOT NULL, [Alias] NVARCHAR (50) NOT NULL \
)\n \
GO\n \
"

    new_file_path = "/cevac/cache/"    
    new_filename = new_file_path + ('create_'+df.name).upper()+'.sql'
    with open(new_filename,'w') as sql_f:
        sql_f.write(head_str)
            
        for i in range(len(df)):
            insert_str = f"INSERT INTO {df.name} (WAP_ID,WAP_Name,Room,Floor,Alias) \
VALUES ({df.iloc[i]['WAP_ID']},'{str((df.iloc[i]['WAP_Name']))}','{str(df.iloc[i]['Room'])}', \
'{str(df.iloc[i]['Floor'])}','{' '.join(str(df.iloc[i]['Alias']).split())}');\n \
GO\n"
            sql_f.write(insert_str)
        sql_f.close()
        
        print(len(df), "lines have been written in: ", new_filename)
        return new_filename
        
def rename_raw_csv(filename):
    file_path = "/cevac/xref/"
    
    now_time = time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))
    new_csv_filename = file_path + filename.split('/')[-1][:-4].upper() + '_' + now_time + '.csv'
    shutil.move(filename, new_csv_filename)
    return new_csv_filename

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
    #use command line to do the double check
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
    
    return {'metric': metric, 'buidling_name': building_name}


def check_attr(filename, metric_web, building_web):
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
    
    #filename = str(sys.argv[1])
    #metric = (filename.split('/')[-1][:-4].upper()).split('_')[2]
    if(check_attr(filename, metric, building)):
        print("Metric $ Builiding check pass")

    if (metric == 'WAP'):
        print('Dealing with WAP_xref\n')
        new_sql = WAP_xref(filename)
    else:
        print('Dealing with PSID_xref\n')
        new_sql = PSID_xref(filename)
        
    if(new_sql):
        new_csv_filename = rename_raw_csv(filename)
        if(new_csv_filename):
            print("csv file rename success, new filename: ", new_csv_filename)            
        else:
            print("fail to rename csv file")
            
        cmd = "/cevac/scripts/exec_sql_script.sh " + new_sql
        os.system(cmd)
        os.remove(new_sql)
        print("All done")        
    else:
        print("fail")

if __name__ == '__main__':
    main(sys.argv[1:])