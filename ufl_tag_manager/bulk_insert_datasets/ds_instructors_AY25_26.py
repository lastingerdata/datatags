from root.snowflake.libs import instructors_column_desc
from root.flask.data_lake.libs.swagger_docs import swagger_dict

instructors_description = swagger_dict["instructors"]["description"]

dataset_list = [
    ### INSTRUCTORS: ACADEMIC YEAR 2025-26 ###
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_advanced_cop_facilitator_training_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Advanced CoP Facilitator Training"}]""",
        },        
    }, 
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_cda_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
        },        
    }, 
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_coaching_calibrations_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Calibrations"}]""",
        },        
    }, 
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_coaching_certification_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Certification"}]""",
        },        
    }, 
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_community_of_practice_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Community of Practice"}]""",
        },        
    }, 
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_cop_calibrations_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"CoP Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_elementary_micro_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_emergent_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_fta_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Florida Tutoring Advantage"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_initial_cop_facilitator_training_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Initial CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_leadership_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Leadership"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_literacy_coach_endorsement_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_literacy_matrix_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_math_matrix_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Math Micro-Credential"}]""",
        },        
    },
        {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_online_course_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'instructors',
        "Description": instructors_description,
        "TableName": "instructors_secondary_micro_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in instructors_column_desc.instructors_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
]