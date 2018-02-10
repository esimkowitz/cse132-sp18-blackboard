class Student:
    def __init__( self, wkey, student_id ):
        self.grades = {}
        self.wkey = wkey
        self.student_id = student_id
        self.lates = 0
        self.section = None

    def addGrade( self, grade ):
        if not grade.name in self.grades.iterkeys():
            self.grades[grade.name] = grade
        elif grade.getIsRegrade() is True:
            self.grades[grade.name].regrade(grade)
        elif grade.getTimestamp() == self.grades[grade.name].getTimestamp():
            self.grades[grade.name] = grade
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
        return self.lates
    
    def setSection( self, section ):
        self.section = section

    def setLates( self, numLates ):
        self.lates = numLates

    def getLabs( self ):
        return { k : v for k, v in self.grades.iteritems() if ((v.getKind() == "assignment") and (v.getIsLate() == False))}

    def getStudios( self ):
        return {k: v for k, v in self.grades.iteritems() if v.getKind() == "studio"}

    def printGrades( self ):
        for g in self.grades:
            print str( g )

    def __str__( self ):
        return  "(%s,%s)"%(str(self.wkey), str(self.student_id)) + ":\n " + str( [ str(g) for g in self.getGrades() ] )
