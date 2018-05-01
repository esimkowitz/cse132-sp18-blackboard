import argparse
import json
import csv
import time
import os
import traceback
import sys
from student import Student, Students

def process(assignment_number, roster_file, gradebook_path):
    global current_gradebook_path
    global old_gradebook_path
    global students

    form_name = "Assignment %i" % assignment_number
    print "Rerunning grader for %s"%form_name

    current_gradebook_path = gradebook_path
    old_gradebook_path = None
    old_gradebook_dir = "old_gradebooks"
    grade_outputs_dir = "grade_outputs"

    try:
        gradebook_file = open(gradebook_path, 'r')
        students = Students(roster_file, gradebook_file)
        gradebook_file.close()
        if not os.path.exists(old_gradebook_dir):
            os.mkdir(old_gradebook_dir)
        old_gradebook_path = "%s/old_gradebook_%i.json" % (
            old_gradebook_dir, time.time())
        os.rename(gradebook_path, old_gradebook_path)
    except IOError as e:
        error("Unexpected IOError: %s" % e)
    except ValueError as e:
        error("ValueError decoding JSON: %s" % e)

    roster_file.close()
    try:
        students.processLates()
        gradebook_file = open(gradebook_path, 'w')
        students.makeGradeBook(gradebook_file)
        gradebook_file.close()
        if not os.path.exists(grade_outputs_dir):
            os.mkdir(grade_outputs_dir)
        upload_filename = "%s/assignment_%i_output.txt"%(grade_outputs_dir, assignment_number)
        students.makeUploadFile(form_name, upload_filename)
    except Exception as e:
        error("Unexpected error", e)


def revert_changes(file_path, old_file_path):
    print "Reverting to previous %s" % file_path
    if old_file_path != None:
        if os.path.exists(old_file_path):
            if os.path.exists(file_path):
                os.remove(file_path)
            os.rename(old_file_path, file_path)


def error(error_string, error_obj=None):
    global old_gradebook_path
    global current_gradebook_path
    if error_obj != None:
        traceback.print_exc(error_obj)
        print "\nERROR: %s. %s" % (error_string, error_obj)
    else:
        print"\nERROR: %s" % error_string
    revert_changes(current_gradebook_path, old_gradebook_path)
    print "Exiting"
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rerun the grading output for a given assignment")

    parser.add_argument("assignment_number", choices=[1, 2, 3, 5, 6, 7, 8, 10, 11, 12],
                        help="The number for the assignment to rerun", type=int, metavar="NUM")
    parser.add_argument("--roster", dest="roster_file",
                        help="Path to the class roster file", metavar="FILE", default="roster.json",
                        type=argparse.FileType('r'))
    parser.add_argument("--gradebook", dest="gradebook_path",
                        help="Path to the class gradebook file", metavar="FILE", default="gradebook.json",
                        type=str)
    args = parser.parse_args()
    process(args.assignment_number, args.roster_file, args.gradebook_path)
