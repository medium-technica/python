class Human:
	
	def __init__(self, gender):
		self.gender = gender
		print self,"Object created! with gender",self.gender
	
	def name_initiation(self, *args):
		self.fname = args[0]
		self.mname = args[1]
		self.lname = args[2]
		self.name = args[0]
		self.full_name = args[0]+" "+args[1]+" "+args[2]

abraham = Human('Male')
abraham.name_initiation('Abraham', 'Pollayil', 'Alexander')
print "Name of the Object:", abraham.name
