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
# ======== Program part
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
	where programs.code = %s
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

# ======== Stream part
def getBasicStreamInfo(db, streamcode):
	cursor = db.cursor()
	query = """
	select
		streams.code as code,
		streams.name as name,
		orgunits.longname as offeredby
	from streams
	join orgunits on (streams.offeredby = orgunits.id)
	where streams.code = %s;
	"""
	cursor.execute(query,[streamcode])
	results = cursor.fetchone()
	cursor.close()
	if not results:
		return None
	else:
		return results

def getDetailStreamInfo(db, streamcode):
	cursor = db.cursor()
	query = """
	select
		rules.name as name,
		rules.type as type,
		rules.min_req as min_req,
		rules.max_req as max_req,
		aog.definition as course_requirements
	from rules
	join stream_rules on (stream_rules.rule = rules.id)
	join streams on (streams.id = stream_rules.stream)
	join academic_object_groups aog on (rules.ao_group = aog.id)
	where streams.code = %s;
	"""
	cursor.execute(query,[streamcode])
	results = cursor.fetchall()
	cursor.close()
	if not results:
		return None
	else:
		return results

# ================ Q3 ==================
def getProgramStreamTableByZid(db, zid):
	cursor = db.cursor()
	query = """
	select
		program_enrolments.student,
		programs.code as program,
		streams.code as stream,
		terms.code as term,
		streams.name as stream_name,
		programs.name as program_name
	from program_enrolments
	join programs on (program_enrolments.program = programs.id)
	join stream_enrolments on (stream_enrolments.partof = program_enrolments.id)
	join streams on (stream_enrolments.stream = streams.id)
	join terms on (program_enrolments.term = terms.id)
	where program_enrolments.student = %s
	order by terms.code;
	"""
	cursor.execute(query,[zid])
	results = cursor.fetchall()
	cursor.close()
	if not results:
		return None
	else:
		return results

def getNameByZid(db, zid):
	cursor = db.cursor()
	query = """
	select
		people.id,
		people.family,
		people.given
	from people
	where people.id = %s
	"""
	cursor.execute(query,[zid])
	result = cursor.fetchone()
	cursor.close()
	if not result:
		return None
	else:
		return result

def getCompletedSubjects(db, zid):
	return getTranscriptInfo(db, zid)

def getStreamRules(db, streamcode):
	cursor = db.cursor()
	query = """
	select
		rules.name as rule_name,
		rules.type as rule_type,
		rules.min_req as min_req,
		rules.max_req as max_req,
		academic_object_groups.definition as requirements
	from stream_rules
	join streams on (stream_rules.stream = streams.id)
	join rules on (stream_rules.rule = rules.id)
	join academic_object_groups on (academic_object_groups.id = rules.ao_group)
	where streams.code = %s;
	"""
	cursor.execute(query,[streamcode])
	results = cursor.fetchall()
	cursor.close()
	if not results:
		return None
	else:
		return results

def getProgramRules(db, programcode):
	cursor = db.cursor()
	query = """
	select
		rules.name as rule_name,
		rules.type as rule_type,
		rules.min_req as min_req,
		rules.max_req as max_req,
		academic_object_groups.definition as requirements
	from program_rules
	join programs on (programs.id = program_rules.program)
	join rules on (rules.id = program_rules.rule)
	join academic_object_groups on (academic_object_groups.id = rules.ao_group)
	where programs.code = %s;
	"""
	cursor.execute(query,[programcode])
	results = cursor.fetchall()
	cursor.close()
	if not results:
		return None
	else:
		return results









# ================ print functions ==================
# ======== Program part
def PrintBasicProgramInfo(info):
	[id, name, uoc, duration, offeredby] = info
	print(f"{id} {name}, {uoc} UOC, {duration / 12:.1f} years")
	print(f"- offered by {offeredby}")

# ======== Stream part
def PrintBasicStreamInfo(info):
	[streamcode, name, offeredby] = info
	print(f"{streamcode} {name}")
	print(f"- offered by {offeredby}")

def PrintDS(db, name, min_req, max_req, streams):
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

def PrintCC(db, name, min_req, max_req, subjects):
	subject_list = subjects.split(",")
	if len(subject_list) == 1:
		print(f"{name}")
	elif min_req == max_req:
		print(f"all courses from {name}")
	else:
		print(f"between {min_req} and {max_req} UOC courses from {name}")

	for subject in subject_list:
		subject = subject.replace('{', '["')
		subject = subject.replace('}', '"]')
		subject = subject.replace(';', '","')
		if '[' in subject and ']' in subject:
			subject = eval(subject)

		if type(subject) != list:
			subject_info = getSubjectNameByCode(db, subject)
			if subject_info == None:
				subject_name = "???"
			else:
				subject_name = subject_info[1]
			print(f"- {subject} {subject_name}")
		else:
			for i in range(len(subject)):
				subject_info = getSubjectNameByCode(db, subject[i])
				if i == 1:
					print(f"  or {subject[i]} {subject_info[1]}")
				else:
					print(f"- {subject[i]} {subject_info[1]}")
	return

def PrintGE(UOC):
	print(f"{UOC} UOC of General Education")
	return

def PrintPE(db, name, min_req, max_req, subjects):
	subject_list = subjects.split(",")
	if min_req != None and max_req != None:
		if min_req == max_req:
			print(f"{min_req} UOC courses from {name}")
		elif min_req < max_req:
			print(f"between {min_req} and {max_req} UOC courses from {name}")
	elif min_req == None:
		print(f"up to {max_req} UOC courses from {name}")
	elif max_req == None:
		print(f"at least {min_req} UOC courses from {name}")
	

	if min_req != None and max_req != None:
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
	else:
		print(f"- courses matching {subjects}")
	return

def PrintFE(db, name, min_req, max_req, subjects):
	if min_req == None:
		print(f"up to {min_req} UOC courses from {name}")
	elif max_req == None:
		if "Free Electives" not in name:
			print(f"at least {min_req} UOC of {name}")
		else:
			print(f"at least {min_req} UOC of Free Electives")