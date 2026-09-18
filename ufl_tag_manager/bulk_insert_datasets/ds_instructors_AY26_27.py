from root.flask.data_lake.libs.swagger_docs import swagger_dict
from root.snowflake.libs import instructors_column_desc

instructors_description = swagger_dict["instructors"]["description"]

dataset_list = [
    
    ### INSTRUCTORS: ACADEMIC YEAR 2026-27 ###
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_CDA_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_elementary_micro_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_emergent_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_fta_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Florida Tutoring Advantage"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_literacy_coach_endorsement_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_literacy_matrix_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_math_matrix_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Math Micro-Credential"}]""",
        },        
    },
        {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_online_course_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_secondary_micro_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
]