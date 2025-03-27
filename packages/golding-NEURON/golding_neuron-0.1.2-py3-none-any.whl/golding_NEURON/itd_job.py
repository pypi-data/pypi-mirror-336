# import necessary libraries and create global variables for parameters
from .fileaccess import get_package_path
from .cell import Cell
from .attributes import (
    tiplist,
    sectionlist_length,
    parentlist,)
from .data_collection import itd_test
from neuron import h
import os
import numpy as np
import glob
import pandas
from pathlib import Path
import dill
import logging
import itertools
import copy

logger = logging.getLogger(__name__)


class ITDJob:
    def __init__(
        self,
        filenames,
        iterables,
        **kwargs,
    ):
        for key in kwargs:
            self.__setattr__(key, kwargs[key])

        self.itd_args = {
            "axon": self.axon,
            "inhibition": self.inhibition,
            "excitation": self.excitation,
            "threshold": self.threshold,
            "numsyn": self.numsyn,
            "synspace": self.synspace,
            "numfiber": self.numfiber,
            "exc_fiber_gmax": self.exc_fiber_gmax,
            "inh_fiber_gmax": self.inh_fiber_gmax,
            "inh_timing": self.inh_timing,
            "axonspeed": self.axonspeed,
            "absolute_threshold": self.absolute_threshold,
            "traces": self.traces,
            "itd_range": kwargs["itd_range"],
            "itd_step": kwargs["itd_step"],
            "parallel": False,
        }

        self.iterables = iterables
        self.filenames = filenames

        # Gathering morphology file paths

        cell_filepaths = glob.glob(get_package_path("cells") + "/*.asc")
        self.double_cells = [
            "160112_06P",
            "151209_06_LOOK",
            "160126_08_LOOK",
            "160112_16P",
            "160305_01p",
            "160318_21p",
            "151201_06P",
            "160111_02P",
            "151217_12p",
            "151214_09p",
            "160105_14P",
            "160105_15P",
            "151210_04P_LOOK",
        ]
        self.quadruple_cells = [
            "160123_08_LOOK",
            "151201_05_LOOK",
            "160317_16_LOOK",
            "160112_26P_LOOK",
            "160112_20P_LOOK",
            "160112_19P",
            "160317_13p",
            "151209_03P",
            "151210_03P_LOOK",
            "160105_12P",
            "151214_10P",
            "151214_02or03",
            "151210_02P",
            "160105_10",
        ]

    def generate_tasks(
        self,
    ):
        # Distribute the tasks for each cell out to the parallel context
        print("distributing tasks")
        print(self.filenames)
        task_list = []

        for tempfilename in self.filenames:
            if  tempfilename in self.double_cells:
                amplify = 1.25
            elif tempfilename in self.quadruple_cells:
                amplify = 1.5
            else:
                amplify = 1
            iterable_arrays = {}
            print(self.iterables)
            self.itd_args["temp_file_name"] = tempfilename
            self.itd_args["amplification"] = amplify

            if not len(self.iterables) == 0:
                for iterable_key in self.iterables:
                    start, stop, step = self.iterables[iterable_key]
                    if start > stop:
                        step = -step
                    iterable_arrays[iterable_key] = list(
                        np.arange(start, stop + step, step)
                    )
                logger.info(f"iterable_arrays: {list(iterable_arrays.values())}")
                combinations = itertools.product(*list(iterable_arrays.values()))
                for combination in combinations:
                    logger.info(f"combo:{combination}")

                    for val, key in zip(combination, self.iterables):
                        self.itd_args[key] = val
                        # print(self.itd_args[iterable_key])
                    for trial in range(int(self.itd_trials)):
                        task_list.append(copy.deepcopy(self.itd_args))
                        # logger.info(f"appended: {self.itd_args}")

            else:
                for trial in range(int(self.itd_trials)):
                    print("running task")
                    task_list.append(copy.deepcopy(self.itd_args))
        return task_list

    # Make a list of all iterated delay values
    # create a function to be called several times by NEURON's parellel context


def itd_task(kwargs):
    """Run ITD tests and return results."""
    current_cell = Cell(f"{get_package_path("cells")}/{kwargs['temp_file_name']}.asc")
    kwargs.pop("temp_file_name")
    name = current_cell.cell_name
    # list to store data
    itd_threshold_probabilities = np.zeros(
        int(kwargs["itd_range"] / kwargs["itd_step"]) + 1
    )
    # assign properties and categorized section lists
    current_cell.assign_properties(seg_density=0.5)
    logger.info("task created with params:")
    # for key, kwarg in kwargs.items():
    # logger.info(f"{key}: {kwarg}")
    if kwargs["axon"]:
        current_cell.attach_axon()

    if kwargs["excitation"]:
        kwargs["exc_fiber_gmax"] = kwargs["exc_fiber_gmax"] * kwargs["amplification"]
    else:
        kwargs["exc_fiber_gmax"] = 0
    kwargs.pop("excitation")
    kwargs.pop("amplification")


    dendrite_tips = tiplist(current_cell.dendrites_nofilopodia)
    # Check if the cell has dendrites that are too short to fit a synapse
    for tip in dendrite_tips:
        tip_path = parentlist(tip)
        path_length = sectionlist_length(current_cell, tip_path)[0]
        if path_length < kwargs["numsyn"] * kwargs["synspace"]:
            return itd_threshold_probabilities, name
    # logger.info(
    #     f"itd test starting for {name}\n{(f"{key}:from{self.iterables[key][0]} to {self.iterables[key][1]} by {self.iterables[key][2]}" for key in self.iterables)}",
    # )
    # Run itd tests and return results

    test_results = itd_test(
        current_cell,
        current_cell.lateral_nofilopodia,
        current_cell.medial_nofilopodia,
        numtrial=1,
        **kwargs,
    )
    logger.info(f"{name} returned to task")
    # print("kwargs",kwargs)
    if kwargs["traces"]:
        logger.info("traces requested... returning")
        itd_threshold_probabilities, trace_output = test_results
        del current_cell
        return (itd_threshold_probabilities, name, trace_output)
    else:
        logger.info("traces not requested... returning w/o traces")
        itd_threshold_probabilities = test_results
        del current_cell
        return (itd_threshold_probabilities, name)


def save_csv(itd, name, *iterable_keys, **job_args):  # -> np.ndarray:
    """Save data into csv."""
    sweep_data = {"name": name}
    for key in iterable_keys:
        sweep_data[key] = job_args[key]
    itd_vals = np.arange(
        -job_args["itd_range"] / 2,
        job_args["itd_range"] / 2 + job_args["itd_step"],
        job_args["itd_step"],
    )
    if len(itd_vals) != len(itd):
        raise ValueError(
            f"Number of itd steps ({len(itd_vals)}) does not match number of itds tested ({len(itd)})"
        )
    for index, i in enumerate(itd_vals):
        sweep_data[i] = itd[index]
    df = pandas.DataFrame(sweep_data, index=[0])
    spreadsheetname = "itd_data.csv"
    if os.path.isfile(spreadsheetname):
        df.to_csv(spreadsheetname, mode="a", header=False)
    else:
        df.to_csv(spreadsheetname, mode="a")


def save_dill(
    trace_ret, name, id, job_name=None, *iterable_keys, **job_args
):  # -> np.ndarray:
    """Save traces into dills."""
    folder_string = ""
    path_without_iter = f"traces/{name}"
    if job_name is not None:
        path_without_iter = f"traces/{job_name}/{name}"

    if len(iterable_keys) != 0:
        for iterable in iterable_keys:
            folder_string += f"{iterable}_{job_args[iterable]}"
    else:
        folder_string = "no_iter"

    os.makedirs(f"{path_without_iter}/{folder_string}", exist_ok=True)
    serialized = dill.dumps(trace_ret)
    with open(
        f"{path_without_iter}/{folder_string}/{id}.pkl",
        "wb",
    ) as f:  # open a text file
        f.write(serialized)

    # Start the parallelization process


def open_itd_test_obj(dill_path):
    with open(dill_path, 'rb') as f:
        serialized = f.read()
    itd_tester = dill.load(serialized)
    # Creating NEURON's parallel context, to distribute tasks
    print("running")
    return itd_tester


def run_tasks(tasks, iterables, job_name="itd_job"):

    pc = h.ParallelContext()
    pc.runworker()

    iterated_dict = iterables
    for task in tasks:
        logger.info(f"task: {task}")
        pc.submit(itd_task, task)
    while pc.working():
        # Retrieve the finished data from the parallel context
        id = pc.userid()
        # print(id)
        submit_args = pc.upkpyobj()

        if submit_args["traces"]:
            (itd, name, trace_ret) = pc.pyret()
            save_dill(
                trace_ret, name, id, job_name, *iterated_dict.keys(), **submit_args
            )
            logger.info(f"{name} ({id}) dill saved")
        else:
            (itd, name) = pc.pyret()

        log_string = f"{name} ({id}) data retrieved\nargs:\n"
        for arg, val in submit_args.items():
            if arg in iterated_dict:
                log_string += f"\033[1m{arg}:{val}\033[0m\n"
            else:
                log_string += f"{arg}:{val}\n"
        logger.info(log_string)

        # Save data into csv
        save_csv(itd, name, *iterated_dict.keys(), **submit_args)
        logger.info(f"{name} ({id}) csv saved")
        # Save traces into dills


if __name__ == "__main__":
    search_path = glob.glob("/*.dill")
    if len(search_path) == 0:
        raise ValueError("No .dill file found in the current directory.")
    elif len(search_path) > 1:
        raise ValueError("Multiple .dill files found in the current directory.")
    dill_path = search_path[0]
    itd_tester = open_itd_test_obj(dill_path)
    tasks = itd_tester.generate_tasks()
    iterables = itd_tester.iterables
    run_tasks(tasks, iterables)