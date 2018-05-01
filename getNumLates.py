import argparse
import json
import os

from grade import Grade
from student import Student, Students


def get_num_lates(roster_path, gradebook_path):
    grade_outputs_dir = "grade_outputs"
    roster_file = open(roster_path, 'r')
    gradebook_file = open(gradebook_path, 'r')
    students = Students(roster_file, gradebook_file)
    gradebook_file.close()
    roster_file.close()
    if not os.path.exists(grade_outputs_dir):
            os.mkdir(grade_outputs_dir)
    upload_filename = "%s/late_output.txt" %(grade_outputs_dir)
    students.makeUploadFile("Lates", upload_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Get number of late coupons for each student, output to Blackboard upload file")

    parser.add_argument("--roster", dest="roster_path",
                        help="Path to the class roster file", metavar="FILE", default="roster.json",
                        type=str)
    parser.add_argument("--gradebook", dest="gradebook_path",
                    help="Path to the class gradebook file", metavar="FILE", default="gradebook.json",
                    type=str)
    
    args = parser.parse_args()
    get_num_lates(args.roster_path, args.gradebook_path)
