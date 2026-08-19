from root.snowflake.libs import assessment_answers_column_desc
from root.flask.data_lake.libs.swagger_docs import swagger_dict

assessment_answers_description = swagger_dict["assessment_answers"]["description"]


dataset_list = [
    ### ASSESSMENT ANSWERS: ACADEMIC YEAR 2024-25 ###
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_elementary_micro_AY24_25",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2024-25",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_emergent_AY24_25",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2024-25",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_literacy_coach_endorsement_AY24_25",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2024-25",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_literacy_matrix_AY24_25",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2024-25",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_secondary_micro_AY24_25",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2024-25",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
    ### ASSESSMENT ANSWERS: ACADEMIC YEAR 2023-24 ###
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_elementary_micro_AY23_24",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2023-24",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_emergent_AY23_24",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2023-24",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_literacy_coach_endorsement_AY23_24",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2023-24",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_literacy_matrix_AY23_24",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2023-24",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_secondary_micro_AY23_24",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2023-24",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
    ### ASSESSMENT ANSWERS: ACADEMIC YEAR 2022-23 ###
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_elementary_micro_AY22_23",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2022-23",
            "tagSections": """[{"tag_name":"Program","tag_value":"Elementary Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_emergent_AY22_23",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2022-23",
            "tagSections": """[{"tag_name":"Program","tag_value":"Emergent Micro-Credential"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_literacy_coach_endorsement_AY22_23",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2022-23",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Coach Endorsement"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_literacy_matrix_AY22_23",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2022-23",
            "tagSections": """[{"tag_name":"Program","tag_value":"Literacy Matrix"}]""",
        },        
    },
    {
        "EndPoint": 'assessment_answers',
        "Description": assessment_answers_description,
        "TableName": "assessment_answers_secondary_micro_AY22_23",
        "column_description": {col_name: col_data.get("description", "") for col_name, col_data in assessment_answers_column_desc.assessment_answers_columns.items()},
        "headers": {
            "ApiKey": '596fa395d7a9072c06207b119ec415164487d50a37f904d08542305466a80fce', 
            "Segment": "Academic Year 2022-23",
            "tagSections": """[{"tag_name":"Program","tag_value":"Secondary Micro-Credential"}]""",
        },        
    },
]