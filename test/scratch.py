import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rfsys.core.sim_engine import CascadeEngine
from rfsys.components.passive_components import PassiveComponent
from rfsys.components.active_components import ActiveComponent


filter = PassiveComponent('1', 'Filter')
filter.add_parameter('gain', [10, 20], [-0.5, -1])
#filter.add_parameter('NF', [10, 20], [0.5, 1])
lna = ActiveComponent('2', 'LNA')
lna.add_parameter('gain', [10, 20], [20, 20])
lna.add_parameter('NF', [10, 20], [3, 6])
sim = CascadeEngine([filter, lna])

print("-----------------------------------------------")
for freq in [10, 15, 20]:
    print("Simulation Freq: {} MHz".format(freq))
    sim.run(freq)
    for d in sim.comp_data:
        print("uid: {} | gain: {} dB | NF: {} dB".format(d.uid, d.get_value('gain', freq), d.get_value('NF', freq)))
    print("-----------------------------------------------")

