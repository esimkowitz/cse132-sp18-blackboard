class Student:
    def __init__( self, wkey, student_id ):
        self.grades = {}
        self.wkey = wkey
        self.student_id = student_id
        self.section = None

    def addGrade(self, grade):
        if not grade.name in self.grades.iterkeys():
            self.grades[grade.name] = grade
        elif grade.getIsRegrade() is True:
            self.grades[grade.name].regrade(grade)
        elif grade.getTimestamp() == self.grades[grade.name].getTimestamp():
            old_grade_is_late = self.grades[grade.name].getIsLate()
            self.grades[grade.name] = grade
            self.grades[grade.name].setIsLate(old_grade_is_late)
        else:
            pass
    def getSection( self ):
        return self.section

    def getGrades( self ):
        return self.grades

    def getWKey( self ):
        return self.wkey
    
    def getStudentID( self ):
        return self.student_id

    def getLates( self ):
        return len(self.getLateLabs())
    
    def setSection( self, section ):
        self.section = section

    def getLabs( self ):
        return{k: v for k, v in self.grades.iteritems() if((v.getKind() == "assignment") and(v.getIsLate() == False))}
        
    def getLateLabs(self):
        return {k: v for k, v in self.grades.iteritems() if((v.getKind() == "assignment") and(v.getIsLate() == True))}

    def getStudios( self ):
        return {k: v for k, v in self.grades.iteritems() if v.getKind() == "studio"}

    def printGrades( self ):
        for g in self.grades:
            print str( g )

    def __str__( self ):
        return  "(%s,%s)"%(str(self.wkey), str(self.student_id)) + ":\n " + str( [ str(g) for g in self.getGrades() ] )
