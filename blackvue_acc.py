"""
Get accelerometer records out of BlackVue video. Currently outputs CSV files,
with support for more formats added later.

Usage:
  blackvue_acc --to-csv <filename>

"""
import csv
import logging
import os
import warnings

import pandas as pandas
from docopt import docopt

import blackclue


def parse_blackvue_3gf_txt(filename):
    """
    Parse a 3gf.txt file as created by the blackclue tool.

    :param filename: the location of the BlackVue mp4 associated with a
    3gf.txt as string
    :return: a list of GForcePoint
    """
    filename = filename.replace(".mp4", ".3gf.txt")
    columnnames = ['id', 'ms_since_start_hex', 'y_hex',
                   'x_hex', 'z_hex', 'ms_since_start',
                   'y_int', 'x_int', 'z_int']
    try:
        df = pandas.read_csv(filename,
                             sep='\s+',
                             names=columnnames)
        df['y'] = df['y_int'] / 128  # TODO wild guess factor is high here
        df['x'] = df['x_int'] / 128  # 1G is assumed to be 128 as integer
        df['z'] = df['z_int'] / 128  # based on what the sensor for y registers
        return df
    except FileNotFoundError:
        warnings.warn('No accelerometer data for {filename}'.format(
            filename=filename))
        return pandas.DataFrame(columns=columnnames + ['y', 'x', 'z'])


def list_of_namedtuple_to_csv(list_of_tuples, outputfilename):
    """
    Write a list of namedtuples to a csv file.

    :param list_of_tuples: a list of namedtuples of the same type
    :param outputfilename: a target output filename
    """
    fields = []
    if len(list_of_tuples) > 0:
        fields = list_of_tuples[0]._fields
    with open(outputfilename, 'w') as w:
        csvwriter = csv.writer(w)
        csvwriter.writerow(fields)
        for row in list_of_tuples:
            csvwriter.writerow(row)


def main(**kwargs):
    if len(kwargs) == 0:
        kwargs = docopt(__doc__)
    tocsv = kwargs.get('--to-csv')
    filename = kwargs.get('<filename>')
    if filename:
        if os.path.isfile(filename):
            logging.info(
                'Parsing the file {filename}'.format(filename=filename)
            )
            records = parse_blackvue_3gf_txt(filename=filename)
            if tocsv:
                outputfilename = filename.replace('.mp4', '.acc.csv')
                records.to_csv(outputfilename)
        elif os.path.isdir(filename):
            logging.info(
                'Parsing all mp4-files in the folder {filename}'.format(
                    filename=filename
                )
            )
            foldername = filename
            for filename in filter(lambda x: x.endswith('.mp4'),
                                   os.listdir(foldername)):
                blackclue.dump(file=[os.path.join(foldername, filename)],
                               dump_embedded=True,
                               dump_raw_blocks=False,
                               extended_scan=False,
                               verbose=False)
                records = parse_blackvue_3gf_txt(filename=os.path.join(
                    foldername, filename))
                if tocsv:
                    outputfilename = filename.replace('.mp4', '.acc.csv')
                    records.to_csv(os.path.join(foldername, outputfilename))
        else:
            logging.error('The file or folder {filename} does not '
                          'exist'.format(filename=filename)
                          )


if __name__ == "__main__":
    main(**docopt(__doc__))
