import os
import json


default_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
calib_file = os.path.join(default_config_path, 'LofarCtl_calib.json')
config_file = os.path.join(default_config_path, 'LofarCtl_config.json')

config_path = os.path.join(os.environ['HOME'], '.pysovo')
if os.path.exists(config_path):
    tmp = os.path.join(config_path, 'LofarCtl_calib.json')
    if os.path.exists(tmp):
        calib_file = tmp
    tmp = os.path.join(config_path, 'LofarCtl_config.json')
    if os.path.exists(tmp):
        config_file = tmp
else:
    config_path = default_config_path

config = json.load(open(config_file))

