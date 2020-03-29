#!/usr/bin/env python3

import os
import csv
import sys
import json
import math
import argparse

import matplotlib.pyplot as plt

def _int_or_zero(n):
    if n == "":
        return 0
    else:
        return int(n)

def _csv(input_file):
    xticklabels = None
    plotkey_to_counts = dict()

    with open(input_file, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        firstline = True
        for row in csvreader:
            if firstline:
                xticklabels = row[4:len(row)]
                firstline = False
                continue

            plotkey = row[1] + (row[0] != "" and "/" + row[0] or "")
            plotkey_to_counts[plotkey] = [_int_or_zero(n) for n in row[4:len(row)]]

    return xticklabels, plotkey_to_counts

def _transformed(n, transformation):
    if transformation is None:
        return n
    elif transformation == "log":
        if n == 0.0:
            return None
        else:
            return math.log(n)
    else:
        exit.sys("Unknown transformation: " + transformation)

def _xtick_offset(num_xticks, num_recent_entries):
    if num_recent_entries is None:
        return num_xticks
    else:
        assert(num_recent_entries > 0 and num_recent_entries <= num_xticks)
        return num_recent_entries

def _plot(ax, counts, label, y_fun):
    ax.plot(
            [
                y_fun(count)
                for count in counts
                ],
            label=label
            )

def main(args):
    # date_to_rows = dict()
    # for entry in os.scandir(args.daily_reports_dir):
    #     if entry.path.endswith(".csv"):
    #         with open(entry.path, "r") as csvfile:
    #             reader = csv.DictReader(csvfile)
    #             for row in reader:
    #                 date_to_rows[entry.name].append(row)

    xticklabels, plotkey_to_counts = _csv(args.input)
    plotkey_to_scales = json.load(open(args.scale_map, "r"))

    xtick_offset = _xtick_offset(len(xticklabels), args.num_recent_entries)

    fig, ax = plt.subplots()

    xtick_end = len(xticklabels)
    xtick_begin = xtick_end - xtick_offset

    for plotkey, counts in plotkey_to_counts.items():
        if plotkey in plotkey_to_scales:
            if args.scale_key is None:
                _plot(
                        ax,
                        counts[xtick_begin:xtick_end],
                        label=plotkey,
                        y_fun=lambda x: _transformed(x, args.transformation)
                        )
            elif args.scale_key in plotkey_to_scales[plotkey]:
                _plot(
                        ax,
                        counts[xtick_begin:xtick_end],
                        label=plotkey,
                        y_fun=lambda x: _transformed(x / (args.scale_factor * plotkey_to_scales[plotkey][args.scale_key]), args.transformation)
                        )

    ax.set_ylabel(
            (args.transformation is not None and args.transformation + "(" or "")
            + args.ylabel
            + (args.scale_key is not None and " / " or "")
            + (args.scale_factor != 1.0 and " (" or "")
            + (args.scale_key is not None and args.scale_key or "")
            + (args.scale_factor != 1.0 and " * " + str(args.scale_factor) + ")" or "")
            + (args.transformation is not None and ")" or "")
            )

    ax.set_xlabel(args.xlabel)

    ax.set_title(args.title)

    ax.set_xticks([0, xtick_offset-1])
    ax.set_xticklabels([xticklabels[xtick_begin], xticklabels[xtick_end-1]])

    plt.legend()
    plt.savefig(args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plott COVID-19.')

    parser.add_argument("--input", "-i", type=str, action="store", required=True,
            help="Input file path to CSV data by John Hopkins University")

    # parser.add_argument("--daily-reports-dir", "-d", type=str, action="store", required=True,
    #         help="Path to directory with daily reports (CSV files) by John Hopkins University")

    parser.add_argument("--output", "-o", type=str, action="store", required=True,
            help="Output file path (PNG)")

    parser.add_argument("--xlabel", "-x", type=str, action="store", required=True,
            help="Label for x-axis")

    parser.add_argument("--ylabel", "-y", type=str, action="store", required=True,
            help="Label for y-axis")

    parser.add_argument("--scale-key", "-k", type=str, action="store", default=None,
            help="Key to scale factors to be used, as defined in scale map")

    parser.add_argument("--scale-map", "-m", type=str, action="store", required=True,
            help="Path to scale map (JASON) mapping plot keys to scale factors")

    parser.add_argument("--scale-factor", "-p", type=float, action="store", default=1.0,
            help="Precision factor applied to scale (use it to avoid precision errors when scaling large y values)")

    parser.add_argument("--title", "-t", type=str, action="store", required=True,
            help="Title string")

    parser.add_argument("--num-recent-entries", "-r", type=int, action="store", default=None,
            help="Number of recent entries to plot (default: all)")

    parser.add_argument("--transformation", "-f", type=str, action="store", choices=["log"], default=None,
            help="Apply transformation function")

    main(parser.parse_args())
