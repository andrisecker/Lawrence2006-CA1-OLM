#!/usr/bin/ipython -i

from neuron import *
from nrn import *
#from neuron import gui


def create_comp(name = 'soma'):
    
    comp = h.Section('soma')

    
    comp.insert('cad_orig')
    comp.insert('ica_clamp')
    comp.eca = 50

    comp.nseg = 1
    comp.L = 1
    comp.diam = 1
    
    comp.insert('pas')
    comp(0.5).g_pas = 3e-4
    comp(0.5).e_pas = -65

    h.cao0_ca_ion = 2
    h.cai0_ca_ion = 5e-6

    h.celsius = 24

    return comp

    
def plot_timeseries(vdict, varlist):
    from pylab import plot, show, figure, title
    t = vdict['t']
    for n in varlist:
        figure()
        plot(t, vdict[n], label=n)
        title(n)
    
    show()

def create_dumps(section, varlist):
    recordings = {n: h.Vector() for n in varlist}

    for (vn, v) in recordings.iteritems():
        v.record(section(0.5).__getattribute__('_ref_' + vn))
    
    recordings['t'] = h.Vector()
    recordings['t'].record(h._ref_t)
    return recordings 


def dump_to_file(vdict, varlist, fname='nrn_ca.dat'):
    from numpy import savetxt, array

    vnames = ['t'] + varlist
    X = array([vdict[x].to_python() for x in vnames]).T
    savetxt(fname, X)


def run(tstop=10, dt=0.001):
    h.dt = dt
    h.finitialize(-65)
    h.fcurrent()
    h.frecord_init()
    while h.t < tstop:
        h.fadvance()



comp = create_comp('soma')

stim = h.IClamp(0.5, sec=comp)
stim.delay = 40
stim.dur = 120
stim.amp = 0.001

varlist = ['debugVal0_cad_orig', 'debugVal1_cad_orig', 'debugVal2_cad_orig', 'debugVal3_cad_orig', 'pump_cad_orig', 'pumpca_cad_orig', 'ica']
ds = create_dumps(comp, varlist)

run(300, 0.001)

plot_timeseries(ds, varlist)
dump_to_file(ds, varlist)
