#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 09:39:07 2019

@author: Lingxiao
"""

import sys
import os
import shutil
import time
import numpy as np
import pandas as pd
import bsql

'''
import win32ui 
dOpen = 1
filename_filter = "Filetype (*.csv)|*.csv||"
dlg = win32ui.CreateFileDialog(1 if dOpen else 0, None, None, 1, filename_filter, None) 
dlg.SetOFNInitialDir("D:\ ")
dlg.DoModal()
filename = dlg.GetPathName()
'''
def WAP_xref(filename):
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
    
    '''
    error_rows = []
    for i in range(len(core_df)):
        for j in core_df.iloc[i]:
            if j=='NULL':
                error_rows.append(i)
                break
    '''
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
    
    WAP_IDS_dict = dict(zip(wap_name_list, total_data))
    
    df['WAP_ID'] = None
    
    for i in range(len(df)):
        temp_wap_name = df['WAP_Name'][i]
        temp_wap_id = WAP_IDS_dict[temp_wap_name][0]
        df['WAP_ID'][i] = temp_wap_id
    
    if (metric_name=='WAP'):
         head_str = f"IF OBJECT_ID('{df.name}') IS NOT NULL DROP TABLE '{df.name}';\n \
GO\n \
USE [WFIC-CEVAC]\n CREATE TABLE [dbo].[{df.name}](\n \
[WAP_Name] NVARCHAR (100) NOT NULL, [Room] NVARCHAR (50) NOT NULL, \
[Floor] NVARCHAR (50) NOT NULL, [Alias] NVARCHAR (50) NOT NULL, \
CONSTRAINT [CEVAC_WAP_IDS] PRIMARY KEY (WAP_ID)\n \
)\n \
GO\n \
"

    new_file_path = "/cevac/cache/"    
    new_filename = new_file_path + ('create_'+df.name).upper()+'.sql'
    with open(new_filename,'w') as sql_f:
        sql_f.write(head_str)
            
        for i in range(len(df)):
            insert_str = f"INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias)\
            VALUES ('{str((df.iloc[i]['WAP_Name']))}','{str(df.iloc[i]['Room'])}', \
            '{str(df.iloc[i]['Floor'])}','{str(df.iloc[i]['Alias'])}');\n \
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

    
    
if __name__ == '__main__':
    filename = str(sys.argv[1])
    #filename = file_path + filename
    #filename = input("filename: ")   
    metric = (filename.split('/')[-1][:-4].upper()).split('_')[2]
    if (metric == 'WAP'):
        print('Dealing with WAP_XREF')
        wap_xref(filename)
    else:
        print(metric)
    new_sql = wap_xref(filename)
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
