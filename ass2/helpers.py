# COMP3311 21T3 Ass2 ... Python helper functions
# add here any functions to share between Python scripts 
# you must submit this even if you add nothing

def getProgram(db,code):
	cur = db.cursor()
	cur.execute("select * from Programs where code = %s",[code])
	info = cur.fetchone()
	cur.close()
	if not info:
		return None
	else:
		return info

def getStream(db,code):
	cur = db.cursor()
	cur.execute("select * from Streams where code = %s",[code])
	info = cur.fetchone()
	cur.close()
	if not info:
		return None
	else:
		return info

def getStudent(db,zid):
	cur = db.cursor()
	qry = """
	select * from people where people.id = %s
	"""
	cur.execute(qry,[zid])
	info = cur.fetchone()
	cur.close()
	if not info:
		return None
	else:
		return info

# ================ Q1 ==================
def getTranscriptInfo(db, zid):
	cursor = db.cursor()
	query = """
	select
		subjects.code as subject,
		terms.code as term,
		subjects.name as title,
		course_enrolments.mark,
		course_enrolments.grade,
		subjects.uoc
	from course_enrolments
	join courses on (course_enrolments.course = courses.id)
	join subjects on (courses.subject = subjects.id)
	join terms on (courses.term = terms.id)
	where course_enrolments.student = %s
	order by terms.code, subjects.code;
	"""
	cursor.execute(query,[zid])
	results = cursor.fetchall()
	cursor.close()
	if not results:
		return None
	else:
		return results