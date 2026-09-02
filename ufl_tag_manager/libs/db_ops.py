from libs import taggingMySQLDB_connection as localMySQLDB_connection
import datetime


def log_action(username, action_type, details):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        ts = datetime.datetime.utcnow().isoformat()
        cursor.execute(
            """
            INSERT INTO tag_action_logs (username, action_type, details, timestamp)
            VALUES (%s, %s, %s, %s)
            """,
            (username, action_type, details, ts),
        )
        db.commit()
    finally:
        cursor.close()
        db.close()


def get_non_segmentation_tags():
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM ufl_tags")
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()


def add_tag(tag_name, description):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO ufl_tags (tag_name, description) VALUES (%s, %s)",
            (tag_name, description),
        )
        db.commit()
    finally:
        cursor.close()
        db.close()


def can_delete_tag(tag_id):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT COUNT(*) AS cnt FROM ufl_tag_values WHERE tag_id = %s",
            (tag_id,),
        )
        return int(cursor.fetchone()["cnt"]) == 0
    finally:
        cursor.close()
        db.close()


def delete_tag(tag_id):
    if not can_delete_tag(tag_id):
        return False
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM ufl_tags WHERE tag_id = %s", (tag_id,))
        db.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        db.close()


def get_tag_values(tag_id):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM ufl_tag_values WHERE tag_id = %s", (tag_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()


def add_tag_value(tag_id, tag_value, description):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO ufl_tag_values (tag_id, tag_value, description)
            VALUES (%s, %s, %s)
            """,
            (tag_id, tag_value, description),
        )
        db.commit()
    finally:
        cursor.close()
        db.close()


def can_delete_tag_value(tag_entry_id):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT COUNT(*) AS cnt FROM ufl_section_tags WHERE tag_entry_id = %s",
            (tag_entry_id,),
        )
        return int(cursor.fetchone()["cnt"]) == 0
    finally:
        cursor.close()
        db.close()


def delete_tag_value(tag_entry_id):
    if not can_delete_tag_value(tag_entry_id):
        return False
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM ufl_tag_values WHERE tag_entry_id = %s", (tag_entry_id,))
        db.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        db.close()


def update_tag_value(tag_entry_id, updated_value, updated_description):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            UPDATE ufl_tag_values
            SET tag_value = %s, description = %s
            WHERE tag_entry_id = %s
            """,
            (updated_value, updated_description, tag_entry_id),
        )
        db.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        db.close()


def get_all_tag_values():
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT v.tag_entry_id, v.tag_value, t.tag_name
            FROM ufl_tag_values v
            JOIN ufl_tags t ON v.tag_id = t.tag_id
            """
        )
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()

def get_section_tag_mappings(
    name,
    d2l_OrgUnitId,
    genius_sectionId,
    tag_name,
    tag_value,
    wild_card=None,
    sort_col="",
    sort_dir="asc",
):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)

    SORT_MAP = {
        "genius_sectionId": "s.genius_sectionId",
        "d2l_OrgUnitId": "s.d2l_OrgUnitId",
        "section_name": "cs.Section_Name",
        "tag_name": "t.tag_name",
        "tag_value": "v.tag_value",
    }

    query = """
        SELECT
            s.d2l_OrgUnitId,
            s.genius_sectionId,
            s.tag_entry_id,
            cs.Section_Name as section_name,
            v.tag_id,
            v.tag_value,
            t.tag_name
        FROM ufl_section_tags s
        LEFT JOIN (
            SELECT
                CASE
                    WHEN salesforce_courseoffering.GENIUS_LEGACY_ID__C REGEXP '^[0-9]+\\.0$'
                    THEN SUBSTRING_INDEX(salesforce_courseoffering.GENIUS_LEGACY_ID__C, '.', 1)
                    ELSE salesforce_courseoffering.GENIUS_LEGACY_ID__C
                END AS SIS_SectionCode,
                CAST(salesforce_courseoffering.BRIGHTSPACE_ID__C AS UNSIGNED) AS D2L_OrgUnitId,
                salesforce_courseoffering.NAME AS Section_Name
            FROM salesforce_courseoffering
            WHERE salesforce_courseoffering.GENIUS_LEGACY_ID__C IS NOT NULL

            UNION ALL

            SELECT
                CASE
                    WHEN salesforce_section__c.COURSE_CODE__C REGEXP '^[0-9]+\\.0$'
                    THEN SUBSTRING_INDEX(salesforce_section__c.COURSE_CODE__C, '.', 1)
                    ELSE salesforce_section__c.COURSE_CODE__C
                END AS SIS_SectionCode,
                CAST(salesforce_courseoffering.BRIGHTSPACE_ID__C AS UNSIGNED) AS D2L_OrgUnitId,
                salesforce_section__c.NAME AS Section_Name
            FROM salesforce_courseoffering
                LEFT JOIN salesforce_section__c ON COURSE_OFFERING__C = salesforce_courseoffering.ID
            WHERE salesforce_courseoffering.GENIUS_LEGACY_ID__C IS NULL
              AND salesforce_section__c.ID IS NOT NULL
        ) AS cs
            ON (cs.D2L_OrgUnitId = s.d2l_OrgUnitId
                OR (cs.D2L_OrgUnitId IS NULL AND s.d2l_OrgUnitId IS NULL))
            AND cs.SIS_SectionCode = s.genius_sectionId
        JOIN ufl_tag_values v ON s.tag_entry_id = v.tag_entry_id
        JOIN ufl_tags t ON v.tag_id = t.tag_id
        WHERE 1 = 1
    """

    params = []

    try:
        if name:
            nl = name.lower()
            if wild_card == "exact_match":
                query += " AND LOWER(cs.Section_Name) = %s"
                params.append(nl)
            elif wild_card == "contains":
                query += " AND LOWER(cs.Section_Name) LIKE %s"
                params.append(f"%{nl}%")
            elif wild_card == "does_not_contain":
                query += " AND LOWER(cs.Section_Name) NOT LIKE %s"
                params.append(f"%{nl}%")
            elif wild_card == "ends_with":
                query += " AND LOWER(cs.Section_Name) LIKE %s"
                params.append(f"%{nl}")
            elif wild_card == "begins_with":
                query += " AND LOWER(cs.Section_Name) LIKE %s"
                params.append(f"{nl}%")
            else:
                query += " AND LOWER(cs.Section_Name) LIKE %s"
                params.append(f"%{nl}%")

        if d2l_OrgUnitId:
            query += " AND s.d2l_OrgUnitId = %s"
            params.append(d2l_OrgUnitId)

        if genius_sectionId:
            query += " AND s.genius_sectionId = %s"
            params.append(genius_sectionId)

        if tag_name:
            query += " AND t.tag_name = %s"
            params.append(tag_name)

        if tag_value:
            query += " AND v.tag_value = %s"
            params.append(tag_value)

        sort_dir = (sort_dir or "asc").lower()
        if sort_dir not in ("asc", "desc"):
            sort_dir = "asc"

        order_col = SORT_MAP.get(sort_col)

        if order_col:
            query += f" ORDER BY {order_col} {sort_dir.upper()} "
        else:
            query += """
                ORDER BY
                    LOWER(cs.Section_Name) ASC,
                    s.genius_sectionId ASC,
                    s.d2l_OrgUnitId ASC,
                    t.tag_name ASC,
                    v.tag_value ASC
            """

        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()

def map_tag_to_sections(tag_entry_id, selected_course_ids):
   db = localMySQLDB_connection.LocalDBConnection().connect()
   cursor = db.cursor()
   inserted_total = 0
   try:
       for item in selected_course_ids:
           parts = item.split("|||", 2)
           if len(parts) != 3:
               continue
           d2l_id, genius_id, sis_source = parts
           if d2l_id in ("None", None, ""):
               d2l_id = None
           if genius_id in ("None", None, ""):
               genius_id = None
           cursor.execute(
               """
               INSERT IGNORE INTO ufl_section_tags (d2l_OrgUnitId, genius_sectionId, tag_entry_id)
               VALUES (%s, %s, %s)
               """,
               (d2l_id, genius_id, tag_entry_id),
           )
           inserted_total += cursor.rowcount
       db.commit()
       return inserted_total > 0
   except Exception:
       db.rollback()
       raise
   finally:
       cursor.close()
       db.close()

def delete_section_tag(d2l_OrgUnitId, genius_sectionId, tag_entry_id):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor()
    try:
        if d2l_OrgUnitId in (None, "None", ""):
            cursor.execute(
                """
                DELETE FROM ufl_section_tags
                WHERE d2l_OrgUnitId IS NULL
                  AND genius_sectionId = %s
                  AND tag_entry_id = %s
                """,
                (genius_sectionId, tag_entry_id),
            )
        else:
            cursor.execute(
                """
                DELETE FROM ufl_section_tags
                WHERE d2l_OrgUnitId = %s
                  AND genius_sectionId = %s
                  AND tag_entry_id = %s
                """,
                (d2l_OrgUnitId, genius_sectionId, tag_entry_id),
            )

        db.commit()
        return cursor.rowcount > 0
    finally:
        cursor.close()
        db.close()

def get_filtered_course_sections1(
    search=None,
    search_course=None,
    tag_entry_id=None,
    start_date=None,
    end_date=None,
    department=None,
    term=None,
    tagged_status=None,
    excluded_courses=None,
    wild_card=None,
    wild_card_course=None,
    page=None,
    per_page=None,
    is_sql=False,
    genius_sectionId=None,
    salesforce_id=None,
):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)

    query = """                    
        SELECT
            cs.D2L_OrgUnitId AS d2l_OrgUnitId,
            cs.SIS_SectionCode AS genius_sectionId,
            cs.SIS_Source AS sis_source,
            cs.SalesforceId AS salesforce_id,
            cs.SalesforceSectionId AS salesforce_section_id,
            cs.Section_Name AS section_name,
            DATE_FORMAT(cs.Start_Date, '%Y-%m-%d') AS startDate,
            DATE_FORMAT(cs.End_Date, '%Y-%m-%d') AS endDate,
            cs.Term AS term_name,
            cs.Course_Name AS course_name,
            cs.Department_Name AS dept_name,
            t.tag_name,
            v.tag_value,
            st.tag_entry_id
        FROM (
            SELECT
                CASE
                    WHEN salesforce_courseoffering.GENIUS_LEGACY_ID__C REGEXP '^[0-9]+\\.0$'
                    THEN SUBSTRING_INDEX(salesforce_courseoffering.GENIUS_LEGACY_ID__C, '.', 1)
                    ELSE salesforce_courseoffering.GENIUS_LEGACY_ID__C
                END AS SIS_SectionCode,
                salesforce_courseoffering.ID AS SalesforceId,
                NULL AS SalesforceSectionId,
                CAST(salesforce_courseoffering.BRIGHTSPACE_ID__C AS UNSIGNED) AS D2L_OrgUnitId,
                salesforce_courseoffering.NAME AS Section_Name,
                salesforce_courseoffering.STARTDATE AS Start_Date,
                salesforce_courseoffering.ENDDATE AS End_Date,
                # genius_courses.NAME AS Course_Name,
                salesforce_courseoffering.NAME AS Course_Name,
                genius_departments.NAME AS Department_Name,
                genius_terms.NAME AS Term,
                'genius' AS SIS_Source
            FROM salesforce_courseoffering
                LEFT JOIN genius_courses_sections ON GENIUS_LEGACY_ID__C = SECTIONID
                LEFT JOIN genius_courses ON genius_courses.COURSEID = genius_courses_sections.COURSEID
                LEFT JOIN genius_terms ON genius_courses_sections.TERMID = genius_terms.TERMID
                LEFT JOIN genius_departments ON genius_courses.DEPARTMENTID = genius_departments.DEPARTMENTID
            WHERE salesforce_courseoffering.GENIUS_LEGACY_ID__C IS NOT NULL
            UNION ALL
            SELECT
                CASE
                    WHEN salesforce_section__c.COURSE_CODE__C REGEXP '^[0-9]+\\.0$'
                    THEN SUBSTRING_INDEX(salesforce_section__c.COURSE_CODE__C, '.', 1)
                    ELSE salesforce_section__c.COURSE_CODE__C
                END AS SIS_SectionCode,
                salesforce_courseoffering.ID AS SalesforceId,
                salesforce_section__c.ID AS SalesforceSectionId,
                CAST(salesforce_courseoffering.BRIGHTSPACE_ID__C AS UNSIGNED) AS D2L_OrgUnitId,
                salesforce_section__c.NAME AS Section_Name,
                salesforce_courseoffering.STARTDATE AS Start_Date,
                salesforce_courseoffering.ENDDATE AS End_Date,
                salesforce_courseoffering.NAME AS Course_Name,
                salesforce_learningprogram.NAME AS Department_Name,
                salesforce_academicterm.NAME AS Term,
                'salesforce' AS SIS_Source
            FROM salesforce_courseoffering
                LEFT JOIN salesforce_section__c ON COURSE_OFFERING__C = salesforce_courseoffering.ID
                LEFT JOIN salesforce_learningprogram ON salesforce_section__c.PROGRAM__C = salesforce_learningprogram.ID
                LEFT JOIN salesforce_academicterm ON ACADEMIC_TERM__C = salesforce_academicterm.ID
            WHERE salesforce_courseoffering.GENIUS_LEGACY_ID__C IS NULL
                AND salesforce_section__c.ID IS NOT NULL
        ) AS cs
        LEFT JOIN ufl_section_tags st
            ON (st.d2l_OrgUnitId = cs.D2L_OrgUnitId
                OR (st.d2l_OrgUnitId IS NULL AND cs.D2L_OrgUnitId IS NULL))
            AND st.genius_sectionId = cs.SIS_SectionCode
        LEFT JOIN ufl_tag_values v
            ON st.tag_entry_id = v.tag_entry_id
        LEFT JOIN ufl_tags t
            ON v.tag_id = t.tag_id
        WHERE 1 = 1
    """

    params = []

    try:
        if search:
            sl = search.lower()
            if wild_card == "exact_match":
                query += " AND LOWER(cs.Section_Name) = %s"
                params.append(sl)
            elif wild_card == "contains":
                query += " AND LOWER(cs.Section_Name) LIKE %s"
                params.append(f"%{sl}%")
            elif wild_card == "does_not_contain":
                query += " AND LOWER(cs.Section_Name) NOT LIKE %s"
                params.append(f"%{sl}%")
            elif wild_card == "ends_with":
                query += " AND LOWER(cs.Section_Name) LIKE %s"
                params.append(f"%{sl}")
            elif wild_card == "begins_with":
                query += " AND LOWER(cs.Section_Name) LIKE %s"
                params.append(f"{sl}%")
            else:
                query += " AND LOWER(cs.Section_Name) LIKE %s"
                params.append(f"%{sl}%")

        if search_course:
            cl = search_course.lower()
            if wild_card_course == "exact_match":
                query += " AND LOWER(cs.Course_Name) = %s"
                params.append(cl)
            elif wild_card_course == "contains":
                query += " AND LOWER(cs.Course_Name) LIKE %s"
                params.append(f"%{cl}%")
            elif wild_card_course == "does_not_contain":
                query += " AND LOWER(cs.Course_Name) NOT LIKE %s"
                params.append(f"%{cl}%")
            elif wild_card_course == "ends_with":
                query += " AND LOWER(cs.Course_Name) LIKE %s"
                params.append(f"%{cl}")
            elif wild_card_course == "begins_with":
                query += " AND LOWER(cs.Course_Name) LIKE %s"
                params.append(f"{cl}%")
            else:
                query += " AND LOWER(cs.Course_Name) LIKE %s"
                params.append(f"%{cl}%")

        if start_date:
            query += " AND DATE(cs.Start_Date) = %s"
            params.append(start_date)

        if end_date:
            query += " AND DATE(cs.End_Date) = %s"
            params.append(end_date)

        # if department:
        #     # Changed from an ID match (old d.departmentId) to a name match,
        #     # since the unified query only exposes Department_Name (string).
        #     # Flagged to Juliana — revisit if this loosens filtering more than expected.
        #     query += " AND LOWER(cs.Department_Name) LIKE %s"
        #     params.append(f"%{department.strip().lower()}%")

        if genius_sectionId:
            query += " AND TRIM(CAST(cs.SIS_SectionCode AS CHAR)) = TRIM(%s)"
            params.append(genius_sectionId)
        if salesforce_id:
            query += " AND TRIM(CAST(cs.SalesforceId AS CHAR)) = TRIM(%s)"
            params.append(salesforce_id)

        if term:
            query += " AND LOWER(cs.Term) LIKE %s"
            params.append(f"%{term.strip().lower()}%")

        if tagged_status == "tagged":
            query += " AND st.tag_entry_id IS NOT NULL AND v.tag_value IS NOT NULL"
        elif tagged_status == "not_tagged":
            query += " AND st.tag_entry_id IS NULL"

        count_query = f"SELECT COUNT(*) AS total_count FROM ({query}) AS subquery"
        cursor.execute(count_query, params)
        total_results = int(cursor.fetchone()["total_count"])

        query += " ORDER BY cs.Start_Date DESC"

        if page and per_page:
            offset = (int(page) - 1) * int(per_page)
            query += " LIMIT %s OFFSET %s"
            params = list(params) + [int(per_page), int(offset)]

        cursor.execute(query, params)
        return cursor.fetchall(), total_results
    finally:
        cursor.close()
        db.close()