import pandas as pd
import snowflake.connector
import streamlit as st

def main():
    st.set_page_config(
        page_title="Snowflake Column Search",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("❄️ Snowflake Column Search")

    with st.sidebar:
        st.header("Configuration ⚙️")
        user = st.text_input("Username 🧑‍💼")
        use_external_browser_auth = st.checkbox("Use External Browser Authentication")
        password = ""
        authenticator = "externalbrowser" if use_external_browser_auth else "snowflake"
        if not use_external_browser_auth:
            password = st.text_input("Password 🔒", type="password")
        account = st.text_input("Account 🏦")
        warehouse = st.text_input("Warehouse 🏭")
        column_search = st.text_input("Column Name to search for 🔍", "")
        search_value = st.text_input("Value to search within column 🔍", "")
        exclude_databases = st.text_input(
            "Databases to exclude (comma-separated) 🔍", ""
        )
        exclude_schemas = st.text_input(
            "Schemas to exclude (comma-separated) 🔍", ""
        )
        exclude_tables = st.text_input(
            "Tables to exclude (comma-separated) 🔍", ""
        )

        generate_scripts = st.button("Run Search 🚀")

    if generate_scripts:
        if (
            not user
            or not account
            or not warehouse
            or not column_search
            or not search_value
        ):
            st.error("Please fill in all required fields.")
            return

        excluded_dbs = [
            db.strip() for db in exclude_databases.split(",") if db.strip()
        ]
        excluded_schemas = [
            schema.strip() for schema in exclude_schemas.split(",") if schema.strip()
        ]
        excluded_tables = [
            table.strip() for table in exclude_tables.split(",") if table.strip()
        ]

        try:
            ctx = snowflake.connector.connect(
                user=user,
                account=account,
                password=password,
                authenticator=authenticator,
                warehouse=warehouse,
            )

            exclusion_clause = []
            if excluded_dbs:
                exclusion_clause.append(" AND ".join([f"table_catalog != '{db}'" for db in excluded_dbs]))
            if excluded_schemas:
                exclusion_clause.append(" AND ".join([f"table_schema != '{schema}'" for schema in excluded_schemas]))
            if excluded_tables:
                exclusion_clause.append(" AND ".join([f"table_name != '{table}'" for table in excluded_tables]))

            exclusion_clause = " AND " + " AND ".join(exclusion_clause) if exclusion_clause else ""

            find_columns_query = f"""
            SELECT table_catalog, table_schema, table_name, column_name
            FROM snowflake.account_usage.columns 
            WHERE column_name ILIKE %s
            AND DELETED IS NULL
            {exclusion_clause};
            """

            cursor = ctx.cursor()
            cursor.execute(find_columns_query, (f"%{column_search}%",))
            columns = cursor.fetchall()

            df_columns = pd.DataFrame(
                columns,
                columns=[
                    "Database Catalog",
                    "Database Schema",
                    "Table Name",
                    "Column Name",
                ],
            )

            if not df_columns.empty:
                st.write("Found columns:", df_columns)

                queries = []
                for _, row in df_columns.iterrows():
                    catalog, schema, table, column_name = row
                    query = f"""
                    SELECT '{catalog}.{schema}.{table}.{column_name}' AS search_column_name, 
                           '{catalog}' AS database_catalog, 
                           '{schema}' AS database_schema, 
                           '{table}' AS database_table, 
                           \"{column_name}\" AS example_value 
                    FROM \"{catalog}\".\"{schema}\".\"{table}\" 
                    WHERE \"{column_name}\" ILIKE '%{search_value}%'
                    """
                    queries.append(query)
                dynamic_sql = " UNION ALL \n".join(queries) + ";" if queries else ""

                if queries:
                    st.download_button(
                        label="Download SQL query",
                        data=dynamic_sql,
                        file_name="generated_query.sql",
                        mime="text/plain",
                    )
                else:
                    st.info(
                        "No additional queries generated based on the search value."
                    )
            else:
                st.info("No tables found with the specified column.")

        except Exception as e:
            st.error(f"Failed to connect or query Snowflake: {e}")
        finally:
            if cursor is not None:
                cursor.close()
            if ctx is not None:
                ctx.close()

if __name__ == "__main__":
    main()
