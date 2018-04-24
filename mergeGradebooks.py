from student import Students, Student
from grade import Grade
import json, os, argparse

def merge_gradebooks(roster_path, gradebook_path, other_gradebook_path, output_path):
    roster_file = open(roster_path, 'r')
    gradebook_file = open(gradebook_path, 'r')
    other_gradebook_file = open(other_gradebook_path, 'r')
    students = Students(roster_file, gradebook_file)
    gradebook_file.close()
    other_gradebook_dict = json.load(other_gradebook_file)
    other_gradebook_file.close()
    students.loadGrades(other_gradebook_dict)

    if not os.path.exists(output_path):
        output_file = open(output_path, 'w')
        students.makeGradeBook(output_file)
        output_file.close()
        print "Merged gradebook saved to %s"%output_path
    else:
        print "Error: output file path already taken"
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Merge two gradebooks together")

    parser.add_argument("first_gradebook_path",
                        help="Path to the first gradebook", metavar="FILE",
                        type=str)
    parser.add_argument("second_gradebook_path",
                        help="Path to the second gradebook", metavar="FILE",
                        type=str)
    parser.add_argument("output_path",
                        help="Path to the output file destination", metavar="FILE",
                        type=str)
    parser.add_argument("--roster", dest="roster_path",
                        help="Path to the class roster file", metavar="FILE", default="roster.json",
                        type=str)

    args = parser.parse_args()
    merge_gradebooks(args.roster_path, args.first_gradebook_path, args.second_gradebook_path, args.output_path)

