import math
import asciichartpy as asciichart
import re
from math import floor


def strip_ansi(o: str) -> str:
    pattern = re.compile(r"\x1B\[\d+(;\d+){0,2}m")
    stripped = pattern.sub("", o)
    return stripped


def plot(y_array, config=None):
    config = config or {}

    if isinstance(y_array[0], list):
        y_array = y_array
    else:
        y_array = [y_array]

    for a in y_array:
        assert len(a) > 0, "Cannot plot empty array"

    original_width = len(y_array[0])
    if config.get("width"):
        new_y_array = []
        for arr in y_array:
            new_arr = []
            for i in range(config["width"]):
                new_arr.append(arr[floor(i * len(arr) / config["width"])])
            new_y_array.append(new_arr)
        y_array = new_y_array

    plot = asciichart.plot(y_array, config)

    full_width = max([len(strip_ansi(l)) for l in plot.split("\n")])

    # if there is no array for x we use a range
    x_array = config.get("x_array", range(original_width))

    # determine the overall width of the plot (in characters)
    plot_first_line = strip_ansi(plot.split("\n")[0])

    # get the number of characters reserved for the y-axis legend
    left_margin = len(re.split("┤|┼╮|┼", plot_first_line)[0]) + 1

    # the difference between the two is the actual width of the x axis
    width_x_axis = full_width - left_margin

    # get the number of characters of the longest x-axis label
    longest_x_label = max([len(str(l)) for l in x_array])
    tick_distance = longest_x_label + 2

    ticks = " " * (left_margin - 1)
    for i in range(width_x_axis):
        if (i % tick_distance == 0 and (i + tick_distance) < width_x_axis) or i == (
            width_x_axis - 1
        ):
            ticks += "┬"
        else:
            ticks += "─"

    last_tick_value = x_array[-1]

    tick_labels = " " * (left_margin - 1)
    if width_x_axis <= tick_distance:
        tick_labels += str(last_tick_value).rjust(
            width_x_axis - (len(tick_labels) - left_margin + 1)
        )
    else:
        for i in range(width_x_axis):
            # BPER: fix the x Axis
            tick_value = x_array[min(round(i / width_x_axis * original_width), original_width - 1)]
            if i % tick_distance == 0 and (i + tick_distance) < width_x_axis:
                tick_labels += str(tick_value).ljust(tick_distance)

                # final tick
                if i >= (width_x_axis - 2 * tick_distance):
                    tick_labels += str(last_tick_value).rjust(
                        width_x_axis - (len(tick_labels) - left_margin + 1)
                    )

    title = (
        f"{' ' * (left_margin + (width_x_axis - len(config.get('title', '')))//2)}{config.get('title', '')}\n"
        if "title" in config
        else ""
    )

    y_label = ""
    if "y_label" in config or isinstance(config.get("line_labels", None), list):
        if "y_label" in config:
            # y_label += f"{config['y_label'].rjust(left_margin + len(config['y_label'])//2)}{asciichart.reset}"
            y_label += f"{config['y_label'].rjust(left_margin + len(config['y_label'])//2)}"
        if isinstance(config.get("line_labels", None), list):
            legend = ""
            for i in range(min(len(y_array), len(config.get("line_labels")))):
                color = (
                    config.get("colors", [])[i]
                    if isinstance(config.get("colors", None), list)
                    else "default"
                )
                # legend += f"    {color}─── {config['line_labels'][i]}{asciichart.reset}"
                legend += f"    {color}─── {config['line_labels'][i]}"
            y_label += (
                " " * (full_width - 1 - len(strip_ansi(legend)) - len(strip_ansi(y_label)))
                + legend
            )
        y_label += f"\n{'╷'.rjust(left_margin)}\n"

    # x_label = f"\n{config.get('x_label', '').rjust(full_width - 1)}{asciichart.reset}" if 'x_label' in config else ''
    x_label = f"\n{config.get('x_label', '').rjust(full_width - 1)}" if "x_label" in config else ""
    return f"\n{title}{y_label}{plot}\n{ticks}\n{tick_labels}{x_label}\n"
