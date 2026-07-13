from root.snowflake.libs import assignments_column_desc
from root.flask.data_lake.libs.swagger_docs import swagger_dict

assignments_description = swagger_dict["assignments"]["description"]

dataset_list = [
    ### ASSIGNMENTS: ACADEMIC YEAR 2025-26 ###
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_advanced_cop_facilitator_training_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Advanced CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_cda_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_coaching_calibrations_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_coaching_certification_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Certification"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_community_of_practice_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Community of Practice"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_cop_calibrations_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"CoP Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_elementary_micro_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_emergent_micro_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_fta_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Florida Tutoring Advantage"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_initial_cop_facilitator_training_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Initial CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_leadership_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Leadership"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_literacy_coach_endorsement_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_literacy_matrix_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_math_matrix_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Math Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_online_course_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_secondary_micro_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assignments',
        "Description": assignments_description,
        "TableName": "assignments_technical_assistance_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assignments_column_desc.assignments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Technical Assistance"}]""",
        },        
    },
]