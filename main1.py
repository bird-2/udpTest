# -*- coding: utf-8 -*-
#getopt是一个命令行选项解析器,getopt是getopt这个包里面的函数，因此需要引入getopt和sys这两个包
#取得命令行参数，在使用之前，首先要取得命令行参数，使用sys模块可以得到命令行参数
import getopt
import sys
#从主函数中引入roleobject函数
from main import roleobject

if __name__ == '__main__':
    try:
        #getopt.getopt()解析命令行选项与形参列表。 args 为要解析的参数列表，不包含最开头的对正在运行的程序的引用。
        # 通常这意味着 sys.argv[1:]， shortopts 为脚本所要识别的字母选项，包含要求后缀一个冒号 (':') 的选项
        #从外部输入不同的命令行选项时，对应执行不同的功能
        #udp是用u表示，用命令python ./main1.py -u表示，后面通过不同的命令来执行不同的功能，（可选，根据在main()函数里面的role选择）-s表示服务器端，-c表示客户端
        opts, args = getopt.getopt(sys.argv[1:], "ps:u:",
                                   ["udp="])
        for opt, arg in opts:
            if opt == "-u" or opt == "--udp":
                print("udp")
                roleobject(arg)
    except getopt.GetoptError:
        print("argv error,please input")
        exit(-1)

#"spy", "scanner=", "send=",  , "msg="