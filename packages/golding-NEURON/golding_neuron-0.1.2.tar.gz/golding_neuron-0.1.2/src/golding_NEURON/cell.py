from .attributes import tiplist
from pathlib import Path
import math
import numpy as np
from pathlib import Path
from neuron import h
h.load_file("import3d.hoc")


class Cell:
    # variable timestep decreases runtimes
    # (but some simulations NEED fixed timestep)
    cvode = h.CVode()
    cvode.active(1)

    # default parameters used for culling filopodia
    minimum_length = 15.0
    minimum_diameter = 0.5
    seg_density = 0.5
    stabilization_time = 3000
    # cell recordings are volatile immediately after initializing cell

    def define_section_lists(
        self,
        minimum_length: float = minimum_length,
        minimum_diameter: float = minimum_diameter,
    ) -> None:
        """
        This function creates categorized NEURON SectionLists

        section lists include: somatic, lateral, medial, dendrites, and all
        mentioned prior without filopodia (section list+_nofilopodia).

        Parameters
        ----------
        minimum_length : float
            minimum length (µm) of a section allowed before deemed filopodia
        minimum_diameter : float
            minimum diameter (µm) of a section allowed before deemed filopodia
        """
        self.cm = 0.9
        self.Ra = 200
        self.somatic = self.soma
        self.lateral = self.apic
        self.medial = self.dend
        # apical & dend label used to identify dendritic poles
        # (labeled in Neurolucida)

        self.dendrites = self.medial + self.lateral
        self.allsec = self.somatic + self.dendrites

        self.medial_nofilopodia = self.medial
        self.lateral_nofilopodia = self.lateral
        self.allsec_nofilopodia = self.allsec
        self.dendrites_nofilopodia = self.dendrites

        # filopodia list removal and disconnect
        while True:
            deleted = False
            for sec in tiplist(self.allsec):
                # if too short and thin
                if sec.L < minimum_length and sec.diam < minimum_diameter:
                    sec.disconnect()  # detach filopodia electrically but section still exists
                    self.allsec_nofilopodia.remove(sec)
                    if sec in self.dendrites_nofilopodia:
                        self.dendrites_nofilopodia.remove(sec)
                    if sec in self.lateral_nofilopodia:
                        self.lateral_nofilopodia.remove(sec)
                    if sec in self.medial_nofilopodia:
                        self.medial_nofilopodia.remove(sec)
                    deleted = True
            if deleted == False:
                break
        # cycles through until no sections matching criteria remain in
        # _nofilopodia section list

    def __init__(self, cell_file: str) -> None:
        """
        Parameters
        ----------
        cell_file : str
            The filepath for a morphology file in .ASC format from Neurolucida
        """
        self.filepath = cell_file
        self.cell_name = Path(self.filepath).stem
        morph_reader = h.Import3d_Neurolucida3()
        morph_reader.input(cell_file)
        i3d = h.Import3d_GUI(morph_reader, False)
        i3d.instantiate(self)
        self.define_section_lists()

    def assign_properties(
        self,
        seg_density: float = seg_density,
        conductance_set: list = [0.04, 0.001, 0.02],
    ) -> None:
        """
        This function creates compartments, electrical properties, and channel
        mechanisms/conductances.

        If the argument 'seg_density' isn't passed in, the class
        attribute'seg_density' is used.

        Parameters
        ----------
        seg_density: float, optional
            The density of segments created, per micron.
        """

        for sec in self.allsec:
            # add sections to respective groups
            sec.Ra = self.Ra  # Axial resistance in Ohm * cm
            sec.cm = self.cm
            sec.insert("mathews_KLT_deriv")
            sec.insert("khurana_ih")
            sec.insert("leak")
            sec.insert("nabel_KHT")
            sec.ek = -90  # K reverse potential
            sec.eh = -39  # HCN reverse potential

            if sec in self.dendrites:
                length = sec.L
                seg_num = int(math.ceil(length * seg_density))
                sec.nseg = seg_num

                for seg in sec:
                    seg.mathews_KLT_deriv.gbar = conductance_set[2]  # KLVA conductance
                    seg.nabel_KHT.gbar = 0.00055
                    seg.khurana_ih.ghbar = conductance_set[1]  # IH channel conductance
                    seg.leak.e = -70  # leak reversal potential
                    seg.leak.g = 0.00005  # leakconductance
            if sec in self.somatic:
                sec.nseg = 3
                sec.insert("scott_na")
                sec.ena = 69
                for seg in sec:
                    seg.scott_na.gbar = 0.03
                    seg.mathews_KLT_deriv.gbar = conductance_set[
                        0
                    ]  # KLVA channel conductance
                    seg.nabel_KHT.gbar = 0.00055
                    seg.khurana_ih.ghbar = conductance_set[1]  # IH conductance
                    seg.leak.e = -70  # leak reversal potential
                    seg.leak.g = 0.00005  # leak conductance

    def attach_axon(self) -> None:
        """
        Attaches artificial axon to the soma of the Cell instance.
        Axon model morphology is based on Lehnert et al. (2014)
        """
        self.tais = h.Section(name="tais")
        self.tais.nseg = 3
        self.tais.L = 10
        self.tais.Ra = self.Ra
        self.tais.cm = self.cm
        self.tais.insert("scott_na")
        self.tais.insert("mathews_KLT_deriv")
        self.tais.insert("khurana_ih")
        self.tais.insert("pas")
        self.tais.ek = -90
        self.tais.eh = -35
        self.tais.ena = 69
        for segnum, seg in enumerate(self.tais):
            # tapering initial segment
            seg.diam = 1.64 - (((segnum + 1) / self.tais.nseg) * (1.64 - 0.66))
            seg.scott_na.gbar = 0.2
            seg.mathews_KLT_deriv.gbar = 0.155
            seg.khurana_ih.ghbar = 0.002
            seg.pas.g = 0.00005
            seg.pas.e = -70
        self.allsec_nofilopodia.append(self.tais)
        self.cais = h.Section(name="cais")
        self.cais.nseg = 3
        self.cais.L = 10
        self.cais.diam = 0.66
        self.cais.Ra = self.Ra
        self.cais.cm = self.cm
        self.cais.insert("scott_na")
        self.cais.insert("mathews_KLT_deriv")
        self.cais.insert("khurana_ih")
        self.cais.insert("pas")
        self.cais.ek = -90
        self.cais.eh = -35
        self.cais.ena = 69
        for seg in self.cais:
            seg.scott_na.gbar = 0.2
            seg.mathews_KLT_deriv.gbar = 0.155
            seg.khurana_ih.ghbar = 0.0002
            seg.pas.g = 0.00005
            seg.pas.e = -70
        self.tais.connect(self.somatic[0](0.5))
        self.cais.connect(self.tais)
        self.allsec_nofilopodia.append(self.cais)
        # creating and attaching node/internode pairs (default is 5)
        self.internodes = []
        self.nodes = []
        for ax_part_num in range(5):
            self.internodes.append(h.Section(name=f"internode_{ax_part_num}"))
            self.internodes[ax_part_num].L = 100
            self.internodes[ax_part_num].diam = 0.98
            self.internodes[ax_part_num].cm = 0.0111
            self.internodes[ax_part_num].Ra = self.Ra
            self.internodes[ax_part_num].insert("pas")
            for seg in self.internodes[ax_part_num]:
                seg.pas.e = -70
                seg.pas.g = 0.00002
            # checking if theres a node/internode already to connect to
            try:
                self.internodes[ax_part_num].connect(self.nodes[ax_part_num - 1])
            except:
                self.internodes[ax_part_num].connect(self.cais)
            self.nodes.append(h.Section(name=f"node_{ax_part_num}"))
            self.nodes[ax_part_num].L = 1
            self.nodes[ax_part_num].diam = 0.66
            self.nodes[ax_part_num].Ra = self.Ra
            self.nodes[ax_part_num].cm = self.cm
            self.nodes[ax_part_num].insert("scott_na")
            self.nodes[ax_part_num].insert("mathews_KLT_deriv")
            self.nodes[ax_part_num].insert("pas")
            self.nodes[ax_part_num].ek = -90
            # self.nodes[ax_part_num].eh = -35
            self.nodes[ax_part_num].ena = 69
            for seg in self.nodes[ax_part_num]:
                seg.pas.e = -70
                seg.pas.g = 0.005
                seg.scott_na.gbar = 0.2
                seg.mathews_KLT_deriv.gbar = 0.155
            self.nodes[ax_part_num].connect(self.internodes[ax_part_num])
        self.allsec_nofilopodia.extend(self.nodes)
        self.allsec_nofilopodia.extend(self.internodes)

    def set_artificial_resting_potential(
        self,
        resting_potential,
        current_limits=(-1, 1),
        current_step=0.1,
        current_override=None,
    ) -> None:
        """
        Creates an indefinite current injection as close to the given resting
        potential, by sweeping through a given range of possible current levels.

        Parameters
        ----------
        resting_potential: int
            desired artificial resting potential

        current_limits: tuple, optional
            end boundaries of the dc current sweeping test, in nanoamps.
                default = (-1,1)

        current_step: float, optional
            increments of the applied dc current in the sweeping test, in
            nanoamps
                default = (0.1)
        """

        self.artificial_potential_clamp = h.IClamp(self.somatic[0](0.5))

        self.artificial_potential_clamp.delay = 0
        self.artificial_potential_clamp.dur = 10**9  # maximum NEURON sim time
        # ensures dc current is constant throughout sim
        if current_override != None:
            self.artificial_potential_clamp.amp = current_override
            h.finitialize()
            h.continuerun(self.stabilization_time)
            self.artificial_resting_potential = float(self.somatic[0](0.5).v)
            return
        else:
            self.artificial_potential_clamp.amp = 0

        current_steps = np.arange(
            current_limits[0], current_limits[1] + current_step, current_step
        )
        closest_current = current_steps[0]
        closest_resting_potential = 0
        # sweeping through current values
        for current in current_steps:
            print(current)
            self.artificial_potential_clamp.amp = current

            h.finitialize()
            h.continuerun(self.stabilization_time)
            if abs(float(self.somatic[0](0.5).v) - resting_potential) < abs(
                closest_resting_potential - resting_potential
            ):

                closest_current = current
                closest_resting_potential = float(self.somatic[0](0.5).v)
            if (closest_resting_potential - resting_potential) > 0:
                break
        self.artificial_potential_clamp.amp = closest_current
        self.artificial_resting_potential = closest_resting_potential

    def get_time_constant(
        self, initv: float = -58.0, use_steady_state: bool = False, traces: bool = False
    ) -> float:
        """
        This function measures the time constant

        A current clamp is performed at the center of the soma for 10 ms at
        -0.01 nA. The return to resting potential is the portion used to
        measure the time constant.

        Parameters
        ----------
        initv : float, optional
            The voltage that the simulation is initialized with.
        use_steady_state : bool, optional
            Determines which voltage value should be used for time constant
            measurement (steady-state or absolute maximum). Default is False.
        traces : bool, optional
            Determines whether the current, voltage, and time vectors are
            returned from the function. Default is False.

        Returns
        -------
        tau : float
            Time constant calculated in ms
            Stored as an instance variable
        """

        # cannot use variable time step (voltage change may be too small?)
        self.cvode.active(0)

        time_vector = h.Vector().record(h._ref_t)
        voltage_vector = h.Vector().record(self.somatic[0](0.5)._ref_v)

        probe = h.IClamp(self.somatic[0](0.5))
        probe.delay = self.stabilization_time
        probe.dur = 10
        probe.amp = -0.01

        probe_current = h.Vector().record(probe._ref_i)
        trace_dict = {
            "time": time_vector,
            "voltage": voltage_vector,
            "current": probe_current,
        }
        h.finitialize(initv)
        h.dt = 1
        h.continuerun(self.stabilization_time)
        h.frecord_init()
        h.dt = 0.001
        h.continuerun(self.stabilization_time + 2 * probe.dur)

        current_end_ind = time_vector.indwhere(">=", probe.delay + probe.dur)
        current_stopped_voltage_vector = voltage_vector.c(current_end_ind)
        current_stopped_time_vector = time_vector.c(current_end_ind)
        max_voltage = voltage_vector.c(
            current_end_ind, time_vector.indwhere(">=", probe.delay + probe.dur + 2)
        ).max()

        if use_steady_state == True:
            max_voltage = voltage_vector[len(voltage_vector) - 1]
        resting_voltage = voltage_vector[
            time_vector.indwhere(">=", probe.delay + probe.dur) - 1
        ]
        two_thirds_voltage = (max_voltage - resting_voltage) * 0.63 + resting_voltage

        two_thirds_voltage_ind = current_stopped_voltage_vector.indwhere(
            ">=", two_thirds_voltage
        )
        time_at_two_thirds = current_stopped_time_vector[two_thirds_voltage_ind]
        tau = time_at_two_thirds - probe.delay - probe.dur
        if traces == True:
            return tau, trace_dict
        self.tau = tau
        self.cvode.active(1)
        return tau

    def get_resistances_and_resting_potential(
        self, traces: bool = False
    ) -> tuple[float, float, float]:
        """
        This calculates the membrane and input resistance and resting potential

        A current step is performed, from -3 nA to 3 nA, with increments of
        0.25 nA. Each steady state voltage is recorded for each step and
        used to calculate the input resistance. The membrane resistance
        is then calculated using the surdace area of the cell.

        Parameters
        ----------
        traces : bool, optional
            determines if the voltage and time vectors from each simulation are
            returned

        Returns
        -------
        input_resistance : float
        membrane_resistance : float
        resting_potential : float

        All are also stored as instance variables.
        """
        current_step_size = 0.25
        start_current = -3
        end_current = 3
        # calculate number of tests
        current_range = end_current - start_current
        num_current_steps = int((current_range) / current_step_size) + 1
        # create array to store steady state potentials
        steady_state_pots = np.zeros(num_current_steps)
        peak_pots = np.zeros(num_current_steps)
        # value to add resting potential values for averaging
        resting_pots = np.zeros(num_current_steps)

        time_vectors = []
        voltage_vectors = []

        # loop to run each current level
        for current_step_num in range(num_current_steps):
            h.dt = 1
            probe_current = (
                current_step_num * current_step_size
            ) + start_current  # calculating current test level
            # create and set current clamp
            probe = h.IClamp(self.somatic[0](0.5))  # creation
            probe.amp = probe_current  # current level (nA)
            probe.dur = 200  # duration (ms)
            probe.delay = self.stabilization_time  # delay before input (ms)
            # print(probe.amp)
            # creating vectors and starting sim
            voltage_vector = h.Vector().record(self.somatic[0](0.5)._ref_v)
            time_vector = h.Vector().record(h._ref_t)
            h.finitialize(-58)
            h.continuerun(probe.delay - 5)
            h.dt = 0.1
            # allow simulation values to equalize
            h.continuerun(self.stabilization_time + 300)
            # eliminate extra simulation runtime before current pulse
            ind_pre_probe = time_vector.indwhere(">=", probe.delay) - 5
            resized_voltage_vector = voltage_vector.remove(0, ind_pre_probe)
            resized_time_vector = time_vector.remove(0, ind_pre_probe)

            # resting potential measured
            resting_voltage = resized_voltage_vector[0]
            max = 0

            # taking voltage measurement at steady state
            steady_state_voltage = resized_voltage_vector[
                resized_time_vector.indwhere(">=", probe.delay + 150)
            ]

            if (
                resized_voltage_vector.cl(
                    0, resized_time_vector.indwhere(">=", probe.delay + 150)
                ).min()
                < steady_state_voltage
                and resized_voltage_vector.cl(
                    0, resized_time_vector.indwhere(">=", probe.delay + 150)
                ).min()
                < resting_voltage - 1
            ):
                peak_voltage = resized_voltage_vector.min()

            else:
                peak_voltage = resized_voltage_vector.max()

            steady_state_pot = steady_state_voltage - resting_voltage
            peak_pot = peak_voltage - resting_voltage
            # add to total for average
            resting_pots[current_step_num] = resting_voltage
            # recording steadystate potential
            steady_state_pots[current_step_num] = steady_state_pot
            peak_pots[current_step_num] = peak_pot
            # resizing time scale to account for extra simulation removal
            resized_time_vector = resized_time_vector.add(-probe.delay)

            time_vectors.append(resized_time_vector.c())
            voltage_vectors.append(resized_voltage_vector.c())

        # calculate line of best fit for resistance
        self.input_resistance, intercept = np.polyfit(
            np.arange(
                start_current, end_current + current_step_size, current_step_size
            ),
            steady_state_pots,
            1,
        )
        self.ss_plot = (
            np.arange(
                start_current, end_current + current_step_size, current_step_size
            ),
            steady_state_pots,
        )

        self.peak_input_resistance, intercept = np.polyfit(
            np.arange(
                start_current, end_current + current_step_size, current_step_size
            ),
            peak_pots,
            1,
        )
        self.peak_plot = (
            np.arange(
                start_current, end_current + current_step_size, current_step_size
            ),
            peak_pots,
        )

        self.resting_potential = resting_pots.mean()

        total_area = 0
        for sec in self.allsec:
            for seg in sec:
                total_area += seg.area()
        self.surface_area = total_area
        self.membrane_resistance = total_area * self.input_resistance * 100
        self.membrane_capacitance = total_area * self.cm
        probe = None
        trace_dict = {"time": time_vectors, "voltage": voltage_vectors}
        if traces == True:
            return (
                self.input_resistance,
                self.membrane_resistance,
                self.resting_potential,
                trace_dict,
            )

        return (self.input_resistance, self.membrane_resistance, self.resting_potential)
