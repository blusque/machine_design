from fileinput import filename
import imp
import os
import json

from gear_wheel.gear_wheel import gear_wheel_design
from v_belt.belt_cal import v_belt_design

path = os.path.dirname(__file__)
filename = os.path.join(path, 'params.json')

with open(filename, encoding='utf-8') as f:
    params = json.load(f)
    v_belt_params = params['V_belt_params']
    gear_wheel_params = params['gear_wheel_params']

output_filename = os.path.join(path, 'output.txt')
f = open(output_filename, 'w')
f.write("============== 设计开始 ==============\n\n\n")
f.close()

v_belt_design(output_filename, v_belt_params)
for key in gear_wheel_params:
    gear_wheel_design(output_filename, key, gear_wheel_params[key])

f = open(output_filename, 'a')
f.write("============== 设计结束 ==============\n")
f.close()