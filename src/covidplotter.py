#!/usr/bin/env python3

import csv
import sys
import json
import math
import argparse
import urllib.request

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
        if n < 1.0:
            return 0.0
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
    loc_to_denominator = json.load(open(args.denominators, "r"))

    xticklabels, loc_to_counts = _csv(args.input)

    xtick_offset = _xtick_offset(len(xticklabels), args.num_recent_entries)

    fig, ax = plt.subplots()

    xtick_end = len(xticklabels)
    xtick_begin = xtick_end - xtick_offset

    for loc, counts in loc_to_counts.items():
        if loc in loc_to_denominator:
            ax.plot(
                    [
                        _transformation(float(count)/float(loc_to_denominator[loc]), args.transformation)
                        for count in counts[xtick_begin:xtick_end]
                        ],
                    label=loc
                    )

    ax.set_ylabel(args.transformation == "identity" and "Count" or "Count (" + args.transformation + ")")
    ax.set_xlabel("Date")

    ax.set_title(args.title)

    ax.set_xticks([0, xtick_offset-1])
    ax.set_xticklabels([xticklabels[xtick_begin], xticklabels[xtick_end-1]])

    plt.legend()
    plt.savefig(args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plott COVID-19.')

    parser.add_argument("--input", "-i", type=str, action="store", required=True,
            help="Input file path to CSV data by John Hopkins University")

    parser.add_argument("--output", "-o", type=str, action="store", required=True,
            help="Output file path (PNG)")

    parser.add_argument("--denominators", "-d", type=str, action="store", required=True,
            help="Path to map of locations to denominators")

    parser.add_argument("--title", "-t", type=str, action="store", required=True,
            help="Title string")

    parser.add_argument("--num-recent-entries", "-r", type=int, action="store", default=None,
            help="Number of recent entries to plot (default: all)")

    parser.add_argument("--transformation", "-f", type=str, action="store", default="identity",
            help="Apply transformation function. Options: identity, log (default: identity)")

    main(parser.parse_args())
