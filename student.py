from constants import Constants

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
