from neuron import h
from neuron.units import ms
import math
import numpy as np

h.load_file("stdrun.hoc")
h.load_file("import3d.hoc")


def tiplist(section_list: object) -> object:
    """
    This function finds all the terminating sections within a list

    Iterates over each section and identifying those without any 'children'.
    Also will include sections that are the endpoints within the given list,
    not necessarily absolutely endpoints. (i.e. no_filopodia lists will not
    consider excluded filopodia sections as end sections.)

    Parameters
    ----------
    section_list : SectionList
        list of sections to parse through

    Returns
    -------
    end_sections : SectionList
        list of end sections computed
    """

    sections = section_list
    end_sections = h.SectionList()
    # create section ref to utilize sectionref.child array
    section_ref = h.SectionRef()
    child_in_list = False
    for sec in sections:
        section_ref = h.SectionRef(sec=sec)
        # subtree = 1 -> no children
        if len(sec.subtree()) == 1:
            end_sections.append(sec)
        else:
            # check for non-absolute end sections (like omitting filopodia)
            for i in section_ref.child:
                if i in sections:
                    child_in_list = True
                    break
            if child_in_list:
                child_in_list = False
                continue
            end_sections.append(sec)

    return end_sections


def parentlist(
    section: object, starts_from_soma: bool = True, include_soma: bool = False
) -> object:
    """
    This function returns a list of all parent sections of a given section.

    Appends sections until the current section does not have a parent. Includes
    the given section. Functionality added for direction and soma inclusion.

    Parameters
    ----------
    section : h.Section
        section to find parent sections from
    starts_from_soma : bool, optional
        determines list order. Default is True (list begins from soma)
    include_soma : bool, optional
        determines soma inclusion. Default is False (soma not included)

    Returns
    -------
    parent_list : SectionList
        list of parent sections, including original given section.
    """

    parent_list = h.SectionList()
    parent_list_from_soma = h.SectionList()
    sectionref = h.SectionRef(section)  # SectionRef has 'has_parent' function

    while sectionref.has_parent():
        parent_list.append(sectionref.sec)
        sectionref = h.SectionRef(sectionref.parent)

    if include_soma == True:
        parent_list.append(sectionref.root)

    if starts_from_soma == True:
        for sec in reversed(list(parent_list)):
            parent_list_from_soma.append(sec)
        parent_list = parent_list_from_soma

    return parent_list


def sectionlist_length(
    cell: object, section_list: object, return_array: bool = True
) -> float | tuple[float, list]:
    """
    This function finds lengths of each section and the total length from list

    Adds each section length to a running total, while also storing each in a
    list. If the soma is included, only one half will be considered (for use
    with polar dendritic branches)

    Parameters
    ----------
    cell : Cell
        Cell instance to check for if a section is somatic
    section_list : SectionList
        list to pull section lengths from
    return_array : bool. optional
        Option to return an array of each section length.
    """

    total_length = 0
    length_array = []
    for sec in section_list:

        # halves length to measure from soma center
        if sec in cell.somatic:
            total_length += sec.L / 2
            length_array.append(sec.L / 2)
        else:
            total_length += sec.L
            length_array.append(sec.L)

    if return_array == True:
        return total_length, length_array

    return total_length


def furthest_point(cell: object, section_list: object) -> tuple[float, object]:
    """
    Calculates furthest segment and distance from soma within a section list.

    Cycles through each section and its segments, and updates the furthest
    segment. Utilizes distance3D() and getsegxyz() to find distance and
    coordinates of a segment, respectively.

    Parameters
    ----------
    cell : Cell
        Cell instance to find somatic compartment.
    section_list: SectionList
        list to parse through to find furthest segment within.

    Returns
    -------
    furthest_distance : float
        absolute distance from center of soma
    furthest_seg : Segment
        furthest Segment object from center of soma
    """
    furthest_distance = 0
    for sec in section_list:

        for seg in sec:
            seg_distance = distance3D(getsegxyz(cell.somatic[0](0.5)), getsegxyz(seg))
            if seg_distance > furthest_distance:
                furthest_distance = seg_distance
                furthest_seg = seg
    return furthest_distance, furthest_seg


def surface_area(section_list: object) -> float:
    """
    Sums surface area of each section and returns the total surface are of
    section_list

    Parameters
    ---------
    section_list : SectionList
        sections to add surface areas of

    Returns
    -------
    area : float
        total surface area of all section
    """
    area = 0
    for sec in section_list:
        for seg in sec:
            area += seg.area()
    return area


def distance3D(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    """
    Takes 2 3D coordinates and calculate the absolute distance from one another.

    Parameters
    ----------
    a : tuple(x,y,z)
        first 3D coordinate
    b : tuple(x,y,z)
        second 3D coordinate

    Returns
    -------
    distance : float
        absolute distance between given points
    """
    distance = abs(
        math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2) + ((a[2] - b[2]) ** 2))
    )
    return distance


def getsegxyz(seg: object) -> tuple[float, float, float]:
    """
    Returns the closest 3D coordinates of a given NEURON segment.

    Can be passed directly into distance3D.

    Parameters
    ----------
    seg : Segment
        segment to retrieve coordinates from

    Returns
    -------
    coords : tuple[x,y,z]
        Closest 3D coordinates of given segment

    """
    seg_location = seg.x  # 0-1 val
    section = seg.sec
    xyz_num = section.n3d()
    xyz_point = int(xyz_num * seg_location)  # finding nearest x,y,z measurement
    x = section.x3d(xyz_point)
    y = section.y3d(xyz_point)
    z = section.z3d(xyz_point)
    coords = (x, y, z)
    return coords


def average_path_length(section_list: object) -> float:
    """
    Finds the average pathlength from all paths to the soma in the section list

    Parameters
    ----------
    section_list: SectionList
        list of sections to find paths to the soma within

    Returns
    -------
    average_path_length : float
    """
    total_path_length = 0
    end_secs = tiplist(section_list)
    for sec in end_secs:
        for sec in parentlist(sec):
            length = sec.L
            total_path_length += length
    average_path_length = total_path_length / (len(list(end_secs)))
    return average_path_length


def mep(cell: object, section_list: object) -> float:
    """
    Calculates the mean electrotonic pathlength (MEP).
    Uses paths to soma from each section in section_list.

    MEP calculation based on (van Elburg and van Ooyen, 2010).

    Parameters
    ----------
    cell: Cell
        cell instance to pass along to pj()
    section_list: SectionList
        sections considered as 'endpoints' of a pathlength

    Returns
    -------
    mep : float
        calculated MEP value

    """
    sections = section_list
    pjarray = np.zeros(len(list(sections)))
    section_count = 0
    cell.get_resistances_and_resting_potential()

    def pj(cell: object, section_list: object) -> float:
        """
        Returns sum of electrotonic pathlengths. Used for MEP calculation.
        MEP calculation based on (van Elburg and van Ooyen, 2010).

        Parameters
        ----------
        cell : Cell
            instance of a Cell to pull membrane resistance from
        section_list: SectionList
            list of sections to calculate electrotonic pathlength

        Returns
        -------
        pj : float
            sum of electrotonic pathlengths
        """
        # array to store electrotonic pathlengths
        electrolength_array = np.zeros(len(list(section_list)))
        sectionCount = 0
        for sec in section_list:

            rm = cell.membrane_resistance  # cm^2 * Ω
            bi = (sec.diam / 2) / 10000  # cm
            numerator = bi * rm  # cm^3 * Ω
            denominator = 2 * sec.Ra  # Ω * cm
            tosqrt = numerator / denominator  # cm^2
            length_const = math.sqrt(tosqrt)  # cm

            length = sec.L / 10000  # cm
            electrolength = length / length_const

            electrolength_array[sectionCount] = electrolength
            sectionCount += 1

        pj = np.sum(electrolength_array)
        return pj

    for sec in sections:

        sec_parentlist = parentlist(sec)
        pjarray[section_count] = pj(cell, sec_parentlist)
        section_count += 1

    mep = np.sum(pjarray) / len(pjarray)
    return mep
