class Grade:
	def __init__( self, name, points, kind, timestamp ):
		self.name = name
		self.points = points
		self.kind = kind
		self.timestamp = timestamp

	def getName( self ):
		return self.name

	def getPoints( self ):
		return self.points

	def setPoints( self, points ):
		self.points = points

	def getTimestamp( self ):
		return self.timestamp

	def __str__( self ):
		return str( self.timestamp ) + ", " + str( self.name ) + ": " + str( self.points )