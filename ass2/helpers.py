# COMP3311 21T3 Ass2 ... Python helper functions
# add here any functions to share between Python scripts 
# you must submit this even if you add nothing

import re

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

# ================ Q2 ==================
def getBasicProgramInfo(db, programcode):
	cursor = db.cursor()
	query = """
	select
		programs.code as program,
		programs.name as name,
		programs.uoc as uoc,
		programs.duration as duration,
		orgunits.longname as offeredby
	from programs
	join orgunits on (programs.offeredby = orgunits.id)
	where programs.code = %s;
	"""
	cursor.execute(query,[programcode])
	results = cursor.fetchone()
	cursor.close()
	if not results:
		return None
	else:
		return results

def getDetailProgramInfo(db, programcode):
	cursor = db.cursor()
	query = """
	select
		rules.name as name,
		rules.type as type,
		rules.min_req as min_req,
		rules.max_req as max_req,
		academic_object_groups.definition as courses
	from rules
	join program_rules on (program_rules.rule = rules.id)
	join programs on (programs.id = program_rules.program)
	join academic_object_groups on (rules.ao_group = academic_object_groups.id)
	where programs.id = %s;
	"""
	cursor.execute(query,[programcode])
	results = cursor.fetchall()
	cursor.close()
	if not results:
		return None
	else:
		return results

def getStreamNameByCode(db, streamcode):
	cursor = db.cursor()
	query = """
	select
		streams.code,
		streams.name
	from streams
	where streams.code = %s;
	"""
	cursor.execute(query,[streamcode])
	results = cursor.fetchone()
	cursor.close()
	if not results:
		return None
	else:
		return results

def getSubjectNameByCode(db, subjectcode):
	cursor = db.cursor()
	query = """
	select
		subjects.code,
		subjects.name
	from subjects
	where subjects.code = %s;
	"""
	cursor.execute(query,[subjectcode])
	results = cursor.fetchone()
	cursor.close()
	if not results:
		return None
	else:
		return results

# ================ print functions ==================
def PrintBasicProgramInfo(info):
	[id, name, uoc, duration, offeredby] = info
	print(f"{id} {name}, {uoc} UOC, {duration / 12:.1f} years")
	print(f"- offered by {offeredby}")

def PrintDS(db, min_req, max_req, name, streams):
	print(f"{min_req} stream(s) from {name}")
	stream_list = streams.split(",")
	for stream_code in stream_list:
		stream_info = getStreamNameByCode(db, stream_code)
		if stream_info == None:
			stream_name = "???"
		else:
			stream_name = stream_info[1]
		print(f"- {stream_code} {stream_name}")
	return

def PrintCC(db, min_req, max_req, name, subjects):
	subject_list = subjects.split(",")
	if len(subject_list) == 1:
		print(f"{name}")
	elif min_req == max_req:
		print(f"all courses from {name}")
	else:
		print(f"between {min_req} and {max_req} UOC courses from {name}")

	for subject in subject_list:
		if len(subject) == 8:
			subject_info = getSubjectNameByCode(db, subject)
			if subject_info == None:
				subject_name = "???"
			else:
				subject_name = subject_info[1]
			print(f"- {subject} {subject_name}")
		else:
			alter_list = re.split("{|;|}", subject)
			alter_list = list(filter(None, alter_list))

			for i in range(len(alter_list)):
				subject_info = getSubjectNameByCode(db, alter_list[i])
				if i == 1:
					print(f"  or {alter_list[i]} {subject_info[1]}")
				else:
					print(f"- {alter_list[i]} {subject_info[1]}")
	return

def PrintGE(UOC):
	print(f"{UOC} UOC of General Education")
	return