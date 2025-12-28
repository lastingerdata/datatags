#!/usr/bin/env python3
import os
import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Navigate up to the templates directory
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATES = ROOT

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html", "xml"])
)

# Sample data matching the first screenshot
course_data = [
    {
        'id': 1,
        'genius_section_id': '4884',
        'd2l_org_unit_id': '16314',
        'section_name': 'Advanced CoP Cohort 6 Winter 2026',
        'course_start_date': '2025-11-03',
        'course_end_date': '2026-06-30',
        'course_name': 'Advanced Communities of Practice (25-26)',
        'department_name': 'FEL Communities of Practice',
        'term': '222',
        'tag_status': ''
    },
    {
        'id': 2,
        'genius_section_id': '4884',
        'd2l_org_unit_id': '16314',
        'section_name': 'Advanced CoP Cohort 6 Winter 2026',
        'course_start_date': '2025-11-03',
        'course_end_date': '2026-06-30',
        'course_name': 'Advanced Communities of Practice (25-26)',
        'department_name': 'FEL Communities of Practice',
        'term': '222',
        'tag_status': 'Segment: Academic Year 2025-26'
    },
    {
        'id': 3,
        'genius_section_id': '4884',
        'd2l_org_unit_id': '16314',
        'section_name': 'Short Section Name',
        'course_start_date': '2025-11-03',
        'course_end_date': '2026-06-30',
        'course_name': 'Short Course Name',
        'department_name': 'Dept Name',
        'term': '222',
        'tag_status': 'OKR: Early Learning'
    },
    {
        'id': 4,
        'genius_section_id': '4884',
        'd2l_org_unit_id': '16314',
        'section_name': 'Advanced CoP Cohort 6 Winter 2026',
        'course_start_date': '2025-11-03',
        'course_end_date': '2026-06-30',
        'course_name': 'Advanced Communities of Practice (25-26)',
        'department_name': 'FEL Communities of Practice',
        'term': '222',
        'tag_status': '-'
    },
    {
        'id': 5,
        'genius_section_id': '4884',
        'd2l_org_unit_id': '16314',
        'section_name': 'Advanced CoP Cohort 6 Winter 2026',
        'course_start_date': '2025-11-03',
        'course_end_date': '2026-06-30',
        'course_name': 'Advanced Communities of Practice (25-26)',
        'department_name': 'FEL Communities of Practice',
        'term': '222',
        'tag_status': 'Segment: Academic Year 2025-26'
    },
]

def main():
    html = env.get_template("components/table/table_demo.html").render(
        course_data=course_data
    )
    
    print("Content-Type: text/html; charset=utf-8")
    print()
    print(html)

if __name__ == "__main__":
    main()
