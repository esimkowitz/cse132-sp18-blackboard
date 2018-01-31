class Student:
    def __init__( self, wkey, uuid ):
        self.grades = {}
        self.info = ( wkey, uuid )
        self.lates = 0

    def addGrade( self, grade ):
        if not grade.name in self.grades.iterkeys():
            self.grades[grade.name] = grade
        elif grade.getIsRegrade() is True:
            self.grades[grade.name].regrade(grade)
        else:
            pass

    def getGrades( self ):
        return self.grades

    def getInfo( self ):
        return self.info

    def getLates( self ):
        return self.lates

    def setLates( self, numLates ):
        self.lates = numLates

    def getLabs( self ):
        return { k : v for k, v in self.grades.iteritems() if "Lab" in k and not "Late" in k }

    def getStudios( self ):
        return { k : v for k, v in self.grades.iteritems() if "Stu" in k }

    def printGrades( self ):
        for g in self.getGrades():
            print str( g )

    def __str__( self ):
        return str( self.info ) + ":\n " + str( [ str(g) for g in self.getGrades() ] )