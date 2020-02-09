"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(sys.path)
"""
from .xml_parser import load_components
from ..components.base_component import component_builder
from .sim_engine import CascadeEngine

FILENAME = "../../usr/component_schema.xml"

raw_comp_list = load_components(FILENAME)
comp_obj_list = list()
for comp_dict in raw_comp_list:
    comp_obj = component_builder(comp_dict)
    comp_obj_list.append(comp_obj)

sim = CascadeEngine(comp_obj_list)
print("-----------------------------------------------")
for freq in [10, 15, 20]:
    print("Simulation Freq: {} MHz".format(freq))
    sim.run(freq)
    for d in sim.comp_data:
        print("uid: {} | gain: {} dB | NF: {} dB".format(d.uid, d.get_value('gain', freq), d.get_value('NF', freq)))
    print("-----------------------------------------------")