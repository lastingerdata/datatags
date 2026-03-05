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
        "section_name": "gcs.name",
        "tag_name": "t.tag_name",
        "tag_value": "v.tag_value",
    }

    query = """
        SELECT
            s.d2l_OrgUnitId,
            s.genius_sectionId,
            s.tag_entry_id,
            gcs.name as section_name,
            v.tag_id,
            v.tag_value,
            t.tag_name
        FROM genius_courses_sections gcs
        LEFT JOIN ufl_section_tags s
            ON (s.d2l_OrgUnitId = gcs.externalSectionCode
                OR (s.d2l_OrgUnitId IS NULL AND gcs.externalSectionCode IS NULL))
            AND s.genius_sectionId = gcs.sectionId
        JOIN ufl_tag_values v ON s.tag_entry_id = v.tag_entry_id
        JOIN ufl_tags t ON v.tag_id = t.tag_id
        WHERE 1 = 1
    """

    params = []

    try:
        if name:
            nl = name.lower()
            if wild_card == "exact_match":
                query += " AND LOWER(gcs.name) = %s"
                params.append(nl)
            elif wild_card == "contains":
                query += " AND LOWER(gcs.name) LIKE %s"
                params.append(f"%{nl}%")
            elif wild_card == "does_not_contain":
                query += " AND LOWER(gcs.name) NOT LIKE %s"
                params.append(f"%{nl}%")
            elif wild_card == "ends_with":
                query += " AND LOWER(gcs.name) LIKE %s"
                params.append(f"%{nl}")
            elif wild_card == "begins_with":
                query += " AND LOWER(gcs.name) LIKE %s"
                params.append(f"{nl}%")
            else:
                query += " AND LOWER(gcs.name) LIKE %s"
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
                    LOWER(gcs.name) ASC,
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
            d2l_id, genius_id = item.split("_", 1)
            if d2l_id in ("None", None, ""):
                d2l_id = None

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
):
    db = localMySQLDB_connection.LocalDBConnection().connect()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT
            cs.externalSectionCode AS d2l_OrgUnitId,
            cs.sectionId AS genius_sectionId,
            cs.name AS section_name,
            DATE_FORMAT(cs.startDate, '%Y-%m-%d') AS startDate,
            DATE_FORMAT(cs.endDate, '%Y-%m-%d') AS endDate,
            gt.name AS term_name,
            c.name AS course_name,
            d.name AS dept_name,
            t.tag_name,
            v.tag_value,
            st.tag_entry_id
        FROM genius_courses_sections cs
        LEFT JOIN genius_courses c
            ON cs.courseId = c.courseId
        LEFT JOIN genius_departments d
            ON c.departmentId = d.departmentId
        LEFT JOIN genius_terms gt
            ON cs.termId = gt.termId
        LEFT JOIN ufl_section_tags st
            ON (st.d2l_OrgUnitId = cs.externalSectionCode
                OR (st.d2l_OrgUnitId IS NULL AND cs.externalSectionCode IS NULL))
            AND cs.sectionId = st.genius_sectionId
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
                query += " AND LOWER(cs.name) = %s"
                params.append(sl)
            elif wild_card == "contains":
                query += " AND LOWER(cs.name) LIKE %s"
                params.append(f"%{sl}%")
            elif wild_card == "does_not_contain":
                query += " AND LOWER(cs.name) NOT LIKE %s"
                params.append(f"%{sl}%")
            elif wild_card == "ends_with":
                query += " AND LOWER(cs.name) LIKE %s"
                params.append(f"%{sl}")
            elif wild_card == "begins_with":
                query += " AND LOWER(cs.name) LIKE %s"
                params.append(f"{sl}%")
            else:
                query += " AND LOWER(cs.name) LIKE %s"
                params.append(f"%{sl}%")

        if search_course:
            cl = search_course.lower()
            if wild_card_course == "exact_match":
                query += " AND LOWER(c.name) = %s"
                params.append(cl)
            elif wild_card_course == "contains":
                query += " AND LOWER(c.name) LIKE %s"
                params.append(f"%{cl}%")
            elif wild_card_course == "does_not_contain":
                query += " AND LOWER(c.name) NOT LIKE %s"
                params.append(f"%{cl}%")
            elif wild_card_course == "ends_with":
                query += " AND LOWER(c.name) LIKE %s"
                params.append(f"%{cl}")
            elif wild_card_course == "begins_with":
                query += " AND LOWER(c.name) LIKE %s"
                params.append(f"{cl}%")
            else:
                query += " AND LOWER(c.name) LIKE %s"
                params.append(f"%{cl}%")

        if start_date:
            query += " AND DATE(cs.startDate) = %s"
            params.append(start_date)

        if end_date:
            query += " AND DATE(cs.endDate) = %s"
            params.append(end_date)

        if department:
            query += " AND d.departmentId = %s"
            params.append(department)

        if term:
            query += " AND LOWER(gt.name) LIKE %s"
            params.append(f"%{term.strip().lower()}%")

        if tagged_status == "tagged":
            query += " AND st.tag_entry_id IS NOT NULL AND v.tag_value IS NOT NULL"
        elif tagged_status == "not_tagged":
            query += " AND st.tag_entry_id IS NULL"

        count_query = f"SELECT COUNT(*) AS total_count FROM ({query}) AS subquery"
        cursor.execute(count_query, params)
        total_results = int(cursor.fetchone()["total_count"])

        query += " ORDER BY cs.startDate DESC"

        if page and per_page:
            offset = (int(page) - 1) * int(per_page)
            query += " LIMIT %s OFFSET %s"
            params = list(params) + [int(per_page), int(offset)]

        cursor.execute(query, params)
        return cursor.fetchall(), total_results
    finally:
        cursor.close()
        db.close()