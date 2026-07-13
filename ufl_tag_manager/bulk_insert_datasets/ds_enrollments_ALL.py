from root.snowflake.libs import enrollments_column_desc
from root.flask.data_lake.libs.swagger_docs import swagger_dict

enrollments_description = swagger_dict["enrollments"]["description"]

dataset_list = [
    ### ENROLLMENTS: ALL ACADEMIC YEARS ###   
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_advanced_cop_facilitator_training",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Advanced CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_ccrr_asset",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"CCR&R Asset"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_cda",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"CDA"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_coaching_calibrations",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_coaching_certification",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Certification"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_coaching_recertification",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Coaching Recertification"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_community_of_practice",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Community of Practice"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_cop_calibrations",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"CoP Calibrations"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_elementary_micro",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    # {
    #     "EndPoint": 'enrollments',
    #    "Description": enrollments_description,
    #     "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
    #     "TableName": "enrollments_emergent",
    #     "headers": {
    #         "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
    #         "Segment": "all",
    #         "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
    #     },        
    # },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_fta",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Florida Tutoring Advantage"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_initial_cop_facilitator_training",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Initial CoP Facilitator Training"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_leadership",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Leadership"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_literacy_coach_endorsement",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_literacy_matrix",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_literacy_small_group",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Small Group Instruction"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_ma_training",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"MA Training"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_math_matrix",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Math Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_nwri_teacher_pl",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"NWRI Teacher Professional Learning"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_online_course",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Online Course"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_secondary_micro",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_technical_assistance",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Technical Assistance"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "TableName": "enrollments_webinar",
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"Program","tag_value":"Webinar"}]""",
        },        
    },
    ### ENROLLMENTS (OKR): ALL ACADEMIC YEARS ###
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "TableName": "enrollments_okr_early_learning",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Early Learning"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "TableName": "enrollments_okr_coaching",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Coaching"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "TableName": "enrollments_okr_literacy",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Literacy"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "TableName": "enrollments_okr_math_matrix",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"OKR","tag_value":"Math Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'enrollments',
        "Description": enrollments_description,
        "TableName": "enrollments_okr_new_worlds_reading",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in enrollments_column_desc.enrollments_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "all",
            "tagSections": """[{"tag_name":"OKR","tag_value":"New Worlds Reading"}]""",
        },        
    },
]