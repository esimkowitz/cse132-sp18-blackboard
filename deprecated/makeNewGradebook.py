import csv, json, sys, os, re
from argparse import ArgumentParser


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

def is_path_free(parser, arg):
    if os.path.exists(arg):
        parser.error("The path %s is not empty!" % arg)
    else:
        return arg


def nameString(firstname, lastname):
    return "".join([firstname," ",lastname])


# regex = r"(?P<firstname>[a-zA-Z]+)\s+(?P<lastname>[a-zA-Z]+)\s*"

def createStudent(student_dict, roster_path):
    with open(roster_path, 'rt') as csvfile:
        csvfile.readline()

        reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        for row in reader:
            student_dict[row[3]] = {
                "name": [row[0], row[1]],
                "username": row[2],
                "studentID": row[3],
                "grades": "",
            }

# def addSectionList(section_dict, section_path, section_letter):
#     with open(section_path, 'rt') as section_file:
#         section_file.readline()
#         line = section_file.readline()
#         while line:
#             match = re.match(regex, line).groupdict()
#             # print nameString(match['firstname'], match['lastname'])
#             section_dict[nameString(match['firstname'], match['lastname'])]=section_letter
#             line = section_file.readline()



def makeNewRoster( gradebook, output_path):
    student_dict = {}
    createStudent(student_dict, gradebook)
    with open(output_path, 'w') as jsonfile:
        json.dump(student_dict, jsonfile)


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Generate a roster complete with section names, given rosters for each section.')
    # parser.add_argument("--roster", dest="filepath", required=True,
    #                     help="path to class roster CSV", metavar="FILE",
    #                     type=lambda x: is_valid_file(parser, x))

    parser.add_argument("--gradebook", dest="gradebook", required=True,
                        help="path to gradebook CSV", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("--output", dest="output", required=True,
                        help="path to output json file", metavar="FILE",
                        type=lambda x: is_path_free(parser, x))
    args = parser.parse_args()
    makeNewRoster( args.gradebook, args.output)

