import os
from typing import Optional, Dict, Any

import pymysql
from pymysql.cursors import DictCursor


def get_connection():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "caruser"),
        password=os.getenv("MYSQL_PASSWORD", "carpass"),
        database=os.getenv("MYSQL_DATABASE", "carvalue"),
        cursorclass=DictCursor,
        autocommit=True,
    )


def _run_query(
    conn,
    make: str,
    year: int,
    model_prefix: str,
    debug: bool = False,
) -> Optional[Dict[str, Any]]:
    sql = """
        SELECT *
        FROM datasource
        WHERE make = %s
          AND year = %s
          AND model LIKE %s
        LIMIT 1
    """
    params = (make, year, f"{model_prefix}%")

    if debug:
        print("SQL:", sql.strip())
        print("PARAMS:", params)

    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchone()


async def canprice(make: str, model: str, year: int, debug: bool = False) -> dict:
    last_year = year - 1
    next_year = year + 1
    parts = model.split()

    conn = get_connection()
    try:
        # 1. Exact year, full model prefix
        row = _run_query(conn, make, year, model, debug)
        if row:
            return {"result": "true", "price_new": int(row["price_new"])}

        # 2. First 4 parts, same year / last year / next year
        if len(parts) > 3:
            prefix4 = " ".join(parts[:4])

            row = _run_query(conn, make, year, prefix4, debug)
            if row:
                return {"result": "true", "price_new": int(row["price_new"])}

            row = _run_query(conn, make, last_year, prefix4, debug)
            if row:
                return {"result": "true", "price_new": int(row["price_new"])}

            row = _run_query(conn, make, next_year, prefix4, debug)
            if row:
                return {"result": "true", "price_new": int(row["price_new"])}

        # 3. First 3 parts, same year / last year / next year
        if len(parts) > 2:
            prefix3 = " ".join(parts[:3])

            row = _run_query(conn, make, year, prefix3, debug)
            if row:
                return {"result": "true", "price_new": int(row["price_new"])}

            row = _run_query(conn, make, last_year, prefix3, debug)
            if row:
                return {"result": "true", "price_new": int(row["price_new"])}

            row = _run_query(conn, make, next_year, prefix3, debug)
            if row:
                return {"result": "true", "price_new": int(row["price_new"])}

            # 4. First 2 parts, only if first part length > 2, same year only
            if len(parts[0]) > 2:
                prefix2 = " ".join(parts[:2])

                row = _run_query(conn, make, year, prefix2, debug)
                if row:
                    return {"result": "true", "price_new": int(row["price_new"])}

        return {"result": "false", "price_new": 0}

    finally:
        conn.close()