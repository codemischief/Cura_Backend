import traceback
import psycopg2
import logging

query_map = {
    "special_case1" : '',
    "special_case2": '',
}


logger = logging.getLogger(__name__)

def filterAndPaginate(db_config,
                      required_columns,
                      table_name,
                      filters=None,
                      sort_column=None,
                      sort_order='asc',
                      page_number=1,
                      page_size=10,
                      query = None,
                      search_key = None):
    try:
        # Base query
        query_frontend = False
        if query is None:
            query = f"SELECT distinct {','.join(required_columns)} FROM {table_name}"
            query_frontend = True
        # Adding filters
        where_clauses = []
        for column, filter_type, value in (filters or []):
            if value != '':
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
        if where_clauses and query_frontend:
            query += " WHERE " + " AND ".join(where_clauses)
        elif where_clauses and not query_frontend:
            query += " AND " + " AND ".join(where_clauses)
        if sort_column:
            query += f" ORDER BY {sort_column[0]} {sort_order}"
        # Handle pagination
        counts_query = query
        if page_number !=0 and page_size !=0 and search_key is None:
            # Calculate OFFSET
            offset = (page_number - 1) * page_size
            # Adding pagination
            query += f" LIMIT {page_size} OFFSET {offset}"
        else:
            pass
            # when page_number=0 and page_size=0
            # do not paginate - return all. This is
            # for downloading all the filtered data.

        #logging.info(f'Prepared final query [{query}]')
        # fetch results and return to caller
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()
        cur.execute(query)
        #logging.info(f"Cursor message is {cur.statusmessage}")
        rows = cur.fetchall()
        cur = conn.cursor()
        cur.execute(counts_query)
        rows_for_counts = cur.fetchall()
        total_count = len(rows_for_counts)
        colnames = [desc[0] for desc in cur.description]
        #logging.info(f'filterAndPaginate: Given filter yeilds <{total_count}> entries')
        cur.close()
        conn.close()

        if search_key is not None:
            search_results = []
            for row in rows:
                concatenated_row = " ".join( str(item) for item in row)
                if str(search_key).lower() in concatenated_row.lower():
                    search_results.append(row)
                else:
                    pass
            total_count = len(search_results)
            #logging.info(f'filterAndPaginate: Given search key <{search_key}> yeilds <{total_count}> entries')
            start_index = (page_number - 1) * page_size
            end_index = start_index + page_size
            rows = search_results[start_index:end_index]

        return {'data':rows, 'total_count' : total_count, 'message':'success', 'colnames':colnames}
    except Exception as e:
        #logging.exception(traceback.print_exc())
        msg = str(e).replace("\n","")
        return {'data':None, 'message':f'exception due to <{msg}>'}



def filterAndPaginate_v2(db_config,
                         required_columns,
                         table_name,
                         filters=None,
                         sort_column=None,
                         sort_order='asc',
                         page_number=1,
                         page_size=10,
                         query = None,
                         search_key = None):
    try:
        # Base query
        query_frontend = False
        if query is None:
            query = f"SELECT distinct {','.join(required_columns)} FROM {table_name}"
            query_frontend = True
        # Adding filters
        where_clauses = []
        print(filters)
        for column, filter_type, value, dataType in (filters or []):
            ##########################################################
            #                     STRING FILTERS
            ##########################################################
            if dataType == 'String':
                if filter_type == 'contains':
                    where_clauses.append(f"{column} LIKE '%{value}%'")
                elif filter_type == 'doesNotContain':
                    where_clauses.append(f"{column} NOT LIKE '%{value}%'")
                elif filter_type == 'startsWith':
                    where_clauses.append(f"{column} LIKE '{value}%'")
                elif filter_type == 'endsWith':
                    where_clauses.append(f"{column} LIKE '%{value}'")
                elif filter_type == 'equalTo':
                    where_clauses.append(f"{column} = '{value}'")
                elif filter_type == 'isNull':
                    where_clauses.append(f"{column} = ''")
                elif filter_type == 'isNotNull':
                    where_clauses.append(f"{column} != ''")
            ##########################################################
            #                     NUMERIC FILTERS
            ##########################################################
            elif dataType == 'Numeric':
                if filter_type == 'equalTo':
                    where_clauses.append(f"{column} = {value}")
                elif filter_type == 'notEqualTo':
                    where_clauses.append(f"{column} != {value}")
                elif filter_type == 'greaterThan':
                    where_clauses.append(f"{column} > {value}")
                elif filter_type == 'lessThan':
                    where_clauses.append(f"{column} < {value}")
                elif filter_type == 'greaterThanOrEqualTo':
                    where_clauses.append(f"{column} >= {value}")
                elif filter_type == 'lessThanOrEqualTo':
                    where_clauses.append(f"{column} =< {value}")
                elif filter_type == 'between':
                    where_clauses.append(f" ({column} >= {value[0]} AND {column} <= {value[1]}) ")
                elif filter_type == 'notBetween':
                    where_clauses.append(f" ({column} <= {value[0]} OR {column} >= {value[1]}) ")
                elif filter_type == 'isNull':
                    where_clauses.append(f"{column} is null")
                elif filter_type == 'isNotNull':
                    where_clauses.append(f"{column} is not null")
            ##########################################################
            #                     DATE FILTERS
            ##########################################################
            elif dataType == 'Date':
                if filter_type == 'equalTo':
                    where_clauses.append(f"{column} = '{value}'")
                elif filter_type == 'notEqualTo':
                    where_clauses.append(f"{column} != '{value}'")
                elif filter_type == 'greaterThan':
                    where_clauses.append(f"{column} > '{value}'")
                elif filter_type == 'lessThan':
                    where_clauses.append(f"{column} < '{value}'")
                elif filter_type == 'greaterThanOrEqualTo':
                    where_clauses.append(f"{column} >= '{value}'")
                elif filter_type == 'lessThanOrEqualTo':
                    where_clauses.append(f"{column} <= '{value}'")
                elif filter_type == 'isNull':
                    where_clauses.append(f"{column} is null")
                elif filter_type == 'isNotNull':
                    where_clauses.append(f"{column} is not null")
            else:
                # must throw a warning here
                pass
        # handle where clause and sorting
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        if sort_column:
            query += f" ORDER BY {sort_column} {sort_order}"
        # Handle pagination
        counts_query = query
        if page_number !=0 and page_size !=0 and search_key is None:
            # Calculate OFFSET
            offset = (page_number - 1) * page_size
            # Adding pagination
            query += f" LIMIT {page_size} OFFSET {offset}"
        else:
            pass
            # when page_number=0 and page_size=0
            # do not paginate - return all. This is
            # for downloading all the filtered data.

        #logging.info(f'Prepared final query [{query}]')
        print(f'\nPrepared final query [{query}]\n')
        # fetch results and return to caller
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute(query)
        #logging.info(f"Cursor message is {cur.statusmessage}")
        rows = cur.fetchall()
        cur = conn.cursor()
        cur.execute(counts_query)
        rows_for_counts = cur.fetchall()
        total_count = len(rows_for_counts)
        colnames = [desc[0] for desc in cur.description]
        #logging.info(f'filterAndPaginate: Given filter yeilds <{total_count}> entries')
        cur.close()
        conn.close()

        if search_key is not None:
            search_results = []
            for row in rows:
                concatenated_row = " ".join( str(item) for item in row)
                if str(search_key).lower() in concatenated_row.lower():
                    search_results.append(row)
                else:
                    pass
            total_count = len(search_results)
            #logging.info(f'filterAndPaginate: Given search key <{search_key}> yeilds <{total_count}> entries')
            start_index = (page_number - 1) * page_size
            end_index = start_index + page_size
            rows = search_results[start_index:end_index]

        return {'data':rows, 'total_count' : total_count, 'message':'success', 'colnames':colnames}
    except Exception as e:
        #logging.exception(traceback.print_exc())
        print(traceback.print_exc())
        msg = str(e).replace("\n","")
        return {'data':None, 'message':f'exception due to <{msg}>'}

# Database configuration
db_config = {
    'dbname': 'cura_db',
    'user': 'postgres',
    'password': 'cura123',
    'host': '20.197.13.140'
}

# Example usage
#results_v1 = filterAndPaginate(
#    db_config=db_config,
#    # BACKEND CAN FIND IT
#    table_name='builder',
#    # FROM_UI
#    #required_columns=['id','buildername','phone1','phone2','email1','email2','city','state','country'],
#    required_columns=['id','buildername','country', 'city', 'suburb'],
#    # FROM_UI
#    # possible datatypes are 'String', 'Numeric', 'Date'
#    filters=[
#        ('buildername', 'contains', 's', 'String'),
#        ('email1', 'isNull', None, 'String'),
#        ('phone2','isNotNull',None, 'String'),
#        ('phone1', 'endWith', '00', 'String'),
#    ],
#    # FROM_UI
#    sort_column='buildername',
#    # FROM_UI
#    sort_order='asc',
#    # FROM_UI
#    page_number=1,
#    # FROM_UI
#    page_size=10
#)
#
## Print the results
#if results_v1['data'] is not None:
#    for row in results_v1['data']:
#        print(row)
#else:
#    print (results_v1['message'])

results_v2 = filterAndPaginate_v2(
    db_config=db_config,
    # BACKEND CAN FIND IT
    table_name='builder',
    # FROM_UI
    # required_columns=['id','buildername','phone1','phone2','email1','email2','city','state','country'],
    required_columns=['id', 'buildername', 'country', 'city', 'suburb', 'dated'],
    # FROM_UI
    # possible datatypes are 'String', 'Numeric', 'Date'
    filters=[
        ['id', 'notBetween', [0,5], 'Numeric'],
        ['dated', 'lessThanOrEqualTo', '01-01-2016', 'Date'],
        ['buildername', 'contains', 'rum', 'String'],
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
if results_v2['data'] is not None:
    for row in results_v2['data']:
        print(row)
else:
    print(results_v2['message'])
print(results_v2)