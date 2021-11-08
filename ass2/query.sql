-- Q1
-- select
--     subjects.code as subject,
--     terms.code as term,
--     subjects.name as title,
--     course_enrolments.mark,
--     course_enrolments.grade,
--     subjects.uoc
-- from course_enrolments
-- join courses on (course_enrolments.course = courses.id)
-- join subjects on (courses.subject = subjects.id)
-- join terms on (courses.term = terms.id)
-- where course_enrolments.student = '5143550'
-- order by terms.code, subjects.code;

-- Q2
-- select
--     programs.code as program,
--     orgunits.longname as offeredby,
--     rules.name as rule_name,
--     aog.definition as course_requirements
-- from program_rules pr
-- join programs on (pr.program = programs.id)
-- join orgunits on (programs.offeredby = orgunits.id)
-- join rules on (pr.rule = rules.id)
-- join academic_object_groups aog on (rules.ao_group = aog.id)
-- where programs.code = '3778';

-- Q1
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
where course_enrolments.student = '5143550'
order by terms.code, subjects.code;