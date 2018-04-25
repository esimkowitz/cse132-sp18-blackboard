import argparse
import json
import csv
import time
import os
import traceback
import sys
from student import Student, Students

def process(roster_file, gradebook_path, wustl_key=None):
    global students

    if wustl_key != None:
        print "Printing late labs for %s" % wustl_key
    else:
        print "Printing all late labs"

    gradebook_file = open(gradebook_path, 'r')
    students = Students(roster_file, gradebook_file)
    gradebook_file.close()

    roster_file.close()
    students.processLates()
    if wustl_key != None:
        try:
            students.get(wustl_key).printLateLabs()
        except KeyError as e:
            print "Unable to find student with WUSTL Key \"%s\""%wustl_key
        except Exception as e:
            raise e
    else:
        students.printLateLabs()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print out all the late assignments in the gradebook, optionally just for one student")
    parser.add_argument("-s", "--student", dest="wustl_key",
                    help="Print out lates for just the specified student", metavar="WUSTLKEY", default=None,
                    type=str)
    parser.add_argument("--roster", dest="roster_file",
                        help="Path to the class roster file", metavar="FILE", default="roster.json",
                        type=argparse.FileType('r'))
    parser.add_argument("--gradebook", dest="gradebook_path",
                        help="Path to the class gradebook file", metavar="FILE", default="gradebook.json",
                        type=str)
    args = parser.parse_args()
    process(args.roster_file, args.gradebook_path, args.wustl_key)
