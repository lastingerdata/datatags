from root.flask.data_lake.libs.swagger_docs import swagger_dict
from root.snowflake.libs import surveys_column_desc

surveys_description = swagger_dict["surveys"]["description"]

dataset_list = [
    ### SURVEYS (PROGRAM): ACADEMIC YEAR 2025-26 ###
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_advanced_cop_facilitator_training_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Advanced CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_cda_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "TableName": "surveys_coaching_calibrations_AY25_26",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "TableName": "surveys_coaching_certification_AY25_26",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Certification"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "TableName": "surveys_community_of_practice_AY25_26",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Community of Practice"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "TableName": "surveys_cop_calibrations_AY25_26",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"CoP Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "TableName": "surveys_elementary_micro_AY25_26",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "TableName": "surveys_emergent_AY25_26",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "TableName": "surveys_fta_AY25_26",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Florida Tutoring Advantage"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "TableName": "surveys_initial_cop_facilitator_training_AY25_26",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Initial CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "TableName": "surveys_leadership_AY25_26",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Leadership"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_literacy_coach_endorsement_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_literacy_matrix_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_math_matrix_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Math Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "TableName": "surveys_online_course_AY25_26",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_secondary_micro_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
    ### SURVEYS (OKR): ACADEMIC YEAR 2025-26 ###
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_okr_coaching_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Coaching"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_okr_early_childhood_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Early Childhood"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_okr_literacy_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Literacy"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_okr_math_matrix_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Math Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'surveys',
        "Description": surveys_description,
        "TableName": "surveys_okr_new_worlds_reading_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in surveys_column_desc.surveys_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"OKR","tag_value":"New Worlds Reading"}]""",
        },        
    },
]