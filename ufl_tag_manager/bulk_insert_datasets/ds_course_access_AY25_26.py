from root.snowflake.libs import course_access_column_desc
from root.flask.data_lake.libs.swagger_docs import swagger_dict

course_access_description = swagger_dict["course_access"]["description"]

dataset_list = [
    ### COURSE ACCESS: ACADEMIC YEAR 2025-26 ###
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_advanced_cop_facilitator_training_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Advanced CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_cda_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_coaching_calibrations_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_coaching_certification_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Certification"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_community_of_practice_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Community of Practice"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_cop_calibrations_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"CoP Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_elementary_micro_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_emergent_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_initial_cop_facilitator_training_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Initial CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_leadership_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Leadership"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_literacy_coach_endorsement_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_literacy_matrix_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_online_course_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'course_access',
        "Description": course_access_description,
        "TableName": "course_access_secondary_micro_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in course_access_column_desc.course_access_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
]