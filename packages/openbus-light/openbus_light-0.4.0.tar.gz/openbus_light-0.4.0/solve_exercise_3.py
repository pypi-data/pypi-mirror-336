import json
import os.path
import subprocess
import sys
from collections.abc import Mapping
from concurrent.futures import ProcessPoolExecutor
from enum import IntEnum, unique
from pathlib import Path
from typing import Sequence

import plotly.graph_objects as go
from _constants import RESULT_DIRECTORY
from plotly.subplots import make_subplots

from openbus_light.model import CHF
from openbus_light.plan import Summary
from openbus_light.plan.network import Activity
from openbus_light.plot import create_colormap


@unique
class _Experiment(IntEnum):
    BENCHMARK = 0
    FREE_VEHICLE = 1
    CHEAP_VEHICLE = 2
    MEDIUM_VEHICLE = 3
    EXPENSIVE_VEHICLE = 4
    RIDICULOUSLY_EXPENSIVE_VEHICLE = 5


def _run_experiment(args: list[str]) -> None:
    """
    Executes the line planning problem with given command line arguments using the current Python interpreter.
    :param args: List of command-line arguments for the script.
    """
    current_python_interpreter = sys.executable
    command_line_arguments = [current_python_interpreter, "exercise_3.py"] + args
    print(f"Running experiment with arguments: {command_line_arguments}")
    code = subprocess.run(command_line_arguments, check=True)
    print(f"Experiment finished with exit code: {code}, (0 means success)")
    assert code == 0, f"Experiment failed with exit code: {code}"


def _map_parameters_to_experiment_id() -> Mapping[_Experiment, list[str]]:
    """
    Maps the experiment ID to the command-line arguments for the line planning problem.
    :return: A dictionary mapping the experiment ID to the command-line arguments.
    """
    return {
        # Benchmark with current frequencies
        _Experiment.BENCHMARK: ["--use_current_frequencies"],
        # Four experiments with variable frequencies and different vehicle costs
        _Experiment.FREE_VEHICLE: ["--vehicle_cost_per_period=0"],
        _Experiment.CHEAP_VEHICLE: ["--vehicle_cost_per_period=100"],
        _Experiment.MEDIUM_VEHICLE: ["--vehicle_cost_per_period=200"],
        _Experiment.EXPENSIVE_VEHICLE: ["--vehicle_cost_per_period=500"],
        _Experiment.RIDICULOUSLY_EXPENSIVE_VEHICLE: ["--vehicle_cost_per_period=10000"],
    }


def _plot_results_with_subplots(data: Sequence[tuple[_Experiment, int, Mapping[Activity, CHF], CHF]]) -> go.Figure:
    """
    Plots the results of the experiments with subplots: One for the scatter plot of overall generalised_travel_times,
    and another for the bar plot showing the composition of the generalised_travel_times by activity.

    :param data: A list of tuples containing the experiment ID, the number of vehicles used,
    and the objective decomposed by Activity.
    """
    figure = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Overall Objective vs. Number of Vehicles", "Objective Composition by Activity"),
        specs=[[{"type": "scatter"}, {"type": "bar"}]],
    )

    # Scatter plot for overall objective
    cmap = create_colormap([experiment_id.name for experiment_id, _, _, _ in data] + list(Activity))
    for experiment_id, number_of_vehicles, generalised_travel_times, total_cost in data:
        figure.add_trace(
            go.Scatter(
                x=[number_of_vehicles],
                y=[total_cost],
                mode="markers",
                name=str(experiment_id.name),
                showlegend=True,
                legendgroup="Total Cost",
                marker={"color": cmap[experiment_id.name], "symbol": "star"},
            ),
            row=1,
            col=1,
        )
        figure.add_trace(
            go.Scatter(
                x=[number_of_vehicles],
                y=[sum(generalised_travel_times.values())],
                mode="markers",
                name=str(experiment_id.name),
                showlegend=True,
                legendgroup="Generalised Travel Times",
                marker={"color": cmap[experiment_id.name], "symbol": "square"},
            ),
            row=1,
            col=1,
        )

    # Stacked bar plot for objective composition by activity
    experiments_ran = [experiment_id.name for experiment_id, _, _, _ in data]
    for activity in Activity:
        figure.add_trace(
            go.Bar(
                x=experiments_ran,
                y=[result[2].get(activity, 0) for result in data],
                name=str(activity.name),
                marker={"color": cmap[activity]},
                showlegend=True,
            ),
            row=1,
            col=2,
        ),

    # add one more trace for the total cost
    figure.add_trace(
        go.Bar(
            x=experiments_ran,
            y=[result[3] - sum(result[2].values()) for result in data],
            name="Vehicle Cost",
            marker={"color": "black"},
            showlegend=True,
        ),
        row=1,
        col=2,
    )

    # Make the bars stacked
    figure.update_layout(barmode="stack", title_text="Experiment Results: Objective Analysis")

    figure.update_xaxes(title_text="Number of Vehicles", row=1, col=1, range=[0, None])
    figure.update_yaxes(title_text="Overall Objective (CHF/Period)", row=1, col=1, range=[0, None])
    figure.update_xaxes(title_text="Experiment ID", row=1, col=2)
    figure.update_yaxes(title_text="Objective by Activity (CHF/Period)", row=1, col=2)

    return figure


def extract_data_from_json(file_path: Path) -> tuple[_Experiment, int, Mapping[Activity, CHF], CHF]:
    """
    Extracts the experiment ID, the number of vehicles used, and the objective decomposed by Activity from a JSON file.
    :param file_path: Path, path to the JSON file
    :return: tuple[_Experiment, int, Mapping[Activity, CHFPerHour]], experiment ID, number of vehicles, and objective
    """

    with open(file_path, "r") as file:
        data: Summary = json.load(file)
        experiment_id = file_path.stem.split(".")[0]
        number_of_vehicles = data["used_vehicles"]
        passenger_cost = {Activity[key]: CHF(value) for key, value in data["weighted_cost_per_activity"].items()}
        total_cost = CHF(
            sum(passenger_cost.values()) + number_of_vehicles * data["used_parameters"]["vehicle_cost_per_period"]
        )
        return _Experiment(_Experiment[experiment_id]), number_of_vehicles, passenger_cost, total_cost


def main() -> None:
    """
    Runs the line planning problem with different vehicle experiments and plots the results.
    """
    parametrised_experiments = _map_parameters_to_experiment_id()

    with ProcessPoolExecutor() as executor:
        # Submit each experiment as a separate process, and run them concurrently (means your CPU cores will be busy)
        for experiment_id, args in parametrised_experiments.items():
            executor.submit(_run_experiment, [f"--experiment_id={_Experiment(experiment_id).name}"] + args)

    file_paths = [
        RESULT_DIRECTORY / f"{experiment.name}" / f"{experiment.name}.Summary.json"
        for experiment in parametrised_experiments.keys()
    ]
    result_figure = _plot_results_with_subplots([extract_data_from_json(file_path) for file_path in file_paths])
    result_figure.write_html(
        RESULT_DIRECTORY
        / f"result_{'_'.join(map(lambda x: str(x.value), sorted(parametrised_experiments.keys())))}.html"
    )
    result_figure.show()


if __name__ == "__main__":
    main()
