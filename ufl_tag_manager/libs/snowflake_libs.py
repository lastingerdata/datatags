import snowflake.connector, pandas, uuid
from snowflake.connector.pandas_tools import write_pandas 

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def get_pkb():
    try:
        import os
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.backends import default_backend
        current_libs_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(current_libs_dir, "../../../secure/snowflake_key.p8.encrypted")
        with open(key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=b'1<sqT9VJw$?x8zGNB+[yvAVl',  
                backend=default_backend()
            )
        pkb = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pkb
    except Exception as e: print(f"Content-Type: text/html\n\n{e}<hr>{type(e).__name__}")         

def map_dtype_to_snowflake(dtype):
    if pandas.api.types.is_integer_dtype(dtype):
        return "NUMBER"
    elif pandas.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pandas.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    elif pandas.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP_NTZ"
    else:
        return "TEXT"
 
def prep_dataframe(this_dataframe):
    
    text_columns = []
    for col, dtype in zip(this_dataframe.columns, this_dataframe.dtypes):
        if map_dtype_to_snowflake(dtype) == 'TEXT':
            text_columns.append(col)

    def decode_and_clean(value):
        if isinstance(value, bytes):
            # --- LOGIC A: Handle MySQL BINARY(16) UUIDs ---
            # MySQL stores UUIDs as exactly 16 bytes.
            if len(value) == 16:
                try:
                    # This converts raw bytes to 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'
                    return str(uuid.UUID(bytes=value))
                except (ValueError, TypeError):
                    # If conversion fails (rare), fall through to Logic B
                    pass

            # --- LOGIC B: Handle Dirty Text (Latin-1 / NBSP) ---
            # If it's not a UUID (or is a byte string of a different length),
            # decode it as text to handle characters like 0xa0.
            return value.decode('latin1').strip()

        elif isinstance(value, str):
            # Clean existing strings
            return value.strip()

        # Handle None/NaN
        return value    
    for col in text_columns:
        if col in this_dataframe.columns:
            # Convert blanks to None
            this_dataframe[col] = this_dataframe[col].replace("", None)
            this_dataframe[col] = this_dataframe[col].apply(decode_and_clean)
            this_dataframe[col] = this_dataframe[col].astype("string")  # pandas' nullable string dtype

    for col in this_dataframe.columns:
        if pandas.api.types.is_datetime64_any_dtype(this_dataframe[col]):
            # treat empty strings as NA so they coerce to NaT
            s = this_dataframe[col].replace("", pandas.NA)
            # parse everything as UTC-aware to handle ISO strings with 'Z', then drop tz
            s = pandas.to_datetime(s, errors='coerce', utc=True).dt.tz_localize(None)
            # format for MySQL TIMESTAMP/DATETIME (NaT → NaN; keep as NA if you prefer)
            this_dataframe[col] = s.dt.strftime("%Y-%m-%d %H:%M:%S")
                            
    # uppercase dataframe columns, then set quote_identifiers to TRUE
    # all for reserved words in column names
        this_dataframe.columns = [col.upper() for col in this_dataframe.columns]
    
    return this_dataframe


def map_dtype_to_snowflake(dtype):
    if pandas.api.types.is_integer_dtype(dtype):
        return "NUMBER"
    elif pandas.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pandas.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    elif pandas.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP_NTZ"
    else:
        return "TEXT"
    
def get_create_table(this_dataframe, table_name, this_schema = None):
    this_dataframe.columns = [col.upper() for col in this_dataframe.columns]

    column_defs = [
        f'"{col.upper()}" {map_dtype_to_snowflake(dtype)}'
        for col, dtype in zip(this_dataframe.columns, this_dataframe.dtypes)
    ]
    if this_schema is None:
        create_table_sql = 'CREATE OR REPLACE TABLE "'+table_name.upper()+'" ( ' + ", ".join(column_defs) + ')'
    else:
        create_table_sql = 'CREATE OR REPLACE TABLE "'+this_schema.upper()+'"."' + table_name.upper()+'" ( ' + ", ".join(column_defs) + ')'
    return create_table_sql

    