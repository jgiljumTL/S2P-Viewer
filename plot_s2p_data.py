import skrf as rf
from pylab import *

from skrf import Network, Frequency

ring_slot = Network('TEST_RX25AF_U01283_VNA_N_BWL=0,00_BWH=0,00_GC=1,50_00.s2p')

print(ring_slot)

ring_slot.s21.plot_s_db(label='U01283', m=1, n=0)

plt.show()

