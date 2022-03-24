import imp
import json
import math
import os

from numpy import mat


def v_belt_design(filename, params):
    # 加载数据
    p = params['P_in']
    ka = params['K_A']
    nm = params['n_m']
    d_d1_min = params['d_d1'][0]
    d_d1_max = params['d_d1'][1]
    i = params['i']
    belt_type = params['belt_type']
    P1 = params['P1']
    d_P1 = params['delta_P1']
        
    f = open(filename, 'a')
    f.write('\t\t########## V带设计 ##########\n\n')
    
    f.write('\n######## 确定计算功率 ########\n')
    l_d_list = [[630, 0.81], [700, 0.83], [790, 0.85], [890, 0.87], [990, 0.89], 
                [1100, 0.91], [1250, 0.93], [1430, 0.96], [1640, 0.99], [1750, 1.00], 
                [1940, 1.02], [2050, 1.04], [2200, 1.06], [2300, 1.07], [2480, 1.09], [2700, 1.10]]
    pc = ka * p
    f.write("计算功率Pc为：{0:.3f}kW\n".format(pc))
    d_d1_max = float(d_d1_max)
    d_d1_min = float(d_d1_min)
    
    
    f.write('\n######## 选择带型 ########\n')
    f.write('选择带型为{0}型，选择小带轮直径为{1} ~ {2}mm\n'.format(belt_type, d_d1_min, d_d1_max))
    d_d1_mean = (d_d1_max + d_d1_min) / 2
    d_d2 = i * d_d1_mean * (1 - 0.01)
    res = d_d2 % 5
    if (res / 5 < 0.5):
        d_d2 = d_d2 - res
    else:
        d_d2 = d_d2 + 5 - res
    
    
    f.write('\n######## 确定带轮直径和带速 #########\n')
    f.write("小带轮直径d1为：{}mm\n".format(d_d1_mean))
    f.write("大带轮直径d2为：{}mm\n".format(d_d2))
    v = math.pi * d_d1_mean * nm / 60 / 1000
    if v > 5 and v < 25:
        f.write('经计算，小带轮带速v符合条件，大小为：{0:.3f}m/s\n'.format(v))
    else:
        print('！！！v不符合要求, 请重新设计！！！')
        exit()
    a_min = 0.55 * (d_d1_mean + d_d2)
    a_max = 2 * (d_d1_mean + d_d2)
    a0 = 0.7 * (a_min + a_max)
    
    
    f.write('\n######## 计算带轮中心距和带的基准长度 ########\n')
    f.write("4.1  计算得到预设中心距a0为: {:.3f}mm\n".format(a0))
    l_d0 = 2 * a0 + math.pi / 2 * (d_d1_mean + d_d2) + (d_d2 - d_d1_mean) ** 2 / 4 / a0
    min_err = 10000
    best_l_d = 0
    k_l = 0
    for elem in l_d_list:
        l_d = elem[0]
        if abs(l_d0 - l_d) < min_err:
            min_err = abs(l_d0 - l_d)
            best_l_d = l_d
            k_l = elem[1]
    f.write("4.2  计算得到初估带长为Ld_0: {:.3f}mm\n".format(l_d0))
    f.write("     取最佳基准带长Ld为: {:.3f}mm\n".format(best_l_d))
    a = a0 + (best_l_d - l_d0) / 2
    f.write("4.3  实际选取中心距a: {:.3f}mm\n".format(a))
    
    
    f.write("\n######## 计算小带轮的包角 ########\n")
    alpha1 = 180 - (d_d2 - d_d1_mean) / a * 57.3
    f.write("包角大小为: {:.3f}°\n".format(alpha1))
    if alpha1 > 120:
        f.write("包角大小大于120°，符合要求\n")
    else:
        print("包角大小为 {:.3f}°，不符合大于120°的设计要求，请重新确定参数！\n".format(alpha1))
        exit()
    
    
    f.write('\n######## 计算V带根数 ########\n')
    if (alpha1 > 170):
        k_a = 0.98
    elif alpha1 > 160:
        k_a = 0.95
    elif alpha1 > 150:
        k_a = 0.92
    elif alpha1 > 140:
        k_a = 0.89
    elif alpha1 > 130:
        k_a = 0.86
    elif alpha1 > 120:
        k_a = 0.82
    P = (P1 + d_P1) * k_a * k_l
    z = int(pc / P)
    f.write("确定带的根数为：{}\n".format(z))
    
    
    f.write('\n######## 确定带的初拉力F_0 ########\n')
    F0 = 500 * pc / v / float(z) * (2.5 / k_a - 1) + 0.1 * v ** 2
    f.write("初拉力F0为：{:.3f}N\n".format(F0))
    
    
    f.write('\n######## 计算传动带在轴上的作用力F_Q ########\n')
    alpha1 = alpha1 / 180 * math.pi
    F_Q = 2 * float(z) * F0 * math.sin(alpha1 / 2)
    f.write("传动带的作用力F_Q为: {:.3f}N\n\n".format(F_Q))
    
    
    f.write("\t\t########## V带设计结束 ##########\n\n\n")
    f.close()
    