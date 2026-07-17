from root.flask.data_lake.libs.swagger_docs import swagger_dict
from root.snowflake.libs import sections_column_desc

sections_description = swagger_dict["sections"]["description"]

dataset_list = [
    ### SECTIONS (PROGRAM): ALL ACADEMIC YEARS ###
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_advanced_cop_facilitator_training_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Advanced CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_ccrr_asset_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"CCR&R Asset"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_cda_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_coaching_calibrations_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_coaching_certification_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Certification"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_coaching_recertification_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Recertification"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_community_of_practice_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Community of Practice"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_cop_calibrations_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"CoP Calibrations"}]""",
        },        
    },
    # {
    #     "EndPoint": 'sections',
    #     "Description": sections_description,
    #     "TableName": "sections_elementary_micro_all",
    #     "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
    #     "headers": {
    #         "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
    #         "Segment": "all",
    #         "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
    #     },        
    # },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_emergent_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
     {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_fta_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Florida Tutoring Advantage"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_initial_cop_facilitator_training_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Initial CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_leadership_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Leadership"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_literacy_coach_endorsement_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_literacy_matrix_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_ma_training_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"MA Training"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_math_matrix_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Math Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_online_course_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_secondary_micro_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_technical_assistance_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Technical Assistance"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_webinar_all",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Webinar"}]""",
        },        
    },
    ### SECTIONS (OKR): ALL ACADEMIC YEARS ###
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_okr_coaching",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Coaching"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_okr_early_childhood",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Early Childhood"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_okr_literacy",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Literacy"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_okr_math_matrix",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Math Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'sections',
        "Description": sections_description,
        "TableName": "sections_okr_new_worlds_reading",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in sections_column_desc.sections_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"OKR","tag_value":"New Worlds Reading"}]""",
        },        
    },
]