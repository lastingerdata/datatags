from root.snowflake.libs import assignments_column_desc
from root.flask.data_lake.libs.swagger_docs import swagger_dict

assignments_description = swagger_dict["assignments"]["description"]

dataset_list = [
    
    ### ASSIGNMENTS: ACADEMIC YEAR 2026-27 ###
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_cda_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_elementary_micro_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_emergent_micro_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_fta_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Florida Tutoring Advantage"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_literacy_coach_endorsement_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_literacy_matrix_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_math_matrix_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Math Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_online_course_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_secondary_micro_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
]