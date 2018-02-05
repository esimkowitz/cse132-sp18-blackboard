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

# FIXME: we just want to map WUSTL Key to WUSTL Key
def getKeyToUUID(roster_path):
    #Load dictionary mapping WUSTL key to Schoology UUID
    with open( roster_path ) as roster_file:
        roster = json.load(roster_file)
        # mapLines = map( lambda x: tuple( x.split( ',' ) ), mapLines )
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
        if( roster[key]["section"] == "a" ):
            student_dict_A[roster[key]["wk"]] = Student(roster[key]["wk"], key)
        elif( roster[key]["section"] == "b" ):
            student_dict_B[roster[key]["wk"]] = Student(roster[key]["wk"], key)
        elif( roster[key]["section"] == "c" ):
            student_dict_C[roster[key]["wk"]] = Student(roster[key]["wk"], key)
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

    
    # form_results_json = readWriteData( file_name )

    # FIXME: repair the script for tab-delimited files
    # form_results.close()
    form_results = pandas.read_table(form_results_file)
    form_results.columns = map(str.lower, form_results.columns)
    # print form_results
    print len(form_results.index)
    # sys.exit(0)
    # form_results_json_path = readWriteDataExcel(form_results.name)


    regex = r"(?P<form_type>Assignment|Studio)( )?(?P<form_number>[0-9]+)"
    # regex = r"(?:CSE 132 (?P<semester>(?:SP|FL)[0-9]{2}) )?(?P<form_name>(?P<form_type>Assignment|Studio)( )?(?P<form_number>[0-9]+))(?:\([0-9]+\-[0-9]+\))"
    match_result = re.search(regex, form_results_file.name)
    form_type = match_result.group('form_type')
    form_name = "%s %s"%(form_type, match_result.group('form_number'))



    print "Processing form for " + form_name
    if (form_type.lower() == "studio" and mode != "studios") or (form_type.lower() == "assignment" and mode != "labs"):
        print "Error: form type and mode type don't match"
        sys.exit(0)
    # with open( form_results_json, 'r' ) as f:

    # 	for row in f:
    # 		#Get data from JSON encoded file created by readWriteData
    # 		data = json.loads( row )
    # 		typeOfDemo = data["What are you demoing?"]
    # 		if mode.lower()[0::-1] not in typeOfDemo.lower():
    # 			continue
    # 		#Format time properly
    # 		dateString = data["Timestamp"].split( " " )[0]
    # 		time_string = data["Timestamp"].split( " " )[1]
    # 		dateSplit = dateString.split( "/" )
    # 		if len(dateSplit[2]) < 4:
    # 			dateSplit[2] = "20" + dateSplit[2]
    # 		dateObject = date( int( dateSplit[2] ), int( dateSplit[0] ), int( dateSplit[1] ) ).strftime( "%b %d %Y" )
    # 		try:
    # 			timestamp = dt.strptime( str( dateObject ) + " " + time_string, "%b %d %Y %H:%M:%S" )
    # 		except:
    # 			timestamp = dt.strptime( str( dateObject ) + " " + time_string, "%b %d %Y %H:%M" )
    # 		#Assign other variables
    # 		if typeOfDemo == "Lab":
    # 			typeOfDemo = "Assignment"
    # 		#Fill student dictionary - generalized to handle studio input as well as exts/labs
    # 		wustlKeys = [ str(v) for k, v in data.iteritems() if "Key" in k and not v == "" ]
    # 		assignment = map( lambda x: str( x.split( " - " )[0] ), data[str(typeOfDemo) + " Being Demoed"].split(", ") )
    # 		for wk in wustlKeys:
    # 			if not wk in student_dict.iterkeys():
    # 				try:
    # 					student_dict[wk] = Student( wk, uuid_map[wk] )
    # 				except:
    # 					pass
    # 		#Add all assignments to students
    # 		points = -1
    # 		if typeOfDemo == "Assignment" or typeOfDemo == "Studio":
    # 			points = 1
    # 			for wk in wustlKeys:
    # 				if not wk == "":
    # 					if typeOfDemo == "Assignment":
    # 						typeOfDemo = "Lab"
    # 					g = Grade( assignment[0], points, typeOfDemo, timestamp )
    # 					try:
    # 						print str(g)
    # 						student_dict[wk].addGrade( g )
    # 					except:
    # 						pass
    # os.remove( form_results_json )
    #Do grading for right mode
    # form_results_file = open(form_results_json_path, 'r')
    # form_results_json = json.load(form_results_file)['sheet1']
    # form_results_file.seek(0)
    gradebook_file.seek(0)
    # print json.dumps(form_results_json)
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
    gradebook_file.close()
    form_results_file.close()



def loadGrades( student_dict, grade_dict, uuid_map ):
    print "Loading grades from gradebook"
    for student_uuid in grade_dict:
        for grade in grade_dict[student_uuid]["grades"]:
            grade_obj = Grade(grade["name"], grade["points"], grade["kind"], grade["timestamp"], grade["grader"])
            history = grade["history"]
            for old_grade in history:
                old_grade_obj = Grade(old_grade["name"], old_grade["points"], old_grade["kind"], old_grade["timestamp"], old_grade["grader"])
                grade_obj.addGrade(old_grade_obj)
            student_dict[student_uuid].addGrade(grade_obj)
        student_dict[student_uuid].setLates(grade_dict[student_uuid]["lates"])

def doLabs( student_dict, lab_name, form_results, uuid_map, student_dict_A, student_dict_B, student_dict_C ):
    #Calculate late coupon usage
    # print form_results[0]

    # Calculate grades for the lab grading form entries
    for entry_tuple in form_results.iterrows():
        # entry = form_results[i]
        entry = entry_tuple[1]
        entry_number = entry_tuple[0]
        # print entry
        partners = []
        for const in constants.labPartnerFields[0]:
            try:
                partners.append(str(int(entry[const])))
                break
            except KeyError:
                pass
        # partners.append(entry[6])

        if len(partners) < 1:
            print "Unable to find partner 1 for entry: " + str(entry_number)

        if entry[constants.labWorkingWithPartner] == "Yes":
            for const1 in constants.labPartnerFields[1]:
                try:
                    partners.append(str(int(entry[const1])))
                    break
                except KeyError:
                    pass
            if len(partners) < 2:
                print "Unable to find partner 2 for entry: " + str(entry_number)

        score = 0
        for key in entry.index:
            # print "key: " + key
            if not key in constants.labNonGradingFields:
                # print "key " + key + " is not in constants.labNonGradingFields"
                try:
                    field_score = float(entry[key])
                    score += field_score
                except ValueError:
                    print key + " is not a grading field"

        if entry[constants.labCommitToGithub] != True:
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

        time_string = entry[constants.labStartTime]

        try:
            timestamp = dt.strptime( time_string, "%Y-%m-%dT%H:%M:%S" )
        except ValueError:
            timestamp = dt.strptime( time_string, "%m/%d/%y %H:%M:%S" )
        
        ta_name = entry[constants.labTAName]
        
        grade = Grade(lab_name, score, "assignment", timestamp, ta_name)
        for partner in partners:
            try:
                student_dict[uuid_map[partner]].addGrade(grade)
            except KeyError:
                print "KeyError: Unable to find key \"%s\" from entry %i"%(partner, entry_number)
        
    # Process late labs
    for k in student_dict.iterkeys():
        cur_student = student_dict[k]
        cur_section = ""
        if ( k in student_dict_A.keys() ):
            cur_section = "a"
        elif ( k in student_dict_B.keys() ):
            cur_section = "b"
        elif ( k in student_dict_C.keys() ):
            cur_section = "c"
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

    #Build lab CSV file for writing
    csv_data = []
    headers = [ "WUSTL Key", "Unique User ID" ] + list( lab_cutoffs.iterkeys() ) + [ "LateLabs" ]
    csv_data.append( headers )
    for k in student_dict.iterkeys():
        student_data_row = []
        cur_student = student_dict[k]
        student_labs = cur_student.getLabs()
        student_data_row.append( cur_student.getInfo()[0] )
        student_data_row.append( cur_student.getInfo()[1] )
        for assignment in headers[2:len( headers )-1]:
            if assignment in student_labs.iterkeys():
                student_data_row.append( student_labs[assignment].getPoints() )
            else:
                student_data_row.append( 0 )
        student_data_row.append( cur_student.getLates() )
        csv_data.append( student_data_row )
    labGrades = csv_data
    #Write lab CSV file
    with open( "labgrades.csv", "w" ) as f:
        print "Writing labgrades.csv"
        csv_writer = csv.writer( f, delimiter="," )
        csv_writer.writerows( csv_data )
        print "Done writing labgrades.csv"

def doStudios( student_dict, studio_name, form_results, uuid_map ):

    # Process studio attendance for each form entry
    for entry_tuple in form_results.iterrows():
        entry = entry_tuple[1]
        entry_number = entry_tuple[0]
        # print entry
        partners = []
        for partner_field in constants.studioPartnerFields:
            if not math.isnan(entry[partner_field]):
                partners.append(str(int(entry[partner_field])))

        # for key in entry:
        #     if not key in constants.labNonGradingFields:
        #         try:
        #             field_score = float(entry[key])
        #             score += field_score
        #         except ValueError:
        #             print key + " is not a grading field"

        # if entry[constants.labCommitToGithub] != "True":
        #     score -= 1
        # print "Score for " + str(partners) + " is " + str(score)
        # if score > constants.maxScore[lab_name]:
        #     print "ERROR: Invalid score for this assignment. Check that your non-grading fields are correct."
        #     sys.exit(1)

        time_string = entry[constants.studioStartTime]

        try:
            timestamp = dt.strptime(time_string, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            timestamp = dt.strptime(time_string, "%m/%d/%y %H:%M:%S")
        
        ta_name = entry[constants.studioTAName]

        grade = Grade(studio_name, 1, "studio", timestamp, ta_name)
        for partner in partners:
            try:
                student_dict[uuid_map[partner]].addGrade(grade)
                print "Grade added for student " + uuid_map[partner] + " with ID " + partner
                print str(student_dict[uuid_map[partner]])
            except KeyError:
                print "Unable to find student with ID " + partner
    #Build studio CSV file
    csv_data = []
    headers = [ "Unique User ID" ] + [ "Studio " + str(k) for k in range( 1, 11 ) ]
    csv_data.append( headers )
    for k in student_dict.iterkeys():
        cur_student = student_dict[k]
        student_data_row = []
        student_data_row.append( cur_student.getInfo()[1] )
        student_studios = cur_student.getStudios()
        for assignment in headers[1::]:
            if assignment in student_studios.iterkeys():
                student_data_row.append( student_studios[assignment].getPoints() )
            else:
                student_data_row.append( 0 )
        csv_data.append( student_data_row )
    studioGrades = csv_data
    #Write studio CSV file
    with open( "studiogrades.csv", "w" ) as f:
        print "Writing studiogrades.csv"
        csv_writer = csv.writer( f, delimiter="," )
        csv_writer.writerows( csv_data )
        print "Done writing studiogrades.csv"

def maybe_new_file(file_path):
    if os.path.exists(file_path):
        return open(file_path, 'r+')
    else:
        return open(file_path, 'w')

def makeGradeBook( student_dict, gradebook ):
    gradebook_output = {}
    for student_id in student_dict:
        student = student_dict[student_id]
        student_output = { "grades": [], "lates": student.getLates()}
        student_grades = student.getGrades()
        for grade_key in student_grades:
            student_output["grades"].append(student_grades[grade_key].output())
        gradebook_output[student_id] = student_output
    # print json.dumps(gradebook_output)
    json.dump(gradebook_output, gradebook)
            
        

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
