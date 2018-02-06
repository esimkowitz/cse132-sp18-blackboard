#!/usr/bin/env python
import sys, os, csv, json, re, math, httplib2, xlrd, argparse, time, pandas

from xlstojson import xlstojson
from datetime import datetime as dt
from datetime import date
from student import Student
from constantsTab import Constants
from grade import Grade
from shutil import copyfile


#Load constants from constants.py
constants = Constants()
lab_cutoffs = constants.labCutoffs
lab_cutoffs_secA = constants.labCutoffsSecA
lab_cutoffs_secB = constants.labCutoffsSecB
lab_cutoffs_secC = constants.labCutoffsSecC
gradebook_columns = {}
#figure out which labs have extra credit
labsWithExtraCredit = []
labGrades = []
studioGrades = []

def getKeyToUUID(roster_path):
    #Load dictionary mapping WUSTL key to Schoology UUID
    with open( roster_path ) as roster_file:
        roster = json.load(roster_file)
        uuid_map = {}
        for key in roster:
            uuid_map[key.lower()] = roster[key]["wk"]
        return uuid_map

def readWriteData( file_name ):
    #Turn CSV file into JSON file
    try:
        with open(file_name, 'r') as grades:
            with open("jsontemp", 'w') as form_results_json:
                reader = csv.DictReader(grades)
                form_results.seek()
                for row in reader:
                    json.dump(row, form_results_json)
                    form_results_json.write("\n")
                return form_results_json.name
    except:
        print "Invalid file name"
        sys.exit( 0 )

def readWriteDataExcel( file_name ):
    #Turn xls file into JSON file
    file_path = os.path.realpath(file_name)
    return xlstojson(file_path)
    

def process( mode, form_results_file, roster_file, gradebook_path ):
    #Initialize empty dict of students, to be filled from JSON file
    count = 0
    student_dict = {}
    student_dict_A = {}
    student_dict_B = {}
    student_dict_C = {}
    uuid_map = getKeyToUUID(roster_file.name)
    #Open JSON file
    roster_file.seek(0)

    roster = json.load(roster_file)
    roster_file.close()

    #add all students to student_dict, add each student to their own section's student_dict
    for key in roster:
        student_dict[roster[key]["wk"]] = Student(roster[key]["wk"], key)
        student_dict[roster[key]["wk"]].setSection(roster[key]["section"])
        # if( roster[key]["section"] == "a" ):
        #     student_dict_A[roster[key]["wk"]] = Student(roster[key]["wk"], key)
        # elif( roster[key]["section"] == "b" ):
        #     student_dict_B[roster[key]["wk"]] = Student(roster[key]["wk"], key)
        # elif( roster[key]["section"] == "c" ):
        #     student_dict_C[roster[key]["wk"]] = Student(roster[key]["wk"], key)
    try:        
        gradebook_file = open(gradebook_path, 'r')
        gradebook_file.seek(0)        
        gradebook = json.load(gradebook_file)
        try:
            loadGrades(student_dict, gradebook, uuid_map)
        except ValueError as e:
            print "ValueError: Error with loadGrades: %s" % e
        gradebook_file.close()    
        os.rename(gradebook_path, "old_gradebook_%i.json" % time.time())
    except IOError as e:
        if e.errno == 2:
            print "IOError: Gradebook is empty, skipping loadGrades"
        else:
            print "Unexpected IOError: %s"%e
    except ValueError as e:
        print "ValueError decoding JSON: %s"%e
    gradebook_file = open(gradebook_path, 'w')

    form_results = pandas.read_table(form_results_file)
    print len(form_results.index)


    regex = r"(?P<form_type>Assignment|Studio)( )?(?P<form_number>[0-9]+)"
    # regex = r"(?:CSE 132 (?P<semester>(?:SP|FL)[0-9]{2}) )?(?P<form_name>(?P<form_type>Assignment|Studio)( )?(?P<form_number>[0-9]+))(?:\([0-9]+\-[0-9]+\))"
    match_result = re.search(regex, form_results_file.name)
    form_type = match_result.group('form_type')
    form_name = "%s %s"%(form_type, match_result.group('form_number'))

    print "Processing form for " + form_name
    if (form_type.lower() == "studio" and mode != "studios") or (form_type.lower() == "assignment" and mode != "labs"):
        print "Error: form type and mode type don't match"
        sys.exit(0)
    
    gradebook_file.seek(0)
    if mode == "labs":
        print "Doing labs"
        #pass in each section's student dict as well as total
        doLabs( student_dict, form_name, form_results, uuid_map, student_dict_A, student_dict_B, student_dict_C )
    elif mode == "studios":
        print "Doing studios"
        doStudios( student_dict, form_name, form_results, uuid_map )
    else:
        print "Invalid assignment type."
        sys.exit( 0 )
    makeGradeBook(student_dict, gradebook_file)
    makeUploadFile(student_dict, form_name)
    gradebook_file.close()
    form_results_file.close()


def doLabs( student_dict, lab_name, form_results, uuid_map, student_dict_A, student_dict_B, student_dict_C ):
    # Calculate grades for the lab grading form entries
    if constants.labRubricUpToDate[lab_name]:
        for entry_tuple in form_results.iterrows():
            # entry = form_results[i]
            entry = entry_tuple[1]
            entry_number = entry_tuple[0]
            # print entry
            partners = []
            partners.append(
                str(int(entry[constants.labPartnerFields[lab_name][0]])))


            if entry[constants.labWorkingWithPartner[lab_name]] == "Yes":
                partners.append(
                    str(int(entry[constants.labPartnerFields[lab_name][1]])))

            score = 0
            for key in entry.index:
                if not key in constants.labNonGradingFields:
                    try:
                        field_score = float(entry[key])
                        score += field_score
                    except ValueError:
                        print key + " is not a grading field"

            if entry[constants.labCommitToGithub[lab_name]] != True:
                score -= 1
            partner_str = partners[0]
            if len(partners) > 1:
                partner_str += " and " + partners[1]
            print "Score for %s is %f"%(partner_str, score)


            if score > constants.maxScore[lab_name]:
                #make this a thing ~~~~~~~~~~
                # if not labsWithExtraCredit[lab_name]:
                print "ERROR: Invalid score for this assignment. Check that your non-grading fields are correct."
                sys.exit(1)

            time_string = entry[constants.labStartTime[lab_name]]

            try:
                timestamp = dt.strptime( time_string, "%Y-%m-%dT%H:%M:%S" )
            except ValueError:
                timestamp = dt.strptime( time_string, "%m/%d/%y %H:%M:%S" )
            
            ta_name = entry[constants.labTAName[lab_name]]

            entry_notes = None

            if constants.labNotes[lab_name] in entry:
                if str(entry[constants.labNotes[lab_name]]) != "":
                    entry_notes = str(entry[constants.labNotes[lab_name]])
            
            grade = Grade(lab_name, score, "assignment", timestamp, ta_name)
            for partner in partners:
                try:
                    student_dict[uuid_map[partner]].addGrade(grade)
                except KeyError:
                    print "KeyError: Unable to find key \"%s\" from entry %i"%(partner, entry_number)
            
        # Process late labs
        for k in student_dict.iterkeys():
            cur_student = student_dict[k]
            cur_section = cur_student.getSection()
            # if ( k in student_dict_A.keys() ):
            #     cur_section = "a"
            # elif ( k in student_dict_B.keys() ):
            #     cur_section = "b"
            # elif ( k in student_dict_C.keys() ):
            #     cur_section = "c"
            num_lates = cur_student.getLates()
            labs = cur_student.getLabs()

            #get student's section here 
            for lab in labs:
                lab_deadline = lab_cutoffs[lab]
                if ( cur_section is "a" ):
                    lab_deadline = lab_cutoffs_secA
                elif ( cur_section is "b" ):
                    lab_deadline = lab_cutoffs_secB
                elif (cur_section is "c" ):
                    lab_deadline = lab_cutoffs_secC
                lab_sub_time = cur_student.getGrades()[lab].getTimestamp()
                lab_is_regrade = cur_student.getGrades()[lab].getIsRegrade()

                if lab_sub_time > lab_deadline and not lab_is_regrade:
                    if ( lab_sub_time - lab_deadline ).days > 7:
                        student_dict[k].grades[lab].setPoints( 0 )
                    else:
                        #add this number to gradebook, so student can see how many
                        if num_lates < 2:
                            num_lates += 1
                        else:
                            #maybe get rid of 
                            num_lates += 1
                            student_dict[k].grades[lab].setPoints( 0 )
            if num_lates > student_dict[k].getLates():
                student_dict[k].setLates( num_lates )
    else:
        print "Rubric for %s is not up to date, please update the update the fields \
               in the constants file and try again."%lab_name

def doStudios( student_dict, studio_name, form_results, uuid_map ):

    if constants.studioRubricUpToDate[studio_name]:
        # Process studio attendance for each form entry
        for entry_tuple in form_results.iterrows():
            entry = entry_tuple[1]
            entry_number = entry_tuple[0]
            # print entry
            partners = []
            for partner_field in constants.studioPartnerFields[studio_name]:
                if partner_field != "":
                    if not math.isnan(entry[partner_field]):
                        partners.append(str(int(entry[partner_field])))

            time_string = entry[constants.studioStartTime[studio_name]]

            try:
                timestamp = dt.strptime(time_string, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                timestamp = dt.strptime(time_string, "%m/%d/%y %H:%M:%S")
            
            ta_name = entry[constants.studioTAName[studio_name]]

            grade = Grade(studio_name, 1, "studio", timestamp, ta_name)
            score_string = "Grade added for student(s) %s"
            partner_string = ""
            for partner in partners:
                try:
                    student_dict[uuid_map[partner]].addGrade(grade)
                    # print "Grade added for student " + uuid_map[partner] + " with ID " + partner
                    # print str(student_dict[uuid_map[partner]])
                    partner_string += "%s, "%partner
                except KeyError:
                    print "Unable to find student with ID " + partner
            print score_string%partner_string[0:len(partner_string)-2]
        # #Build studio CSV file
        # csv_data = []
        # headers = [ "Unique User ID" ] + [ "Studio " + str(k) for k in range( 1, 11 ) ]
        # csv_data.append( headers )
        # for k in student_dict.iterkeys():
        #     cur_student = student_dict[k]
        #     student_data_row = []
        #     student_data_row.append( cur_student.getInfo()[1] )
        #     student_studios = cur_student.getStudios()
        #     for assignment in headers[1::]:
        #         if assignment in student_studios.iterkeys():
        #             student_data_row.append( student_studios[assignment].getPoints() )
        #         else:
        #             student_data_row.append( 0 )
        #     csv_data.append( student_data_row )
        # studioGrades = csv_data
        # #Write studio CSV file
        # with open( "studiogrades.csv", "w" ) as f:
        #     print "Writing studiogrades.csv"
        #     csv_writer = csv.writer( f, delimiter="," )
        #     csv_writer.writerows( csv_data )
        #     print "Done writing studiogrades.csv"
    else:
        print "Rubric for %s is not up to date, please update the update the fields \
               in the constants file and try again." % studio_name


def makeUploadFile(student_dict, form_name):
    #Build CSV file for upload to Blackboard
    csv_data = []
    headers = ["Username"]
    headers.append(constants.column_ids[form_name])
    csv_data.append(headers)
    for k in student_dict.iterkeys():
        cur_student = student_dict[k]
        student_grades = cur_student.getGrades()
        
        if form_name in student_grades:
            student_data_row = []
            student_data_row.append(cur_student.getWKey())
            student_data_row.append(student_grades[form_name].getPoints())
            csv_data.append(student_data_row)
    #Write lab CSV file
    output_file_name = "grade_output.txt"
    with open(output_file_name, "w") as f:
        print "Writing %s"%output_file_name
        csv_writer = csv.writer(f, delimiter="\t")
        csv_writer.writerows(csv_data)
        print "Done writing %s"%output_file_name


def loadGrades(student_dict, grade_dict, uuid_map):
    print "Loading grades from gradebook"
    for student_uuid in grade_dict:
        for grade in grade_dict[student_uuid]["grades"]:
            grade_obj = Grade(grade["name"], grade["points"], grade["kind"],
                              grade["timestamp"], grade["grader"], grade["notes"], grade["isRegrade"])
            history = grade["history"]
            for old_grade in history:
                old_grade_obj = Grade(old_grade["name"], old_grade["points"], old_grade["kind"],
                                      old_grade["timestamp"], old_grade["grader"], old_grade["notes"], old_grade["isRegrade"])
                grade_obj.addHistory(old_grade_obj)
            student_dict[student_uuid].addGrade(grade_obj)
        student_dict[student_uuid].setLates(grade_dict[student_uuid]["lates"])


def makeGradeBook(student_dict, gradebook):
    gradebook_output = {}
    for student_id in student_dict:
        student = student_dict[student_id]
        student_output = {"grades": [], "lates": student.getLates()}
        student_grades = student.getGrades()
        for grade_key in student_grades:
            student_output["grades"].append(student_grades[grade_key].output())
        gradebook_output[student_id] = student_output
    # print json.dumps(gradebook_output)
    json.dump(gradebook_output, gradebook)


def maybe_new_file(file_path):
    if os.path.exists(file_path):
        return open(file_path, 'r+')
    else:
        return open(file_path, 'w')
            
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Given the outputs of a grading form, process the outputs and generate a CSV for updating grades in Blackboard.")

    parser.add_argument("type", choices=["studios", "labs"], 
                        help="Type of grading form being processed")
    parser.add_argument("input_path",
                        help="Path to grading form output file", metavar="FILE",
                        type=argparse.FileType('r'))
    parser.add_argument("--roster", dest="roster_path",
                        help="Path to the class roster file", metavar="FILE", default="roster.json",
                        type=argparse.FileType('r'))
    parser.add_argument("--gradebook", dest="gradebook_path",
                        help="Path to the class gradebook file", metavar="FILE", default="gradebook.json",
                        type=str)
    args = parser.parse_args()
    process( args.type, args.input_path, args.roster_path, args.gradebook_path ) #arg 0 = studio | lab | ext | blah, arg 1 = file to be processed

def doQuizzes( student_dict ):
    pass
