import codecs
import csv
import os
import sys


def write_tsv(file_path, rows):
    """
    :param file_path:
    :param rows: a list of rows to be written in the tsv file. The rows are lists of items.
    :return:
    """
    csv.field_size_limit(sys.maxsize)
    with codecs.open(file_path, "w+", encoding="utf-8") as fp:
        tsv_writer = csv.writer(fp, delimiter='\t')
        for row in rows:
            tsv_writer.writerow(row)
            # tsv_writer.writerow(["index", "question11", "question2"])
            # tsv_writer.writerow(["0", sentence1, sentence2])


def read_tsv(file_path):
    """
    read a tsv into a nested python list.
    :param file_path:
    :return:
    """
    csv.field_size_limit(sys.maxsize)
    cached_list = []
    with codecs.open(file_path, "r", encoding="utf-8") as fp:
        tsv_reader = csv.reader(fp, delimiter='\t')
        for row in tsv_reader:
            cached_list.append(row)
    return cached_list


def append_tsv(file_path, rows):
    """
    :param file_path:
    :param rows: a list of rows to be written in the tsv file. The rows are lists of items.
    :return:
    """
    csv.field_size_limit(sys.maxsize)
    with codecs.open(file_path, "a+", encoding="utf-8") as fp:
        tsv_writer = csv.writer(fp, delimiter='\t')
        for row in rows:
            tsv_writer.writerow(row)


def segment_large_csv(file_path, destination_path, segmentation_length, duplicate_header=False):
    """
    segment a large file to several smaller files to a destination.
    If duplicate_header is True, the first line of  the original large file will be duplicated to every segmented files,
    results in the length of segmented file = segmentation_length + 1. which also means that
    :param file_path:
    :param destination_path:
    :param segmentation_length:
    :param duplicate_header:
    :return: how many files are segmented.
    """
    csv.field_size_limit(sys.maxsize)
    filename, file_extension = os.path.splitext(os.path.basename(file_path))
    header = None
    with codecs.open(file_path, "r", encoding="utf-8") as fp:
        csv_reader = csv.reader(fp)
        if duplicate_header:
            header = csv_reader.__next__()
            segmentation_length += 1
        j = 0
        while True:
            i = 0
            j += 1
            current_filepath = os.path.join(destination_path, filename + str(j) + file_extension)
            with codecs.open(current_filepath, "w+", encoding="utf-8") as fp:
                csv_writer = csv.writer(fp)
                if duplicate_header:
                    csv_writer.writerow(header)
                while i < segmentation_length:
                    try:
                        row = next(csv_reader)
                        csv_writer.writerow(row)
                        i += 1
                    except StopIteration:
                        return j


def segment_large_tsv(file_path, destination_path, segmentation_length, duplicate_header=False):
    """
    segment a large file to several smaller files to a destination.
    If duplicate_header is True, the first line of  the original large file will be duplicated to every segmented files,
    results in the length of segmented file = segmentation_length + 1. which also means that
    :param file_path:
    :param destination_path:
    :param segmentation_length:
    :param duplicate_header:
    :return: how many files are segmented.
    """
    csv.field_size_limit(sys.maxsize)
    filename, file_extension = os.path.splitext(os.path.basename(file_path))
    header = None
    with codecs.open(file_path, "r", encoding="utf-8") as fp:
        tsv_reader = csv.reader(fp, delimiter='\t')
        if duplicate_header:
            header = tsv_reader.__next__()
            segmentation_length += 1
        j = 0
        while True:
            i = 0
            j += 1
            current_filepath = os.path.join(destination_path, filename + str(j) + file_extension)
            with codecs.open(current_filepath, "w+", encoding="utf-8") as fp:
                tsv_writer = csv.writer(fp, delimiter='\t')
                if duplicate_header:
                    tsv_writer.writerow(header)
                while i < segmentation_length:
                    try:
                        row = next(tsv_reader)
                        tsv_writer.writerow(row)
                        i += 1
                    except StopIteration:
                        return j


def save_tsv_as_csv(tsv_file, csv_file=None):
    csv.field_size_limit(sys.maxsize)
    from mzutils.os_misc import parent_dir_and_name, basename_and_extension
    with codecs.open(tsv_file, "r", encoding="utf-8") as tfp:
        if csv_file is None:
            csv_file = os.path.join(parent_dir_and_name(tsv_file)[0], basename_and_extension(tsv_file)[0]) + '.csv'
        with codecs.open(csv_file, "w+", encoding="utf-8") as cfp:
            tsv_reader = csv.reader(tfp, delimiter='\t')
            csv_writer = csv.writer(cfp, delimiter=',')
            for row in tsv_reader:
                csv_writer.writerow(row)