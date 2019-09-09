# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 12:45:14 2019

@author: cs
"""

import tkinter as tk
from math import exp,log,sin,cos,tan

import re
window= tk.Tk()
window.title('计算器')


equation,result=tk.StringVar(),tk.StringVar()

lb1=tk.Label(window,text='请输入表达式：')
lb1.pack()

entry1=tk.Entry(window,textvariable=equation)
entry1.pack()

lb2=tk.Label(window,text='输出结果:')
lb2.pack()


entry2=tk.Entry(window,textvariable=result)
entry2.pack()

def eq_format(eq):
    '''
    :param eq: 输入的算式字符串
    :return: 格式化以后的列表，如['60','+','7','*','8']
    '''
    format_list = re.findall('[\d\.]+|\(|\+|\-|\*|\/|\)',eq)
    return format_list
 
def change(eq,count):
    '''
    :param eq: 刚去完括号或者乘除后的格式化列表
    :param count: 发生变化的元素的索引
    :return: 返回一个不存在 '+-' ,'--'类的格式化列表
    '''
    if eq[count] == '-':
        if eq[count-1] == '-':
            eq[count-1] = '+'
            del eq[count]
        elif eq[count-1] == '+':
            eq[count-1] = '-'
            del eq[count]
    return eq
 
 
def remove_multiplication_division(eq):
    '''
    :param eq: 带有乘除号的格式化列表
    :return: 去除了乘除号的格式化列表
    '''
    count = 0
    for i in eq:
        if i == '*':
            if eq[count+1] != '-':
                eq[count-1] = float(eq[count-1]) * float(eq[count+1])
                del(eq[count])
                del(eq[count])
            elif eq[count+1] == '-':
                eq[count] = float(eq[count-1]) * float(eq[count+2])
                eq[count-1] = '-'
                del(eq[count+1])
                del(eq[count+1])
            eq = change(eq,count-1)
            return remove_multiplication_division(eq)
        elif i == '/':
            if eq[count+1] != '-':
                eq[count-1] = float(eq[count-1]) / float(eq[count+1])
                del(eq[count])
                del(eq[count])
            elif eq[count+1] == '-':
                eq[count] = float(eq[count-1]) / float(eq[count+2])
                eq[count-1] = '-'
                del(eq[count+1])
                del(eq[count+1])
            eq = change(eq,count-1)
            return remove_multiplication_division(eq)
        count = count + 1
    return eq
 
 
def remove_plus_minus(eq):
    '''
    :param eq: 只带有加减号的格式化列表
    :return: 计算出整个列表的结果
    '''
    count = 0
    if eq[0] != '-':
        sum = float(eq[0])
    else:
        sum = 0.0
    for i in eq:
        if i == '-':
            sum = sum - float(eq[count+1])
        elif i == '+':
            sum = sum + float(eq[count+1])
        count = count + 1
    if sum >= 0:
        eq = [str(sum)]
    else:
        eq = ['-',str(-sum)]
    return eq
 
def calculate(s_eq):
    '''
    :param s_eq: 不带括号的格式化列表
    :return: 计算结果
    '''
    if '*' or '/' in s_eq:
        s_eq = remove_multiplication_division(s_eq)
    if '+' or '-' in s_eq:
        s_eq = remove_plus_minus(s_eq)
    return s_eq
 
 
def simplify(format_list):
    '''
    :param format_list: 输入的算式格式化列表如['60','+','7','*','8']
    :return: 通过递归去括号，返回简化后的列表
    '''
 
    bracket = 0     # 用于存放左括号在格式化列表中的索引
    count = 0
    for i in format_list:
        if i == '(':
            bracket = count
        elif i == ')':
            temp = format_list[bracket + 1 : count]
            # print(temp)
            new_temp = calculate(temp)
            format_list = format_list[:bracket] + new_temp + format_list[count+1:]
            format_list = change(format_list,bracket)     # 解决去括号后会出现的--  +- 问题
            return simplify(format_list)            # 递归去括号
        count = count + 1
    return format_list                     # 当递归到最后一层的时候，不再有括号，因此返回列表
 
 
def caculator(eq):
    format_list = eq_format(eq)
    s_eq = simplify(format_list)
    ans = calculate(s_eq)
    if len(ans) == 2:
        ans = -float(ans[1])
    else:
        ans = float(ans[0])
    return ans
 
 



def getnum(num):
    temp = equation.get( )
    temp2 = result.get( )
    print(temp)
    print(temp2)
    if temp2 != ' ' :
        temp = '0'
        temp2 = ' '
        result.set(temp2)
    if (temp=='0'):
        temp = ''
    temp = temp + num
    equation.set( temp )
    print(equation)


def run( ):
    temp = equation.get( )
    temp = temp.replace('x','*')             # 为了方便后续调用caculator函数进行运算，因此进行符号处理
    temp = temp.replace('÷','/')             # 为了方便后续调用caculator函数进行运算，因此进行符号处理
    # 写一个小彩蛋，可以用于表白哦
    if temp == '5+2+0+1+3+1+4':               # 暗号
        result.set('xxx我爱你')               # 彩蛋或者表白语
        return 0
    print(temp)
    answer =caculator(temp)
    answer = '%.2f'%answer                   # 设定结果的小数点个数，可自定义
    result.set(str(answer))

def clear( ):
    equation.set('0')
    result.set(' ')

frame1=tk.Frame(window)
frame1.pack()  
op=[[1,2,3,'+'],[4,5,6,'-'],[7,8,9,'*'],[0,'.','=','/'],['(',')','exp','log'],['sin','cos','tan','clear']]    


button_1=tk.Button(frame1,text='1',command= lambda : getnum('1'))
button_1.grid(row=0,column=0)

button_2=tk.Button(frame1,text='2',command= lambda : getnum('2'))
button_2.grid(row=0,column=1)

button_3=tk.Button(frame1,text='3',command= lambda : getnum('3'))
button_3.grid(row=0,column=2)

button_add=tk.Button(frame1,text='+',command= lambda : getnum('+'))
button_add.grid(row=0,column=3)

button_4=tk.Button(frame1,text='4',command= lambda : getnum('4'))
button_4.grid(row=1,column=0)

button_5=tk.Button(frame1,text='5',command= lambda : getnum('5'))
button_5.grid(row=1,column=1)

button_6=tk.Button(frame1,text='6',command= lambda : getnum('6'))
button_6.grid(row=1,column=2)

button_minus=tk.Button(frame1,text='-',command= lambda : getnum('-'))
button_minus.grid(row=1,column=3)

button_7=tk.Button(frame1,text='7',command= lambda : getnum('7'))
button_7.grid(row=2,column=0)

button_8=tk.Button(frame1,text='8',command= lambda : getnum('8'))
button_8.grid(row=2,column=1)

button_9=tk.Button(frame1,text='9',command= lambda : getnum('9'))
button_9.grid(row=2,column=2)

button_mult=tk.Button(frame1,text='*',command= lambda : getnum('*'))
button_mult.grid(row=2,column=3)

button_0=tk.Button(frame1,text='0',command= lambda : getnum('0'))
button_0.grid(row=3,column=0)

button_point=tk.Button(frame1,text='.',command= lambda : getnum('.'))
button_point.grid(row=3,column=1)

button_equal=tk.Button(frame1,text='=',command=run)
button_equal.grid(row=3,column=2)

button_div=tk.Button(frame1,text='/',command= lambda : getnum('/'))
button_div.grid(row=3,column=3)

button_lbracket=tk.Button(frame1,text='(',command= lambda : getnum('('))
button_lbracket.grid(row=4,column=0)

button_rbracket=tk.Button(frame1,text=')',command= lambda : getnum(')'))
button_rbracket.grid(row=4,column=1)

button_exp=tk.Button(frame1,text='exp',command= lambda : getnum('exp'))
button_exp.grid(row=4,column=2)

button_log=tk.Button(frame1,text='log',command= lambda : getnum('log'))
button_log.grid(row=4,column=3)

button_sin=tk.Button(frame1,text='sin',command= lambda : getnum('sin'))
button_sin.grid(row=5,column=0)

button_cos=tk.Button(frame1,text='cos',command= lambda : getnum('cos'))
button_cos.grid(row=5,column=1)

button_tan=tk.Button(frame1,text='tan',command= lambda : getnum('tan'))
button_tan.grid(row=5,column=2)

button_clear=tk.Button(frame1,text='clear',command=clear)
button_clear.grid(row=5,column=3)
window.mainloop()
