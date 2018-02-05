import json, datetime, sys

class Grade:
    def __init__( self, name, points, kind, timestamp, grader, isRegrade = False ):
        self.name = name
        self.points = points
        self.kind = kind
        if isinstance(timestamp, datetime.datetime):
            self.timestamp = timestamp
        else:
            try:
                self.timestamp = datetime.datetime.strptime( timestamp, "%Y-%m-%d %H:%M:%S" )
            except ValueError:
                self.timestamp = datetime.datetime.strptime( timestamp, "%Y-%m-%d %H:%M" )
            except:
                print "Error, unsupported type for timestamp: " + str(type(timestamp))
                sys.exit(1)
        self.isRegrade = isRegrade
        self.grader = grader
        self.history = []

    def getName( self ):
        return self.name

    def getPoints( self ):
        return self.points

    def setPoints( self, points ):
        self.points = points

    def getTimestamp( self ):
        return self.timestamp
        
    def getIsRegrade( self ):
        return self.isRegrade

    def getGrader( self ):
        return self.grader

    def getKind( self ):
        return self.kind

    def regrade( self, new_grade ):
        self.history.append(Grade(self.name, self.points, self.kind, self.timestamp, self.grader, self.isRegrade))
        self.name = new_grade.getName()
        self.points = new_grade.getPoints()
        self.timestamp = new_grade.getTimestamp()
        self.isRegrade = True
        self.grader = new_grade.getGrader()

    def getHistory( self ):
        return self.history
    
    def addHistory( self, old_grade ):
        self.history.append(old_grade)

    def output( self ):
        history = {}
        for grade in self.history:
            history.append(grade.output())
        grade_output = {
            "name": self.name,
            "points": self.points,
            "timestamp": str(self.timestamp),
            "kind": self.kind,
            "isRegrade": self.isRegrade,
            "grader": self.grader,
            "history": history
        }
        return grade_output

    def __str__( self ):
        return str( self.timestamp ) + ", " + str( self.name ) + ": " + str( self.points ) + " (isRegrade: " + isRegrade + ")" + "\n\thistory: " + str([str(grade) for grade in history])