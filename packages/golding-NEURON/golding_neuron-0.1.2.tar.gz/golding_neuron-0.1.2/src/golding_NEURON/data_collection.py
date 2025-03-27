from .attributes import (tiplist,
                         parentlist,
                         getsegxyz,
                         furthest_point,
                         sectionlist_length,
                         distance3D)
import logging
from neuron import h
# from neuron.units import mV
import math
import numpy as np
import pandas as pd
import random
from scipy.optimize import curve_fit

logger = logging.getLogger(__name__)


def propogation_test(
    cell, sectionlist: object, include_absolute=True
) -> tuple[list, list, list, list, object]:
    """
    Tests synapses at every segment and returns time at max depolarization.

    Parameters
    -----------
    cell: Cell
        Cell instance to pass to syntest_max_voltage
    sectionlist: object
        sectionlist (from Cell instance) to place synapses on

    Returns:
    lists_of_t_at_maxv: list
                        format = [sections][individual point recordings]
        list of times (from stim. site peak to soma peak) that max
        depolarization was reached at the some for each point/synapse on each
        section, broken up by section.

    lists_of_v_at_maxv: list
                        format = [sections][individual point recordings]
        list of voltages (from stim. site peak to soma peak) when max
        depolarization was reached at the some for each point/synapse on each
        section, broken up by section.

    lists_of_abs_t_at_maxv: list
                        format = [sections][individual point recordings]
        list of times (from start of simulation) where max depolarization was
        reached at the some for each point/synapse on each section, broken up by section.

    lists_of_abs_v_at_maxv: list
                        format = [sections][individual point recordings]
        list of voltages  that max
        depolarization was reached at the some for each point/synapse on each
        section, broken up by section.

    current_section_list: SectionList
        returned sectionlist parameter, to pass to other functions

    include_absolute: bool, optional
        Whether to include absolute times and voltages in the output. Default is True.
    """
    current_section_list = sectionlist
    py_sections = list(
        current_section_list
    )  # convert SectionList() to python for len()
    lists_of_t_at_maxv = [[] for i in range(len(py_sections))]
    lists_of_v_at_maxv = [[] for i in range(len(py_sections))]
    lists_of_abs_t_at_maxv = [[] for i in range(len(py_sections))]
    lists_of_abs_v_at_maxv = [[] for i in range(len(py_sections))]
    sectionCount = 0
    for sec in current_section_list:
        synlist = syn_place(sec)  # makes list of synapses for synlist_test

        rec_site_maxv, rec_site_maxt, syn_maxv, syn_maxt = indiv_syn_test(
            cell, synlist, cell.somatic[0]
        )
        del synlist

        # adds each max voltage and time value to created 2d list: [section][seg time/voltage]
        for i in range(0, len(rec_site_maxv)):
            lists_of_v_at_maxv[sectionCount].append(abs(rec_site_maxv[i] - syn_maxv[i]))
            lists_of_abs_v_at_maxv[sectionCount].append(rec_site_maxv[i])
        for i in range(0, len(rec_site_maxt)):
            lists_of_t_at_maxv[sectionCount].append(abs(rec_site_maxt[i] - syn_maxt[i]))
            lists_of_abs_t_at_maxv[sectionCount].append(rec_site_maxt[i])
        sectionCount += 1

    if include_absolute:
        return (
            lists_of_t_at_maxv,
            lists_of_v_at_maxv,
            lists_of_abs_t_at_maxv,
            lists_of_abs_v_at_maxv,
            current_section_list,
        )
    else:
        return (
            lists_of_t_at_maxv,
            lists_of_v_at_maxv,
            current_section_list,
        )


def indiv_syn_test(
    cell, synlist: list, rec_section: object, gmax: float = 0.005
) -> tuple[list, list, list, list]:
    """
    Activates each synapse individually in a given list and, for each synapse, records the
    max voltages and time at those voltages at the soma and the synapse site

    Parameters
    ----------
    cell: Cell
        Cell instance to pull stabilization_time variable to use.
    synlist: list
        list of synapse NEURON point processes to activate.
    rec_section: Section
        Section to record from for the non-synapse compartment measurements.
        Records from center of given section.

    Returns
    -------
    recordings: tuple [rec_site_maxv, rec_site_maxt, syn_maxv, syn_maxt]
        tuple of lists of recorded values for the peaks of each trace for each syn.
        Order of provided synlist is the order of each list.
    """
    syncount = len(synlist)
    syn_maxv = []
    syn_maxt = []
    rec_site_maxv = []
    rec_site_maxt = []

    for i in range(0, syncount):
        h.dt = 1  # speed up stabilization period
        netcon = h.NetCon(None, synlist.o(i))
        netcon.weight[0] = gmax
        netcon.delay = 0
        syn_segment = synlist[i].get_segment()
        syn_v = h.Vector().record(syn_segment._ref_v)
        rec_site_v = h.Vector().record(rec_section(0.5)._ref_v)
        t = h.Vector().record(h._ref_t)

        h.finitialize()
        h.continuerun(cell.stabilization_time - 5)
        h.frecord_init()
        netcon.event(cell.stabilization_time)
        h.dt = 0.001
        h.continuerun(cell.stabilization_time + 5)
        netcon.weight[0] = 0.0
        rec_site_maxv.append(rec_site_v.max())
        rec_site_maxt.append(t.get(rec_site_v.max_ind()))
        syn_maxv.append(syn_v.max())
        syn_maxt.append(t.get(syn_v.max_ind()))
        del netcon
    recordings = (rec_site_maxv, rec_site_maxt, syn_maxv, syn_maxt)
    return recordings


def syn_place(section, tau1=0.271, tau2=0.271, e=15, syn_density=None, locs=None):
    """
    Creates Exp2Syn point process along a given section, at every
    segment/given density(syndensity)/specific point(pos).

    Parameters
    ----------
    section: Section
        section to place synapse(s) on.
    tau1 & tau2: float, optional
        Time of rising and falling edge (respectively), in ms. Default is
        0.271 for each.
    e: int
        Reverse potential of synapse process.
    syn_density: float, optional
        Density of placed synapses. If not given, synapse placement will
        either be at every segment (pos not given) or at a specific location (pos given).
    pos: list, optional
        Specific segment/locations of a single placed synapse. If syn_density is given,
        pos will be ignored.

    Returns
    -------
    synlist: list
        list of created synapses, in order of ascending NEURON segment position
        0->1. Almost always proximal to distal in our use case.
    """
    sec_len = section.L  # length used for density calcs
    synlist = h.List()

    # checking input variables
    if syn_density is None:
        if locs is not None:
            for loc in locs:
                syn = h.Exp2Syn(section(loc))
                syn.tau1 = tau1
                syn.tau2 = tau2
                syn.e = e
                synlist.append(syn)
            return synlist
        else:
            syncount = section.nseg
            syninc = sec_len / syncount

    else:
        dens = syn_density
        syncount = int(sec_len * dens)

    # making synapses and setting properties
    for i in range(0, syncount):
        syn = h.Exp2Syn(section(((syninc / 2) + (i * syninc)) / sec_len))
        syn.tau1 = tau1
        syn.tau2 = tau2
        syn.e = e
        synlist.append(syn)
    return synlist


def syn_test(
    cell,
    sectionlists,
    numsyn,
    synspace,
    axonspeed,
    numtrial,
    simultaneous=1,
    gmax=0.037,
    release_probability=0.45,
    traces=False,
) -> dict:
    """
    Takes a list of section lists (likely for each branch), and simulates
    placing synapse groups randomly along them. Activates all synapses at once
    (not including axonal delay).

    Calculates the average time
    to peak and average halfwidth, along with error.

    Parameters
    ----------
    cell : Cell

    sectionlists,: list[sectionlist_a, sectionlist_b]
        list of sectionlists, usually used for polar sides of cell
        (lateral vs. medial).
    numsyn : int
        number of synapses within a synapse span
    synspace : float
        space between each synapse in a group
    axonspeed : float, optional
        speed of axonal delay lines (in m/s)
    numtrial : int
        number of trials to be averaged. Each trial = new synaptic placement.
    simultaneous : int, optional
        number of axon fibers (or synapse groups) innervating each list.
    gmax : float
        combined conductance of all synapses in a span
    release_probability : float (0-1)
        chance of any individual synaptic release
    traces : bool
        whether or not traces for the trials are returned in the dictionary
    Returns
     -------
     dict
        Dictionary containing the average time to peak, average halfwidth, and their standard errors.
        If traces is True, also includes the traces for the trials.
    """
    maxtimeArray = np.zeros(numtrial)
    halfwidthArray = np.zeros(numtrial)
    trace_list = []
    tipsections = []
    python_tipsections = []
    numpaths = []
    furthestdistance, furthestsegment = furthest_point(cell, sectionlists[0])

    for sectionlistnum in range(len(sectionlists)):
        tipsections.append(tiplist(sectionlists[sectionlistnum]))
        python_tipsections.append(list(tipsections[sectionlistnum]))
        numpaths.append(len(python_tipsections[sectionlistnum]))
        if furthest_point(cell, sectionlists[sectionlistnum])[0] > furthestdistance:
            furthestdistance = furthest_point(cell, sectionlists[sectionlistnum])[0]
            furthestsegment = furthest_point(cell, sectionlists[sectionlistnum])[1]

    for trialnum in range(numtrial):

        synlists = []
        netconlists = []
        netstimlists = []
        syn_conductance_vectors = []

        for sectionlistnum in range(len(sectionlists)):

            for tip in tipsections[sectionlistnum]:
                temppath = parentlist(
                    tip
                )  # creating a path composed of each section from an end to the soma
                temppathlength = sectionlist_length(cell, temppath)[
                    0
                ]  # getting the total length of the path
                if (
                    numsyn * synspace > temppathlength
                ):  # checking if the synapse group can fit along this path
                    raise Exception(
                        "Spread of synapses is longer than the shortest path length"
                    )

            for j in range(simultaneous):
                randpath = random.randint(
                    0, numpaths[sectionlistnum] - 1
                )  # chooses a random number to choose a path
                path = parentlist(
                    python_tipsections[sectionlistnum][randpath]
                )  # generates that section list of path from chosen end segment array element
                pathlength = sectionlist_length(cell, path)[
                    0
                ]  # calculates total path length
                randpoint = (
                    random.random() * pathlength
                )  # chooses a random value (0,1) and determines placement of most distal synapse of group

                # pick a new random value if the previous starting point cannot fit on the desired side
                while randpoint - (numsyn * synspace) < 0:
                    randpoint = random.random() * pathlength

                # create storage lists
                synlocations = []
                netconlist = []
                netstimlist = []

                for k in range(numsyn):  # create synapses and add to list
                    synlocations.append(randpoint - (synspace * k))

                # generate group of synapses and add group list to a larger array of them all
                syngroup = syngroup_path_place(cell, path, synlocations)
                synlists.append(syngroup)
                count = 0

                for syn in syngroup:
                    syn_conductance_vectors.append(h.Vector().record(syn._ref_g))
                    netstim = h.NetStim()
                    netcon = h.NetCon(netstim, syn)
                    netcon.delay = 0
                    chance = random.random()
                    if chance >= release_probability:
                        netcon.weight[0] = 0
                    else:
                        netcon.weight[0] = gmax / numsyn

                    netstim.number = 1  # trigger once
                    netstim.interval = 1  # not necessary

                    # find the distance of syn's segment from the most distant segment and calculate axon delay using given speed
                    distanceFromFurthestSegment = distance3D(
                        getsegxyz(furthestsegment), getsegxyz(syn.get_segment())
                    )
                    axon_delay = distanceFromFurthestSegment / (1000 * axonspeed)
                    netstim.start = cell.stabilization_time + axon_delay

                    netstimlist.append(netstim)
                    netconlist.append(netcon)

                netconlists.append(netconlist)
                netstimlists.append(netstimlist)
        v = h.Vector().record(cell.somatic[0](0.5)._ref_v)
        t = h.Vector().record(h._ref_t)
        g = syn_conductance_vectors[0]
        h.finitialize()
        h.dt = 1
        h.continuerun(cell.stabilization_time - 5)
        h.frecord_init()
        h.dt = 0.001
        h.continuerun(cell.stabilization_time + 10)
        t = (
            t - cell.stabilization_time
        )  # set time relative to the start of synaptic activity
        for syn_conductance_vector in syn_conductance_vectors[1:]:
            g = g.add(syn_conductance_vector)
        g = g.div(len(syn_conductance_vectors))
        if traces == True:
            trace_list.append(
                {
                    "time": t.to_python(),
                    "voltage": v.to_python(),
                    "conductance": g.to_python(),
                }
            )
        maxVind = v.max_ind()
        maxtimeArray[trialnum] = t[maxVind]
        halfV = (v.max() + v[0]) / 2

        firsthalf = t[v.indwhere(">=", halfV)]
        secondhalf = t[v.cl(maxVind).indwhere("<=", halfV) + maxVind]
        halfwidth = secondhalf - firsthalf
        halfwidthArray[trialnum] = halfwidth
    maxtimeaverage = np.average(maxtimeArray)
    halfwidthaverage = np.average(halfwidthArray)

    maxtimesumofsquares = 0
    for maxtime in maxtimeArray:
        square = (maxtime - maxtimeaverage) ** 2
        maxtimesumofsquares += square

    maxtimevariance = maxtimesumofsquares / (numtrial - 1)
    maxtimestandarddev = math.sqrt(maxtimevariance)
    maxtimestandarderror = maxtimestandarddev / math.sqrt(numtrial)

    halfwidthsumofsquares = 0
    for halfwidth in halfwidthArray:
        square = (halfwidth - halfwidthaverage) ** 2
        halfwidthsumofsquares += square

    halfwidthvariance = halfwidthsumofsquares / (numtrial - 1)
    halfwidthstandarddev = math.sqrt(halfwidthvariance)
    halfwidthstandarderror = halfwidthstandarddev / math.sqrt(numtrial)
    if traces == True:
        return {
            "maxtime": maxtimeaverage,
            "maxtimestandarderror": maxtimestandarderror,
            "halfwidth": halfwidthaverage,
            "halfwidthstandarderror": halfwidthstandarderror,
            "traces": trace_list,
        }
    else:
        return {
            "maxtime": maxtimeaverage,
            "maxtimestandarderror": maxtimestandarderror,
            "halfwidth": halfwidthaverage,
            "halfwidthstandarderror": halfwidthstandarderror,
        }


# ADD docstring
def itd_test(
    cell,
    sectionlist1,
    sectionlist2,
    itd_range,
    itd_step,
    numtrial,
    numsyn=4,
    synspace=7,
    axonspeed=1,
    numfiber=1,
    cycles=1,
    interval=1,
    inhibition=False,
    inh_timing=-0.32,
    exc_fiber_gmax=0.037,
    inh_fiber_gmax=0.022,
    threshold=0,
    absolute_threshold=False,
    traces=False,
    axon=False,
    parallel=True,
    pc=None
):
    """
    Perform ITD (Interaural Time Difference) tests on a given cell.

    Parameters
    ----------
    cell : Cell
        The cell instance to be tested.
    sectionlist1 : list
        List of polar branches for the first section.
    sectionlist2 : list
        List of polar branches for the second section.
    delay_range : float
        The range of delays to be tested (in ms).
    delay_step : float
        The increment between each delay test (in ms).
    numtrial : int
        The number of trials for each delay.
    numsyn : int, optional
        The number of synapses per group (span). Default is 4.
    synspace : float, optional
        The space between each synapse in a group (in µm). Default is 7.
    axonspeed : float, optional
        The speed of axonal propagation (in m/s). Default is 1.
    simultaneous : int, optional
        The number of axon fibers or synapse spans per branch. Default is 1.
    cycles : int, optional
        The number of netstims. Default is 1.
    interval : float, optional
        The time between netstims. Default is 1.
    inhibition : bool, optional
        Whether to include inhibition in the test. Default is False.
    inh_delays : list, optional
        The delays for inhibition (in ms). Default is [-0.32, -0.38].
    exc_fiber_gmax : float, optional
        The maximum conductance for excitatory fibers. Default is 0.037.
    inh_fiber_gmax : float, optional
        The maximum conductance for inhibitory fibers. Default is 0.15.
    threshold : float, optional
        The voltage threshold for determining ITD. Default is 0.
    absolute_threshold : bool, optional
        Whether to use an absolute threshold. Default is False.
    traces : bool, optional
        Whether to return traces of the trials. Default is False.
    axon : bool, optional
        Whether to record from the axon. Default is False.

    Returns
    -------
    delay_threshold_prob_array : list
        The probability of threshold crossing for each delay.
    trace_list : dict, optional
        The traces of the trials if `traces` is True.
    """
    # create arrays to iterate
    sectionlistarray = [sectionlist1, sectionlist2]
    tipsectionsarray = []
    python_tipsectionsarray = []
    numpatharray = []
    trace_list = {}
    inh_delays = [inh_timing, inh_timing - 0.06]
    numfiber = int(numfiber)
    numsyn=int(numsyn)
    base_delay = (itd_range / 2) + abs(np.max(inh_delays))
    if parallel:
        pc = pc if (pc is not None) else h.ParallelContext()
    else:
        pc = None
    if abs(inh_delays[0]) > base_delay or abs(inh_delays[1]) > base_delay:
        raise Exception("Inhibition delay magnitude is too large")
    
    for sectionlist in sectionlistarray:
        tips = tiplist(sectionlist)
        tipsectionsarray.append(tips)
        python_tips = list(tips)
        python_tipsectionsarray.append(python_tips)
        numpath = len(python_tips)
        numpatharray.append(numpath)

    # initialize storage variables
    thresholdCrossArray = np.zeros(numtrial)
    probabilityArray = np.zeros(int(itd_range / itd_step))
    maxTrialVoltageArray = []
    maxDelayVoltageArrays = []
    stdevArray = []
    # calculates furthest point to be utilized for axonal delay
    if (
        furthest_point(cell, sectionlistarray[0])[0]
        >= furthest_point(cell, sectionlistarray[1])[0]
    ):
        furthestsegment = furthest_point(cell, sectionlistarray[0])[1]
    else:
        furthestsegment = furthest_point(cell, sectionlistarray[1])[1]

    for section in sectionlistarray:
        for tip in tipsectionsarray[0]:
            temppath = parentlist(
                tip
            )  # creating a path composed of each section from an end to the soma
            temppathlength = sectionlist_length(cell, temppath)[
                0
            ]  # getting the total length of the path
            if (
                numsyn * synspace > temppathlength
            ):  # checking if the synapse group can fit along this path
                raise Exception(
                    "Spread of synapses is longer than the shortest path length"
                )
        for tip in tipsectionsarray[1]:
            temppath = parentlist(
                tip
            )  # creating a path composed of each section from an end to the soma
            temppathlength = sectionlist_length(cell, temppath)[
                0
            ]  # getting the total length of the path
            if (
                numsyn * synspace > temppathlength
            ):  # checking if the synapse group can fit along this path
                raise Exception(
                    "Spread of synapses is longer than the shortest path length"
                )

    for delay_step_num in range(
        int(itd_range / itd_step) + 1
    ):  # step through number of delay
        delay_step_traces = []
        maxTrialVoltageArray = []
        inhibitsyns = np.empty(2, dtype=object)

        for inhibitsyn_num in range(2):
            inhibitsyn = h.Exp2Syn(cell.somatic[0](0.5))
            inhibitsyn.e = -90
            inhibitsyn.tau1 = 1.5
            inhibitsyn.tau2 = 1.5
            inhibitstim = h.NetStim()
            inhibitstim.start = -1
            inhibitstim.number = cycles
            inhibitstim.interval = interval
            inhibitcon = h.NetCon(inhibitstim, inhibitsyn)
            inhibitcon.delay = 0
            inhibitcon.weight[0] = inh_fiber_gmax / 2

            if inhibition:
                inhibitstim.start = (
                    cell.stabilization_time
                    + base_delay
                    + inh_delays[inhibitsyn_num]
                    + (
                        (
                            ((-itd_range / 2) + (itd_step * delay_step_num))
                            * inhibitsyn_num
                        )
                    )
                )
            # print(inhibitstim.start)

            inhibitsyns[inhibitsyn_num] = (inhibitsyn, inhibitstim, inhibitcon)

        for trialnum in range(numtrial):  # loop for every trial (same delay value)

            # lists to store the different point processes
            synlists = []
            netconlists = []
            netstimlists = []

            for sectionlistnum in range(len(sectionlistarray)):
                furthestsegment = furthest_point(
                    cell, sectionlistarray[sectionlistnum]
                )[1]
                for synspancount in range(numfiber):
                    randpath = random.randint(
                        0, numpatharray[sectionlistnum] - 1
                    )  # chooses a random number to choose a path
                    path = parentlist(
                        python_tipsectionsarray[sectionlistnum][randpath]
                    )  # generates that section list of path from chosen end segment array element
                    pathlength = sectionlist_length(cell, path)[
                        0
                    ]  # calculates total path length
                    randpoint = (
                        random.random() * pathlength
                    )  # chooses a random value (0,1) and determines placement of most distal synapse of group

                    # pick a new random value if the previous starting point cannot fit on the desired side
                    while randpoint - (numsyn * synspace) < 0:
                        randpoint = random.random() * pathlength

                    # create storage lists
                    synlocations = []
                    netconlist = []
                    netstimlist = []

                    for syncount in range(numsyn):  # create synapses and add to list
                        synlocations.append(randpoint - (synspace * syncount))

                    # generate group of synapses and add group list to a larger array of them all
                    syngroup = syngroup_path_place(cell, path, synlocations)
                    synlists.append(syngroup)

                    count = 0

                    # assigning properties (timing,etc.) to the point processes
                    for syn in syngroup:

                        netstim = h.NetStim()
                        netstim.number = cycles
                        netstim.interval = interval
                        netcon = h.NetCon(netstim, syn)
                        netcon.delay = 0
                        if random.random() >= 0.45:
                            netcon.weight[0] = 0
                        else:
                            netcon.weight[0] = exc_fiber_gmax / numsyn
                            # distribute conductance across all synapses of a fiber

                        # find the distance of the syn's segment from the most distant segment and calculate axon delay using given speed
                        distanceFromFurthestSegment = distance3D(
                            getsegxyz(furthestsegment), getsegxyz(syn.get_segment())
                        )
                        axon_delay = distanceFromFurthestSegment / (1000 * axonspeed)

                        netstim.start = (
                            cell.stabilization_time + axon_delay
                        )  # add axon delay #this is the base time applied to all netstims

                        if sectionlistnum == 0:
                            netstim.start += (
                                base_delay
                                - (itd_range / 2)
                                + (itd_step * delay_step_num)
                            )  # add variable delay relative to base_delay

                        if sectionlistnum == 1:
                            netstim.start += base_delay  # add base_delay to unchanging (ipsilateral) branch
                        # print("exc:", netstim.start)
                        # add net objects to a list to keep in memory
                        netstimlist.append(netstim)
                        netconlist.append(netcon)

                    # add list of netobjects to a list to keep in memory
                    netconlists.append(netconlist)
                    netstimlists.append(netstimlist)

            # running sim
            v_soma = h.Vector().record(cell.somatic[0](0.5)._ref_v)
            v_monitor = v_soma
            if axon: 
                v_axon = h.Vector().record(cell.nodes[-1](0.5)._ref_v)
                v_monitor = v_axon
            t = h.Vector().record(h._ref_t)
            if parallel:
                pc.set_maxstep(10)
                h.stdinit()
                pc.psolve(cell.stabilization_time - 5)
                h.frecord_init()
                pc.psolve(cell.stabilization_time + 10)
            else:
                h.finitialize()
                h.dt = 1
                h.continuerun(cell.stabilization_time - 5)
                h.frecord_init()
                h.dt = 0.001
                h.continuerun(cell.stabilization_time + 10)
            # t = t - t[0]  # -5 #set time relative to the start of synaptic activity
            if traces:
                curr_traces = {"time": t.to_python(), "voltage_soma": v_soma.to_python()}
                curr_traces["voltage_axon"] = v_axon.to_python() if axon else None
                delay_step_traces.append(curr_traces)
            maxTrialVoltageArray.append(v_monitor.max())
            # print(v_monitor.as_numpy())
            resting = v_monitor[0]
            # delete pointers to each point process
            del synlists
            del netconlists
            del netstimlists
        if traces:
            trace_list[-(itd_range / 2) + (itd_step * delay_step_num)] = (
                delay_step_traces
            )
        # add max voltage values for each delay step
        maxDelayVoltageArrays.append(maxTrialVoltageArray)

    def threshold_crossing(voltage_array, itd_threshold):
        delayThresholdProbArray = []

        for delay in range(len(voltage_array)):
            thresholdCount = 0

            # count number of trials that are greater than threshold
            for trial in range(len(voltage_array[0])):
                if maxDelayVoltageArrays[delay][trial] > itd_threshold:
                    thresholdCount += 1

            # calculate/store probability for delay step
            delayThresholdProb = thresholdCount / numtrial

            delayThresholdProbArray.append(delayThresholdProb)
        return delayThresholdProbArray

    # iterating to find a voltage threshold that has a max probability of 0.8
    if threshold == 0:
        itd_threshold = resting
        maxThresholdProb = 1

        while maxThresholdProb > 0.800:
            itd_threshold += 0.01
            delay_threshold_prob_array = threshold_crossing(
                maxDelayVoltageArrays, itd_threshold
            )
            # find max prob value out of all delays
            maxThresholdProb = max(delay_threshold_prob_array)
        print(itd_threshold)

    elif absolute_threshold:
        itd_threshold = threshold
        delay_threshold_prob_array = threshold_crossing(
            maxDelayVoltageArrays, itd_threshold
        )
    else:
        itd_threshold = threshold + resting
        delay_threshold_prob_array = threshold_crossing(
            maxDelayVoltageArrays, itd_threshold
        )
    logger.info("itd sweep complete for %s", cell.cell_name)
    if traces == True:
        return delay_threshold_prob_array, trace_list
    else:
        return delay_threshold_prob_array


def syngroup_path_place(cell, sectionlist, locations, tau1=0.270, tau2=0.271, e=15):

    lengtharray = []
    synlist = []
    for sec in sectionlist:  # record each length of each section
        if sec in cell.somatic:
            lengtharray.append(sec.L / 2)  # cutting soma in half, to keep on one side
        else:
            lengtharray.append(sec.L)

    for loc in locations:
        sectioncount = 0
        lengthcount = 0
        sectionindex = 0
        loconsec = 0

        # move along the length of the path until section and relative location are found
        for length in lengtharray:

            if length + lengthcount > loc:
                sectionindex = sectioncount
                loconsec = loc - lengthcount
                break
            else:
                sectioncount += 1
                lengthcount += length

        syn = h.Exp2Syn(
            list(sectionlist)[sectionindex](
                loconsec / list(sectionlist)[sectionindex].L
            )
        )  # place syn
        syn.tau1 = tau1
        syn.tau2 = tau2
        syn.e = e
        synlist.append(syn)

        syn = None

    return synlist


# ADD docstring
def get_itd_averages(filepath, parameter=False):
    itd_df = pd.read_csv(filepath)
    names = pd.unique(itd_df.get("name"))
    if parameter:
        parameter_vals = pd.unique(itd_df.get(parameter))
    itd_averages_pd = pd.DataFrame()
    delays = np.arange(-0.5, 0.51, 0.01)
    names_to_keep = []
    parameters_to_keep = []
    for name in names:
        if parameter:
            for parameter_val in parameter_vals:
                cell_itds_df = itd_df.loc[
                    (itd_df["name"] == name) & (itd_df[parameter] == parameter_val)
                ]

                cell_itds_df = cell_itds_df
                average_cell_itd = cell_itds_df.drop(["name", parameter], axis=1).mean(
                    axis=0
                )
                names_to_keep.append(name)
                parameters_to_keep.append(parameter_val)
                itd_averages_pd = pd.concat([itd_averages_pd, average_cell_itd], axis=1)
                # itd_averages_pd.index = delays
        else:

            cell_itds_df = itd_df.loc[itd_df["name"] == name]
            # print(cell_itds_df.drop(["name", "control"], axis=1).mean(axis=0))
            average_cell_itd = cell_itds_df.drop(["name"], axis=1).mean(axis=0)
            names_to_keep.append(name)
            itd_averages_pd = pd.concat(
                [
                    itd_averages_pd,
                    average_cell_itd,
                ],
                axis=1,
            )
            # itd_averages_pd.index = delays
    itd_averages_pd.columns = names_to_keep
    itd_averages_pd.sort_index(axis=1)
    itd_averages_pd = itd_averages_pd.transpose()
    itd_averages_pd.reset_index(inplace=True, drop=True)
    itd_averages_pd.insert(0, "name", names_to_keep)
    try:
        itd_averages_pd.insert(1, parameter, parameters_to_keep)
    except:
        pass
    return itd_averages_pd


# ADD docstring
# ADD comments
def get_syntest_averages(filepath):
    """Get average synapse data from a given file path"""
    groupsyn_sheet = filepath
    groupsyn_data = pd.read_csv(groupsyn_sheet)
    groupsyn_data.sort_values("tau", inplace=True)
    param_label = groupsyn_data.columns[2]
    averages = []
    groupsyn_np = groupsyn_data.to_numpy()
    averaged_groupsyn_pd = pd.DataFrame()

    cell_names = np.unique(groupsyn_np[:, 1])
    param_vals = np.unique(groupsyn_np[:, 2])

    for cell_name in cell_names:
        for param_val in param_vals:
            trial_num = 0
            summed_groupsyn_data = np.zeros(len(groupsyn_np[0, 3:]))
            trial_exists = False
            for row in groupsyn_np:
                # print(row, cell_name, param_val)
                if cell_name in row and param_val in row:
                    summed_groupsyn_data += np.array(row[3:], dtype=float)
                    trial_exists = True
                    trial_num += 1
            if trial_exists:
                averaged_groupsyn_data = summed_groupsyn_data / trial_num
                dataframe_row = {
                    "Cell name": cell_name,
                    param_label: param_val,
                }
                print(averaged_groupsyn_data)
                for i in range(len(averaged_groupsyn_data)):
                    dataframe_row[groupsyn_data.columns[i + 3]] = (
                        averaged_groupsyn_data[i]
                    )
                temp_df = pd.DataFrame(dataframe_row, index=[0])
                # print(temp_df)
                averaged_groupsyn_pd = pd.concat((averaged_groupsyn_pd, temp_df))
            else:
                continue
    return averaged_groupsyn_pd


# ADD docstring
# ADD comments
def get_attenuation_values(
    cell,  # cell instance
    sectionlist1,
    sectionlist2,  # list of polar branches
    exc_fiber_gmax=0.037,
):
    """Get attenuation values for a cell"""
    section_lists = [sectionlist1, sectionlist2]
    section_list_data = [dict(), dict()]
    for list_index, section_list in enumerate(section_lists):
        for sec in section_list:
            for seg in sec:
                syn = h.Exp2Syn(seg)
                syn.tau1 = 0.29
                syn.tau2 = 0.29
                syn_con = h.NetCon(None, syn, weight=0.037)
                syn_con.delay = 0
                syn.event(1000)
                t = h.Vector.record(h._ref_t)
                v_soma = h.Vector.record(cell.somatic[0](0.5)._ref_v)
                v_syn = h.Vector.record(seg._ref_v)
                h.finitialize()
                h.continuerun(10010)
                v_proportion = v_syn.max() / v_soma.max()
                try:
                    section_list_data[list_index][sec.nchild].append(v_proportion)
                except:
                    section_list_data[list_index][sec.nchild] = [v_proportion]

    return section_list_data


def fit_gaussian_to_itd(delay_values, probabilities, func=False):

    x = delay_values
    y = probabilities

    mean = sum(x * y) / sum(y)
    sigma = np.sqrt(sum(y * (x - mean) ** 2) / sum(y))

    def Gauss(x, a, x0, sigma):
        return a * np.exp(-((x - x0) ** 2) / (2 * sigma**2))

    popt, pcov = curve_fit(Gauss, x, y, p0=[max(y), mean, sigma])
    y_fit = Gauss(x, *popt)
    equation = popt
    if func:
        return y_fit, Gauss, equation
    else:
        return y_fit
