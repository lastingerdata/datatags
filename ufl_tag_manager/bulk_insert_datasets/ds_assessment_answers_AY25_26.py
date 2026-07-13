from root.snowflake.libs import assessment_answers_column_desc
from root.flask.data_lake.libs.swagger_docs import swagger_dict

assessment_answers_description = swagger_dict["assessment_answers"]["description"]


dataset_list = [
    ### ASSESSMENT ANSWERS: ACADEMIC YEAR 2025-26 ###
    
    # {
    #     "EndPoint": 'assessment_answers',
    #     "Description": assessment_answers_description,
    #     "TableName": "assessment_answers_advanced_cop_facilitator_training_AY25_26",
    #     "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
    #     "headers": {
    #         "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
    #         "Segment": "Academic Year 2025-26",
    #         "tagSections": """[{"tag_name":"Program","tag_value":"Advanced CoP Facilitator Training"}]""",
    #     },        
    # },
    # {
    #     "EndPoint": 'assessment_answers',
    #     "Description": assessment_answers_description,
    #     "TableName": "assessment_answers_cda_AY25_26",
    #     "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
    #     "headers": {
    #         "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
    #         "Segment": "Academic Year 2025-26",
    #         "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
    #     },        
    # },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_coaching_calibrations_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_coaching_certification_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Certification"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_community_of_practice_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Community of Practice"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_cop_calibrations_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"CoP Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_elementary_micro_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_emergent_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_fta_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Florida Tutoring Advantage"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_initial_cop_facilitator_training_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Initial CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_leadership_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Leadership"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_literacy_coach_endorsement_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_literacy_matrix_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_math_matrix_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Math Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_online_course_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_secondary_micro_AY25_26",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2025-26",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    }]