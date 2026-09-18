from root.flask.data_lake.libs.swagger_docs import swagger_dict
from root.snowflake.libs import course_access_column_desc

course_access_description = swagger_dict["course_access"]["description"]

dataset_list = [
    
    ### COURSE ACCESS: ACADEMIC YEAR 2026-27 ###
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_cda_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_elementary_micro_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_emergent_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_literacy_coach_endorsement_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_literacy_matrix_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_math_matrix_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Math Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_online_course_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_secondary_micro_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
]