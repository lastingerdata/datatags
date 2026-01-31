#!/usr/bin/env python3
try:
    import json, os, sys, pandas
    from snowflake.connector.pandas_tools import write_pandas 
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    libs_path = os.path.join(current_dir, "libs")
    sys.path.append(libs_path)
    import snowflake_libs
    
    schema = 'FINAL'
    table = 'DEMO'
    snowflake_params = {
        'user':'UF_SVC_LASTINGER_WEB',
        'account':'ufl-datahub',
        'private_key':snowflake_libs.get_pkb(),
        'database':'PUB_LAKE_LASTINGER',
        'schema':schema
    }    
    
    import snowflake.connector,lake_lastinger_db_connect
    snowflake_connection = snowflake.connector.connect(**snowflake_params)      
    db_connection = lake_lastinger_db_connect.LocalDBConnection().connect()
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute(
        """
SELECT genius_enrollments.*,
       genius_departments.NAME AS departmentName,
       genius_terms.NAME       AS termName

FROM   genius_enrollments
    
       LEFT JOIN genius_courses
              ON genius_enrollments.courseid = genius_courses.courseid
       LEFT JOIN genius_departments
              ON genius_courses.departmentid = genius_departments.departmentid
       LEFT JOIN genius_courses_sections
              ON genius_enrollments.sectionid =genius_courses_sections.sectionid
       LEFT JOIN genius_terms
              ON genius_courses_sections.termid = genius_terms.termid
       LEFT JOIN brightspace_users
              ON brightspace_users.username = genius_enrollments.username
       LEFT JOIN ufl_section_tags
              ON genius_sectionid = genius_enrollments.sectionid
       LEFT JOIN ufl_tag_values
              ON ufl_section_tags.tag_entry_id = ufl_tag_values.tag_entry_id
       LEFT JOIN ufl_tags
              ON ufl_tag_values.tag_id = ufl_tags.tag_id

WHERE  ufl_section_tags.tag_entry_id = 80;      
            """
        )
    
    
    records = cursor.fetchall()
    this_dataframe = pandas.DataFrame(records)

    create_table_sql = snowflake_libs.get_create_table(this_dataframe, table, schema)

    with snowflake_connection.cursor() as cs:
        cs.execute(f"DROP TABLE IF EXISTS {table}")
        cs.execute(create_table_sql)

    success, nchunks, nrows, _ = write_pandas(
        conn=snowflake_connection, 
        df=snowflake_libs.prep_dataframe(this_dataframe), 
        table_name=table,
        schema=schema
    )
     
    print("Content-Type: application/json"); print()
    print(json.dumps({
        "status": "success",
        "message": f"Table Rebuilt, {len(records)} records"
    }))
except Exception as e: print(f"Content-Type: text/html\n\n{e}<hr>{type(e).__name__}")    
