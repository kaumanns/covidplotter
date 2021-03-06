#!/usr/bin/env python3

# Merge and normalise

import os
import csv
import sys
import argparse
import warnings
import collections

import dateparser

def _args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument("--primary-input", "-p", type=str, action="store", required=True,
            help="Input paths to CSV files.")

    parser.add_argument("--primary-key-fields", nargs="+", type=int, action="store", required=True,
            help="")

    parser.add_argument("--primary-value-fields-begin", type=int, action="store", required=True,
            help="")

    parser.add_argument("--secondary-input", "-s", type=str, action="store", default=None,
            help="Input paths to CSV files.")

    parser.add_argument("--secondary-key-fields", nargs="+", type=int, action="store", default=None,
            help="")

    parser.add_argument("--secondary-value-fields-begin", type=int, action="store", default=None,
            help="")

    parser.add_argument("--key-delimiter", type=str, action="store", default="/",
            help="")

    parser.add_argument("--csv-delimiter", type=str, action="store", default=",",
            help="")

    parser.add_argument("--output", "-o", type=str, action="store", required=True,
            help="")

    return parser.parse_args()

def _int_or_zero(n):
    if n == "":
        return 0
    else:
        return int(float(n))

def _csse_csv(path, key_fields, value_idx, csv_delimiter, key_delimiter):
    with open(path, "r") as csvfile:
        rows = list(csv.reader(csvfile, delimiter=csv_delimiter))

        value_labels =  [dateparser.parse(label).strftime("%d-%m-%Y") for label in rows[0][value_idx:]]

        blacklist = dict()

        key_to_values = dict()
        for row in rows[1:]:
            key = key_delimiter.join([row[i] for i in key_fields if row[i] != ""])
            values = [ _int_or_zero(n) for n in row[value_idx:] ]

            if key not in blacklist:
                if key in key_to_values:
                    # assert len(key_to_values[key]) == len(values), "Inconsistent number of values for same key between rows (got {}, expected {}), detected in in file \"{}\" at row \"{}\".".format(len(key_to_values[key]), len(values), path, csv_delimiter.join(row))
                    if len(key_to_values[key]) == len(values):
                        key_to_values[key] = list(map(lambda x,y: x+y, key_to_values[key], values))
                    else:
                        warnings.warn(
                                "Inconsistent number of values ({} and {}) for same key \"{}\" in file \"{}\" -- ignoring key.".format(
                                    len(key_to_values[key]),
                                    len(values),
                                    key,
                                    path
                                    )
                                )
                        key_to_values.pop(key)
                        blacklist[key] = True
                else:
                    key_to_values[key] = values

        if len(blacklist.items()) > 0:
            warnings.warn("Ignored keys: {}".format(blacklist.keys().__str__()))
            for key,_ in blacklist.items():
                assert key not in key_to_values

    return key_to_values, value_labels

def _main(args):
    key_to_values_primary, value_labels_primary = _csse_csv(
            args.primary_input,
            args.primary_key_fields,
            args.primary_value_fields_begin,
            args.csv_delimiter,
            args.key_delimiter
            )

    if args.secondary_input is None:
        key_to_values = collections.OrderedDict(sorted(key_to_values_primary.items()))

        with open(args.output, "w") as outfile:
            outfile.write(args.csv_delimiter.join(["location"] + value_labels_primary) + "\n")
            for key, values in key_to_values.items():
                outfile.write(args.csv_delimiter.join(["\"{}\"".format(key)] + [str(value) for value in values]) + "\n")

    else:
        key_to_values_secondary, value_labels_secondary = _csse_csv(
                args.secondary_input,
                args.secondary_key_fields,
                args.secondary_value_fields_begin,
                args.csv_delimiter,
                args.key_delimiter
                )

        assert value_labels_secondary[0] == value_labels_primary[0]
        value_labels = value_labels_primary
        value_labels.extend([elem for elem in value_labels_secondary if elem not in value_labels_primary])

        # Values from primary replace values from secondary.
        key_to_values = collections.OrderedDict(sorted({**key_to_values_secondary, **key_to_values_primary}.items()))

        with open(args.output, "w") as outfile:
            outfile.write(args.csv_delimiter.join(["location"] + value_labels) + "\n")
            for key, values in key_to_values.items():
                while len(values) < len(value_labels):
                    values.append("")
                assert len(values) == len(value_labels)

                outfile.write(args.csv_delimiter.join(["\"{}\"".format(key)] + [str(value) for value in values]) + "\n")

if __name__ == "__main__":
    _main(_args())

