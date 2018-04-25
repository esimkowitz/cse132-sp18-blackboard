import argparse
import json
import os

from grade import Grade
from student import Student, Students


def get_num_lates(roster_path, gradebook_path, output_path=None):
    roster_file = open(roster_path, 'r')
    gradebook_file = open(gradebook_path, 'r')
    students = Students(roster_file, gradebook_file)
    gradebook_file.close()
    roster_file.close()
    if output_path != None:
        if not os.path.exists(output_path):
            students.makeUploadFile("Lates", output_path)
            print "NumLates upload file saved to \"%s\"" % output_path
        else:
            print "Error: output file path \"%s\" already taken"%output_path
    else:
        print "Num lates per student:"
        num_lates = students.getNumLates()
        for student in num_lates.iterkeys():
            print "%s: %s"%(student, num_lates[student])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Get number of late coupons for each student in a gradebook")

    parser.add_argument("gradebook_path",
                        help="Path to the gradebook", metavar="FILE",
                        type=str)
    parser.add_argument("--output", "-o", dest="output_path",
                        help="Path to the output file (to upload to blackboard)", metavar="FILE",
                        default=None, type=str)
    parser.add_argument("--roster", dest="roster_path",
                        help="Path to the class roster file", metavar="FILE", default="roster.json",
                        type=str)

    args = parser.parse_args()
    get_num_lates(args.roster_path, args.gradebook_path,
                     args.output_path)
