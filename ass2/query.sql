create or replace view Table01
as
select
    rules.name as rule_name,
    aog.definition as rule_content
from rules
join stream_rules on (stream_rules.rule = rules.id)
join streams on (streams.id = stream_rules.stream)
join academic_object_groups aog on (rules.ao_group = aog.id)
where streams.code = 'SENGAH';

create or replace view Table02
as
select
    subjects.code as subject_code,
    terms.code as term,
    subjects.name as subject_name,
    course_enrolments.mark as mark,
    course_enrolments.grade as grade,
    subjects.uoc as uoc
from people
join course_enrolments on (course_enrolments.student = people.id)
join courses on (course_enrolments.course = courses.id)
join terms on (courses.term = terms.id)
join subjects on (subjects.id = courses.subject)
where people.id = '5198386'
order by terms.code, subjects.code;

drop view Table01;
drop view Table02;

create view Table03
as
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
where streams.code = 'COMPBH';

drop view Table03;

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
where programs.code = '3707';



-- Lizi教育
-- =========================Q3=======================
-- select
--     pe.student,
--     programs.code as program,
--     streams.code as stream,
--     terms.code as term,
--     streams.name as stream_name,
--     programs.name as program_name
-- from program_enrolments pe
-- join programs on (pe.program = programs.id)
-- join stream_enrolments se on (se.partof = pe.id)
-- join streams on (se.stream = streams.id)
-- join terms on (pe.term = terms.id)
-- where pe.student = '5197273'
-- order by terms.code;

-- select 
--     program_rules.program as program_id,
--     rules.name as rule_name,
--     rules.type as rule_type,
--     rules.min_req,
--     rules.max_req,
--     aog.type as aog_type,
--     aog.defby,
--     aog.definition
--     -- 0 as uoc_satisfied, -- 储存有多少uoc已被满足，初始值是0,
--     -- '' as course_satisfied -- 储存有什么课已被满足，初始值是'', 
-- from program_rules 
-- join rules on (program_rules.rule = rules.id)
-- join academic_object_groups aog on (rules.ao_group = aog.id)
-- where program_rules.program = '3707';