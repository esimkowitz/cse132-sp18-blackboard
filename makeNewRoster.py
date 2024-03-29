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

def addSectionRoster(student_dict, roster_path, section_letter):
    with open(roster_path, 'rt') as csvfile:
        csvfile.readline()

        reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        for row in reader:
            student_dict[row[3]] = {
                "name": [row[0], row[1]],
                "wk": row[2],
                "section": section_letter,
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



def makeNewRoster(section_a_path, section_b_path, section_c_path, output_path):
    student_dict = {}
    # addSectionList(section_dict, section_a_path, 'a')       
    # addSectionList(section_dict, section_b_path, 'b')
    # addSectionList(section_dict, section_c_path, 'c')
    # print json.dumps(section_dict)
    addSectionRoster(student_dict, section_a_path, 'a')
    addSectionRoster(student_dict, section_b_path, 'b')
    addSectionRoster(student_dict, section_c_path, 'c')
    with open(output_path, 'w') as jsonfile:
        json.dump(student_dict, jsonfile)


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Generate a roster complete with section names, given rosters for each section.')
    # parser.add_argument("--roster", dest="filepath", required=True,
    #                     help="path to class roster CSV", metavar="FILE",
    #                     type=lambda x: is_valid_file(parser, x))

    parser.add_argument("--a", dest="section_a", required=True,
                        help="path to section A roster CSV", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("--b", dest="section_b", required=True,
                        help="path to section B roster CSV", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("--c", dest="section_c", required=True,
                        help="path to section C roster CSV", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    parser.add_argument("--output", dest="output", required=True,
                        help="path to output json file", metavar="FILE",
                        type=lambda x: is_path_free(parser, x))
    args = parser.parse_args()
    makeNewRoster(args.section_a, args.section_b, args.section_c, args.output)

