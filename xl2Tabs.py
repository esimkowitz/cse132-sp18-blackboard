#!/usr/bin/python
import argparse
import csv
import datetime
import os
import sys

import xlrd


def xl_to_tabs(input_file, output_file, sheet_num):
    workbook_path = input_file.name
    input_file.close()

    # if output_filepath != None:
    #     workbook_name, workbook_ext = os.path.splitext(workbook_path)
    #     output_filepath = "%s.txt" % workbook_name
    # if os.path.exists(output_filepath):
    #     print("Unable to convert Excel spreadsheet: Output filepath is not empty")
    #     sys.exit(1)

    # open the output csv
    # define a writer
    wr = csv.writer(output_file, delimiter="\t", quoting=csv.QUOTE_MINIMAL)

    # open the xlsx file
    myfile = xlrd.open_workbook(workbook_path, on_demand=True)
    # get a sheet
    mysheet = myfile.sheet_by_index(sheet_num)

    # write the rows
    for rownum in range(mysheet.nrows):
        curr_row = mysheet.row_slice(rownum)
        # print(curr_row)
        row_out = []
        for cell in curr_row:
            # print(i)
            if cell.ctype == xlrd.XL_CELL_DATE:
                cell_date = datetime.datetime(
                    *xlrd.xldate_as_tuple(cell.value, myfile.datemode))
                row_out.append(cell_date.strftime("%D %T"))
            else:
                row_out.append(cell.value)

        wr.writerow(row_out)

    myfile.release_resources()
    del myfile

    output_file.close()

    return output_file.name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Convert an Excel spreadsheet to a tab-delimited text file")

    parser.add_argument("input_file", help="Path to Excel file", metavar="FILE",
                        type=argparse.FileType(mode='r'))
    parser.add_argument("-s", "--sheet", dest="sheet", help="Sheet number to convert",
                        type=int, default=0, metavar="INT")
    parser.add_argument("-o", "--output", "--out", dest="output_file", help="Path to the output file, optional",
                        type=argparse.FileType(mode='w'), default=sys.stdout, metavar="FILE")
    args = parser.parse_args()
    xl_to_tabs(args.input_file, args.output_file, args.sheet)
