from root.flask.data_lake.libs.swagger_docs import swagger_dict
from root.snowflake.libs import grades_column_desc

grades_description = swagger_dict["grades"]["description"]

dataset_list = [
    
    ### GRADES (PROGRAM): ACADEMIC YEAR 2026-27 ###
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_cda_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_elementary_micro_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_emergent_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_fta_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Florida Tutoring Advantage"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_literacy_coach_endorsement_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_literacy_matrix_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_math_matrix_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Math Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_online_course_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "TableName": "grades_secondary_micro_AY26_27",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
    
    ### GRADES (OKR): ACADEMIC YEAR 2025-26 ###
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_okr_coaching_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Coaching"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_okr_early_childhood_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Early Childhood"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_okr_literacy_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Literacy"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_okr_math_matrix_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Math Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'grades',
        "Description": grades_description,
        "TableName": "grades_okr_new_worlds_reading_AY26_27",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in grades_column_desc.grades_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2026-27",
            "tagSections": """[{"tag_name":"OKR","tag_value":"New Worlds Reading"}]""",
        },        
    },
]