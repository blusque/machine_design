from fileinput import filename
import json
import math
import os

from numpy import mat

def gear_wheel_design(filename, level, params):
    
    material = params['material']
    impact_w = params['impact type worker']
    impact_m = params['impact type motioner']
    precision = params['precision']
    i = params['i']
    z1 = params['z1']
    gamma = params['gamma']
    n1 = params['n1']
    th = params['th']
    S_Hlim = params['S_Hlim']
    S_Flim = params['S_Flim']
    Z_lvr_1 = params['Z_lvr_1']
    Z_lvr_2 = params['Z_lvr_2']
    K_t = params['K_t']
    P = params['P_in']
    Psi_d = params['Psi_d']
    Z_H = params['Z_H']
    Z_beta = params['Z_beta']
        
    f = open(filename, 'a')
    f.write('\t\t########## {}齿轮设计 ##########\n\n'.format(level))

    f.write("\n######## 精度等级及材料 ########\n")
    HB_list = {"45 steel": [229, 289, 240], "40Cr": [241, 286, 260]}
    sigma_list = {"45 steel": 580, "40Cr": 710}
    m_list = [1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20]
    hard_min = HB_list[material][0]
    hard_max = HB_list[material][1]
    hard_mean = HB_list[material][2]
    f.write("预选制造精度等级为：{}\n".format(precision))
    f.write("考虑主动轮转速不是很高，传动尺寸无严格限制，批量较小，\n故两齿轮均选用{0}，\
调制处理，硬度HB = {1} ~ {2}, \n平均取为 {3} HB\n"\
    .format(material, hard_min, hard_max, hard_mean))

    # 初选齿数
    f.write("\n######## 初选齿数 ########\n")
    z2 = i * z1
    z2 = math.floor(z2 + 0.5)
    f.write("初选齿数 z_1 = {0:.0f}，则 \n\t z_2 = i * z_1， \n     得 z_2 为{1:.0f}\n".format(z1, z2))
    

    # 确定材料的许用接触应力
    f.write("\n######## 确定材料的许用接触应力 ########\n")
    sigma_Hlim = sigma_list[material]
    f.write("2.1  确定接触疲劳极限 σ_Hlim = {}MPa\n".format(sigma_Hlim))

    t_h = th['year'] * th['days'] * th['hours']
    N_L1 = 60 * gamma * n1 * t_h * 0.2
    N_L2 = N_L1 / i

    if N_L1 > 1.5e9:
        Z_NT1 = 1.0
    elif N_L1 > 6e5:
        Z_NT1 = 1.6 - 0.177 * (math.log10(N_L1) - math.log10(6e5))
    else:
        Z_NT1 = 1.6
        
    if N_L2 > 1.5e9:
        Z_NT2 = 1.0
    elif N_L2 > 6e5:
        Z_NT2 = 1.6 - 0.177 * (math.log10(N_L2) - math.log10(6e5))
    else:
        Z_NT2 = 1.6
        
    f.write("2.2  小齿轮循环次数为{0:.3f}，大齿轮循环次数为{1:.3f}，\n\
     经计算确定寿命系数Z_NT1为{2:.3f}，Z_NT2为{3:.3f}\n"\
        .format(N_L1, N_L2, Z_NT1, Z_NT2))

    f.write("2.3  确定接触强度尺寸系数Z_X为1.0\n")
    f.write("2.4  确定接触最小安全系数S_Hlim为{:.3f}\n".format(S_Hlim))
    Z_W = 1.2 - (hard_mean - 130) / 1700
    f.write("2.5  确定齿面工作硬化系数Z_W为{:.3f}\n".format(Z_W))
    f.write("2.6  确定润滑油膜影响系数为{:.3f}\n".format(Z_lvr_1))

    sigma_HP1 = sigma_Hlim * Z_NT1 * Z_W * Z_lvr_1 / S_Hlim
    sigma_HP2 = sigma_Hlim * Z_NT2 * Z_W * Z_lvr_2 / S_Hlim
    f.write("2.7  计算许用应力σ_HP1为{0:.3f}MPa, σ_HP2为{1:.3f}MPa\n".format(sigma_HP1, sigma_HP2))

    # 初估小齿轮轮齿直径
    f.write("\n######## 初估小齿轮直径 ########\n")
    f.write("3.1  试选载荷系数K_t为{}\n".format(K_t))
    T1 = 9550 * P / n1
    f.write("3.2  小齿轮传递的扭矩T1为{:.3f}Nm\n".format(T1))
    f.write("3.3  由于是软齿面非对称布置，查得齿宽系数ψ_d为{}\n".format(Psi_d))
    f.write("3.4  根据轮齿材料查表得，材料弹性影响系数Z_E为189.8sqrt(N/mm^2)\n")
    f.write("3.5  确定节点区域系数Z_H为{}\n".format(Z_H))
    epsilon_a = 1.88 - 3.2 * (1 / z1 + 1 / z2)
    Z_epsilon = math.sqrt((4 - epsilon_a) / 3)
    f.write("3.6  计算重合度为{0:.3f}，重合度系数为{1:.3f}\n".format(epsilon_a, Z_epsilon))
    f.write("3.7  由于是直齿轮，螺旋角系数Z_β为1\n")
    d_1t = math.pow(K_t * 2 * T1 * 1000 / Psi_d * (i + 1) / i * (Z_H * 189.8 * Z_epsilon * Z_beta / sigma_HP2) ** 2, 1/3)
    d_1t = math.ceil(d_1t)
    f.write("3.8  确定初估小齿轮直径d_1t为{:.3f}mm\n".format(d_1t))

    # 确定实际计算载荷系数K
    f.write("\n######## 确定实际计算载荷系数K ########\n")
    K_A_list = [[1, 1.25, 1.5, 1.75],
                [1.1, 1.35, 1.6, 1.85],
                [1.25, 1.5, 1.75, 2],
                [1.5, 1.75, 2, 2.25]]
    if impact_w == 'none':
        col = 0
    elif impact_w == 'little':
        col = 1
    elif impact_w == 'middle':
        col = 2
    elif impact_w == 'heavy':
        col = 3
    else:
        print("请重新设置impact type worker参数！\n")
        exit()

    if impact_m == 'none':
        row = 0
    elif impact_m == 'little':
        row = 1
    elif impact_m == 'middle':
        row = 2
    elif impact_m == 'heavy':
        row = 3
    else:
        print("请重新设置impact type motion参数！\n")
        exit()

    K_A = K_A_list[row][col]
    f.write("4.1  确定使用系数K_A为{}\n".format(K_A))
    v = math.pi * d_1t * n1 / 60 / 1000
    if v < 3:
        precision = 9
    elif v < 5:
        precision = 8
    else:
        precision = 7

    if v < 2.5:
        if precision == 7:
            K_V = 1.05
        elif precision == 8:
            K_V = 1.15
        elif precision == 9:
            K_V = 1.27
    elif v < 10:
        if precision == 7:
            K_V = 1.15
        elif precision == 8:
            K_V = 1.27
        elif precision == 9:
            K_V = 1.35
    elif v < 20:
        if precision == 7:
            K_V = 1.22
        elif precision == 8:
            K_V = 1.35
        elif precision == 9:
            K_V = 1.44

    f.write("4.2  确定圆周速度为{0:.3f}m/s，制造精度等级为{2}，\n\
     动载荷系数为{1}\n".format(v, K_V, precision))

    b = Psi_d * d_1t
    wps = K_A * 2 * T1 / b / d_1t * 1000
    if wps > 100:
        K_Halpha = 1.0
    else:
        print("单位载荷为: ", wps)
        print("单位载荷应大于100！")
        print("无合适尺寸对应K_Hα！")
        exit()
        
    # 非对称支撑
    K_Hbeta = 1.11 + 0.16 * (1 + 0.6 * (b / d_1t) ** 2) * (b / d_1t) ** 2 \
        + 0.47 * 1e-3 * b
    f.write("4.3  确定齿间载荷分配系数K_Hα为{0:.3f}，确定齿向载荷分配系数K_Hβ为{1:.3f}\n".format(K_Halpha, K_Hbeta))

    K = K_A * K_V * K_Halpha * K_Hbeta
    f.write("4.4  计算载荷系数K为{:.3f}\n".format(K))

    d_1 = d_1t * math.pow(K / K_t, 1/3)
    f.write("4.5  修正小齿轮分度圆直径d_1为{:.3f}\n".format(d_1))

    m0 = d_1 / z1
    best_m = 0
    min_err = 1000
    for m in m_list:
        if (abs(m - m0) < min_err):
            min_err = abs(m - m0)
            best_m = m
    m = best_m
    f.write("4.6  计算模数m为{}\n".format(m))

    # 确定传动主要几何尺寸
    f.write("\n######## 确定传动主要几何尺寸 ########\n")
    d1 = m * z1
    d2 = m * z2
    a = (d1 + d2) / 2
    b2 = Psi_d * d1
    b2 = math.ceil(b2)
    b1 = b2 + 4
    f.write("经过计算得，小齿轮轮齿直径为{0}，\n大齿轮轮齿直径为{1}，中心距为{2}，\n\
大齿轮齿宽为{3}， 小齿轮齿宽为{4}\n\n".format(d1, d2, a, b2, b1))
    
    f.write('\t\t########## 设计结束 ##########\n\n')
    f.close()
