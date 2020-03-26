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
    loc_to_counts = dict()

    with open(input_file, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        firstline = True
        for row in csvreader:
            if firstline:
                xticklabels = row[4:len(row)]
                firstline = False
                continue

            loc = (row[0] == "" and row[1] or row[0])
            loc_to_counts[loc] = [_int_or_zero(n) for n in row[4:len(row)]]

    return xticklabels, loc_to_counts

def _transformation(n, transformation):
    if transformation == "log":
        if n == 0.0:
            return None
        else:
            return math.log(n)
    elif transformation == "identity":
        return n
    else:
        exit.sys("Unknown transformation: " + transformation)

def _xtick_offset(num_xticks, num_recent_entries):
    if num_recent_entries is None:
        return num_xticks
    else:
        assert(num_recent_entries > 0 and num_recent_entries <= num_xticks)
        return num_recent_entries

def main(args):
    # date_to_rows = dict()
    # for entry in os.scandir(args.daily_reports_dir):
    #     if entry.path.endswith(".csv"):
    #         with open(entry.path, "r") as csvfile:
    #             reader = csv.DictReader(csvfile)
    #             for row in reader:
    #                 date_to_rows[entry.name].append(row)

    xticklabels, loc_to_counts = _csv(args.input)

    loc_to_scale = json.load(open(args.scaling_map, "r"))

    xtick_offset = _xtick_offset(len(xticklabels), args.num_recent_entries)

    fig, ax = plt.subplots()

    xtick_end = len(xticklabels)
    xtick_begin = xtick_end - xtick_offset

    for loc, counts in loc_to_counts.items():
        if loc in loc_to_scale:
            ax.plot(
                    [
                        _transformation(float(count) / (args.precision_factor * float(loc_to_scale[loc])), args.transformation)
                        for count in counts[xtick_begin:xtick_end]
                        ],
                    label=loc
                    )

    ax.set_ylabel(args.ylabel)
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

    parser.add_argument("--xlabel", "-x", type=str, action="store", default="Date",
            help="Label for x-axis")

    parser.add_argument("--ylabel", "-y", type=str, action="store", default="Count",
            help="Label for y-axis")

    parser.add_argument("--scaling-map", "-s", type=str, action="store", required=True,
            help="Path to JSON map from location to scaling factors")

    parser.add_argument("--precision-factor", "-p", type=float, action="store", default=1.0,
            help="Precision factor applied to scaling (use it to avoid precision errors with large numbers such as population size)")

    parser.add_argument("--title", "-t", type=str, action="store", required=True,
            help="Title string")

    parser.add_argument("--num-recent-entries", "-r", type=int, action="store", default=None,
            help="Number of recent entries to plot (default: all)")

    parser.add_argument("--transformation", "-f", type=str, action="store", choices=["identity", "log"], default="identity",
            help="Apply transformation function (default: identity)")

    main(parser.parse_args())
