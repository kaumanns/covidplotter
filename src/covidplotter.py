#!/usr/bin/env python3

import os
import re
import csv
import sys
import json
import math
import argparse

import numpy as np
import matplotlib.pyplot as plt

def _int_or_zero(n):
    if n == "":
        return 0
    else:
        return int(n)

def _csv(input_file, key_fields, key_fields_delimiter, content_fields_begin):
    xticklabels = None
    plotkey_to_counts = dict()

    with open(input_file, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')

        firstline = True
        for row in csvreader:
            if firstline:
                xticklabels = row[content_fields_begin:len(row)]
                firstline = False
                continue

            plotkey = key_fields_delimiter.join([row[i] for i in key_fields if row[i] != ""])
            plotkey_to_counts[plotkey] = [_int_or_zero(n) for n in row[content_fields_begin:len(row)]]

    return xticklabels, plotkey_to_counts

def _xvalue_offset(num_xticks, num_recent_entries):
    if num_recent_entries is None:
        return num_xticks
    else:
        assert num_recent_entries > 0 and num_recent_entries <= num_xticks, "Invalid value for --num-recent-entries."
        return num_recent_entries

def _smaller(x, y):
    if y is None or x < y:
        return x
    elif x is None or x >= y:
        return y

def _larger(x, y):
    if y is None or x > y:
        return x
    elif x is None or x <= y:
        return y

def _yvalues(counts, scales, scale_key, scale_factor):
    if scale_key is None:
        return counts
    elif scale_key in scales:
        return [count / (scale_factor * scales[scale_key]) for count in counts]
    else:
        return None

def _plot(ax, plotkey_to_counts, plotkey_to_scales, xvalue_begin, xvalue_end, scale_key, scale_factor):
    min_yvalue = None
    max_yvalue = None

    for plotkey, scales in plotkey_to_scales.items():
        if plotkey in plotkey_to_counts:
            yvalues = _yvalues(
                    plotkey_to_counts[plotkey][xvalue_begin:xvalue_end],
                    scales,
                    scale_key,
                    scale_factor
                    )

            if yvalues is not None:
                min_yvalue = _smaller(min(yvalues), min_yvalue)
                max_yvalue = _larger(max(yvalues), max_yvalue)
                ax.plot(
                        yvalues,
                        label=plotkey
                        )

    return min_yvalue, max_yvalue

def _define_xaxis(ax, xticklabels, xlabel, num_recent_entries):
    xvalue_end = len(xticklabels)
    xvalue_begin = xvalue_end - _xvalue_offset(len(xticklabels), num_recent_entries)

    ax.set_xticks(np.arange(0, xvalue_end-xvalue_begin))
    ax.set_xticklabels(xticklabels[xvalue_begin:xvalue_end])

    ax.tick_params(axis="x", labelrotation=-60)

    ax.set_xlabel(xlabel)

    return xvalue_begin, xvalue_end

def _define_yaxis(ax, min_yvalue, max_yvalue, ysize, yscale, ylabel, scale_key, scale_factor):
    if yscale is not None:
        ax.set_yscale(yscale)
    else:
        if min_yvalue > 0:
            min_yvalue = 0

        yfraction = round((max_yvalue - min_yvalue) / (ysize * 2))
        ax.set_yticks(np.arange(min_yvalue, max_yvalue, step=round(yfraction, -(len(str(yfraction))-1))))

    ax.set_ylim(min_yvalue, max_yvalue)

    ax.set_ylabel(
            (yscale is not None and yscale + "(" or "")
            + ylabel
            + (scale_key is not None and " / " or "")
            + (scale_factor != 1.0 and " (" or "")
            + (scale_key is not None and scale_key or "")
            + (scale_factor != 1.0 and " * " + str(scale_factor) + ")" or "")
            + (yscale is not None and ")" or "")
            )

    ax.tick_params(right=True, labelright=True)

def _main(args):
    xticklabels, plotkey_to_counts = _csv(args.input, args.key_fields, args.key_fields_delimiter, args.content_fields_begin)

    with open(args.scale_map, "r") as jsonfile:
        plotkey_to_scales = json.load(jsonfile)

    _, ax = plt.subplots(
            figsize=args.figsize,
            dpi=args.dpi
            )

    xvalue_begin, xvalue_end = _define_xaxis(ax, xticklabels, args.xlabel, args.num_recent_entries)

    min_yvalue, max_yvalue = _plot(ax, plotkey_to_counts, plotkey_to_scales, xvalue_begin, xvalue_end, args.scale_key, args.scale_factor)

    _define_yaxis(ax, min_yvalue, max_yvalue, args.figsize[1], args.yscale, args.ylabel, args.scale_key, args.scale_factor)

    ax.grid(axis="x", color="green", alpha=.3, linewidth=2, linestyle=":")
    ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)

    ax.set_title(args.title)

    plt.legend()

    plt.savefig(args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot COVID-19 cases.')

    parser.add_argument("--input", "-i", type=str, action="store", required=True,
            help="Input file path to CSV data by John Hopkins University")

    parser.add_argument("--output", "-o", type=str, action="store", required=True,
            help="Output file path (PNG)")

    parser.add_argument("--key-fields", nargs="+", type=int, action="store", required=True,
            help="Indices of fields whose values are parse as keys")

    parser.add_argument("--key-fields-delimiter", type=str, action="store", default="/",
            help="Delimiter string for concatenating key field values")

    parser.add_argument("--content-fields-begin", type=int, action="store", required=True,
            help="Index of first content field")

    parser.add_argument("--xlabel", "-x", type=str, action="store", default="",
            help="Label for x-axis")

    parser.add_argument("--ylabel", "-y", type=str, action="store", default="",
            help="Label for y-axis")

    parser.add_argument("--scale-key", "-k", type=str, action="store", default=None,
            help="Key to scale factors to be used, as defined in scale map")

    parser.add_argument("--scale-map", "-m", type=str, action="store", required=True,
            help="Path to scale map (JASON) mapping plot keys to scale factors")

    parser.add_argument("--scale-factor", "-p", type=float, action="store", default=1.0,
            help="Precision factor applied to scale (use it to avoid precision errors when scaling large y values)")

    parser.add_argument("--title", "-t", type=str, action="store", default="",
            help="Title string")

    parser.add_argument("--num-recent-entries", "-r", type=int, action="store", default=None,
            help="Number of recent entries to plot (default: all)")

    parser.add_argument("--figsize", "-s", action="store", default="15,15",
            type=lambda x: type(x)==type("") and re.search("^\d+,\d+$", x) and tuple([int(x) for x in x.split(",")]),
            help="Figsize option passed to Matplotlib, as comma-separated tupel of integers")

    parser.add_argument("--dpi", "-d", type=int, action="store", default=80,
            help="DPI option passed to Matplotlib")

    parser.add_argument("--ytickstep", type=int, action="store", default=None,
            help="Steps for y ticks ")

    parser.add_argument("--yscale", "-f", type=str, action="store", default=None,
            help="Yscale option passed to Matplotlib")

    _main(parser.parse_args())
