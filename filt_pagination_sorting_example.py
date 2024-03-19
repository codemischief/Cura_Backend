import psycopg2

query_map = {
    "special_case1" : '',
    "special_case2": '',
}

def getFilteredAndPaginatedDataFromDatabaseTable(db_config,
                                                 required_columns,
                                                 table_name,
                                                 filters=None,
                                                 sort_column=None,
                                                 sort_order='asc',
                                                 page_number=1,
                                                 page_size=10):
    try:
        # Base query
        query = f"SELECT {','.join(required_columns)} FROM {table_name}"
        # Adding filters
        where_clauses = []
        for column, filter_type, value in (filters or []):
            if filter_type == 'startsWith':
                where_clauses.append(f"{column} LIKE '{value}%'")
            elif filter_type == 'endsWith':
                where_clauses.append(f"{column} LIKE '%{value}'")
            elif filter_type == 'contains':
                where_clauses.append(f"{column} LIKE '%{value}%'")
            elif filter_type == 'exactMatch':
                where_clauses.append(f"{column} = '{value}'")
            elif filter_type == 'isNull':
                where_clauses.append(f"{column} = ''")
            elif filter_type == 'isNotNull':
                where_clauses.append(f"{column} != ''")

        # handle where clause and sorting
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        if sort_column:
            query += f" ORDER BY {sort_column} {sort_order}"
        # Calculate OFFSET
        offset = (page_number - 1) * page_size
        # Adding pagination
        query += f" LIMIT {page_size} OFFSET {offset}"
        print(f'Prepared final query [{query}]')
        # fetch results and return to caller
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {'data':rows, 'message':'success'}
    except Exception as e:
        msg = str(e).replace("\n","")
        return {'data':None, 'message':f'exception due to <{msg}>'}

# Database configuration
db_config = {
    'dbname': 'cura_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

# Example usage
results = getFilteredAndPaginatedDataFromDatabaseTable(
    db_config=db_config,
    # BACKEND CAN FIND IT
    table_name='builder',
    # FROM_UI
    #required_columns=['id','buildername','phone1','phone2','email1','email2','city','state','country'],
    required_columns=['id','buildername','country', 'city', 'suburb'],
    # FROM_UI
    filters=[
        ('buildername', 'contains', 's'),
        ('email1', 'isNull', None),
        ('phone2','isNotNull',None),
        ('phone1', 'endWith', '00'),
    ],
    # FROM_UI
    sort_column='buildername',
    # FROM_UI
    sort_order='asc',
    # FROM_UI
    page_number=1,
    # FROM_UI
    page_size=10
)

# Print the results
if results['data'] is not None:
    for row in results['data']:
        print(row)
else:
    print (results['message'])