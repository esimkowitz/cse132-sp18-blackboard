from constants import Constants
from grade import Grade
import json, os, csv
constants = Constants()

class Student:
    def __init__( self, wkey, student_id ):
        self.grades = {}
        self.wkey = wkey
        self.student_id = student_id
        self.section = None

    def addGrade(self, grade):
        if not grade.name in self.grades.iterkeys():
            self.grades[grade.name] = grade
        elif self.grades[grade.name].getIsRegrade() is True:
            # self.grades[grade.name].regrade(grade)
            pass
        elif grade.getTimestamp() == self.grades[grade.name].getTimestamp():
            old_grade_is_late = self.grades[grade.name].getIsLate()
            # old_grade_is_regrade = self.grades[grade.name].getIsRegrade()
            self.grades[grade.name] = grade
            self.grades[grade.name].setIsLate(old_grade_is_late)
        else:
            pass
    
    def addLab(self, grade):
        self.addGrade(grade)
        self.processLates()
        return self.grades[grade.getName()].getIsLate()

    def processLates(self):
        num_lates_counted = 0

        labs = self.getLabs()

        # get student's section here
        # Uncomment below for debugging
        # print "student: %s, labs: %s"%(cur_student.getWKey(), str(labs))
        sorted_labs = sorted(
            labs, key=lambda k: labs[k].getTimestamp())
        for lab in sorted_labs:
            lab_deadline = constants.labCutoffs[self.section][lab]
            lab_sub_time = labs[lab].getTimestamp()
            lab_is_regrade = labs[lab].getIsRegrade()

            # Uncomment below for debugging
            # if lab == lab_name:
            #     print "student: %s, lab: %s, sub_time: %s, deadline: %s"%(cur_student.getWKey(), lab, lab_sub_time, lab_deadline)
            if (lab_sub_time > lab_deadline):
                if(lab_sub_time - lab_deadline).days > constants.labNumLateDays[lab]:
                    # print "Super late lab for %s on %s" % (self.wkey, lab)
                    if lab_is_regrade != True:
                        self.grades[lab].setIsZero(True)
                else:
                    # add this number to gradebook, so student can see how many
                    if(self.grades[lab].getIsLate() == False):
                        self.grades[lab].setIsLate(True)

                        # print "Late lab for %s on %s" % (self.wkey, lab)
                    else:
                        # print"Late lab already known for %s on %s" % (self.wkey, lab)
                        pass
                    if num_lates_counted >= 2:
                        if lab_is_regrade != True:
                            self.grades[lab].setIsZero(True)
                        # print"Late lab for %s on %s with no late coupons left, no credit" % (self.wkey, lab)
                    else:
                        if lab_is_regrade != True:
                            self.grades[lab].setIsZero(False)

                num_lates_counted += 1
    
    def getSection( self ):
        return self.section

    def getGrades( self ):
        return self.grades

    def getWKey( self ):
        return self.wkey
    
    def getStudentID( self ):
        return self.student_id

    def getNumLates( self ):
        return len(self.getLateLabs())
    
    def setSection( self, section ):
        self.section = section

    def getLabs( self ):
        return{k: v for k, v in self.grades.iteritems() if (v.getKind() == "assignment")}
        
    def getLateLabs(self):
        return {k: v for k, v in self.grades.iteritems() if ((v.getKind() == "assignment") and(v.getIsLate() == True))}

    def getStudios( self ):
        return {k: v for k, v in self.grades.iteritems() if v.getKind() == "studio"}

    def printGrades( self ):
        for g in self.grades:
            print str(g)
    
    def printLateLabs(self):
        labs = self.getLateLabs()
        print self.wkey
        for lab in labs:
            print "\t%s; due: %s"%(str(labs[lab]), str(constants.labCutoffs[self.section][lab]))

    def __str__( self ):
        return  "(%s,%s)"%(str(self.wkey), str(self.student_id)) + ":\n " + str( [ str(g) for g in self.getGrades() ] )


class Students():

    def __init__(self, roster_file, gradebook_file=None):
        self.student_dict = {}
        roster_file.seek(0)
        roster = json.load(roster_file)
        for key in roster:
            self.student_dict[roster[key]["wk"]] = Student(roster[key]["wk"], key)
            self.student_dict[roster[key]["wk"]].setSection(roster[key]["section"])
        if (gradebook_file != None):
            try:
                gradebook_file.seek(0)
                gradebook = json.load(gradebook_file)
                try:
                    self.loadGrades(gradebook)
                except ValueError as e:
                    print"ValueError: Error with loadGrades: %s" % e
                gradebook_file.seek(0)
            except IOError as e:
                if e.errno == 2:
                    print "IOError: Gradebook is empty, skipping loadGrades"
                else:
                    raise e

    def loadGrades(self, grade_dict):
        print "Loading grades from gradebook"
        for student_uuid in self.student_dict.iterkeys():
            for grade in grade_dict[student_uuid]["grades"]:
                grade_obj = Grade(grade["name"], grade["points"], grade["kind"],
                                grade["timestamp"], grade["grader"], grade["notes"], isRegrade=grade["isRegrade"], isLate=grade["isLate"], isZero=grade["isZero"])
                history = grade["history"]
                for old_grade in history:
                    old_grade_obj = Grade(old_grade["name"], old_grade["points"], old_grade["kind"],
                                        old_grade["timestamp"], old_grade["grader"], old_grade["notes"], isRegrade=old_grade["isRegrade"],
                                        isLate=old_grade["isLate"], isZero=old_grade["isZero"])
                    grade_obj.addHistory(old_grade_obj)
                self.student_dict[student_uuid].addGrade(grade_obj)

    def makeGradeBook(self, gradebook_file):
        gradebook_output = {}
        for student_id in self.student_dict:
            student = self.student_dict[student_id]
            student_output = {"grades": []}
            student_grades = student.getGrades()
            for grade_key in student_grades:
                student_output["grades"].append(student_grades[grade_key].output())
            gradebook_output[student_id] = student_output
        gradebook_file.seek(0)
        json.dump(gradebook_output, gradebook_file)
        gradebook_file.seek(0)

    def makeUploadFile(self, form_name, output_file_name="grade_output.txt"):
        # Build CSV file for upload to Blackboard
        csv_data = []
        headers = ["Username"]
        headers.append(constants.column_ids[form_name])
        csv_data.append(headers)
        for k in self.student_dict.iterkeys():
            cur_student = self.student_dict[k]
            student_grades = cur_student.getGrades()

            if form_name in student_grades:
                student_data_row = []
                student_data_row.append(cur_student.getWKey())
                if student_grades[form_name].getIsZero():
                    student_data_row.append(0)
                else:
                    student_data_row.append(
                        student_grades[form_name].getPoints())
                csv_data.append(student_data_row)
        # Write lab CSV file
        with open(output_file_name, "w") as f:
            print "Writing %s" % output_file_name
            csv_writer = csv.writer(f, delimiter="\t")
            csv_writer.writerows(csv_data)
            print "Done writing %s" % output_file_name
    def get(self, key):
        return self.student_dict[key]
