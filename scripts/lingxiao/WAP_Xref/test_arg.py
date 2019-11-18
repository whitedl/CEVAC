# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:08:48 2019

@author: suppe
"""

import sys
import getopt

def main(argv):
    filename = ''
    username = ''
    password = ''
    
    try:
        opts, args = getopt.getopt(argv, "f:u:p:", ["filename=", "username=", "password="])
        
        """
            options, args = getopt.getopt(args, shortopts, longopts=[])
            
            参数args：一般是sys.argv[1:]。过滤掉sys.argv[0]，它是执行脚本的名字，不算做命令行参数。
            参数shortopts：短格式分析串。例如："hp:i:"，h后面没有冒号，表示后面不带参数；p和i后面带有冒号，表示后面带参数。
            参数longopts：长格式分析串列表。例如：["help", "ip=", "port="]，help后面没有等号，表示后面不带参数；ip和port后面带冒号，表示后面带参数。
            
            返回值options是以元组为元素的列表，每个元组的形式为：(选项串, 附加参数)，如：('-i', '192.168.0.1')
            返回值args是个列表，其中的元素是那些不含'-'或'--'的参数。
        """
        
    except getopt.GetoptError:
        print("Error: test_arg.py -u <username> -p <password>")
        print("  or: test_arg.py --username=<username> --password=<password>")
        sys.exit()
        
    #print(opts)
    for opt, arg in opts:
        if (opt in ('-f', '--filename')):
            filename = arg
            
        elif (opt in ('-u', '--username')):
            username = arg
            
        elif (opt in ('-p', '--password')):
            password = arg
    
    print("this is opts: ", opts)
    print("this is args: ", args)
    
if __name__ == "__main__":
    main(sys.argv[1:])