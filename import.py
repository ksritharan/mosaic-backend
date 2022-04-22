import json
from datetime import datetime
from db import get_connection_non_flask
def main():
    fp = open('AI Dataset.json', 'r')
    data = fp.read()
    json_data = json.loads(data)
    keys = json_data[0].keys()
    
    columns = get_columns(keys)
    
    conn = get_connection_non_flask(False)
    cur = conn.cursor()
    
    create_db(cur, columns, json_data[0])
    
    import_data(cur, keys, columns, json_data)
    
    conn.commit()
    
def get_columns(keys):
    columns = []
    for key in keys:
        columns.append(key.lower().replace(' ','_').replace('(','').replace(')',''))
    return columns

def get_column_types(obj):
    types = []
    for key in obj:
        val = obj[key]
        if isinstance(val, int):
            types.append('INTEGER')
        elif 'Date' in key:
            types.append('DATE')
        else:
            types.append('TEXT')
    return types

def create_db(cur, column_names, obj):
    query_1 = """
        DROP TABLE IF EXISTS projects;
    """
    cur.execute(query_1)
    
    column_types = get_column_types(obj)
    print(column_types)
    field_list = []
    for i, name in enumerate(column_names):
        record = "%s %s" % (name, column_types[i])
        field_list.append(record)
    fields = ",\n".join(field_list)
    query_2 = """
        CREATE TABLE projects (
            %s
        )    
    """ % fields
    print(query_2)
    cur.execute(query_2)

def import_data(cur, keys, columns, json_data):
    num_keys = len(keys)
    key_list = list(keys)
    columns_joined = ','.join(columns)
    values = []
    column_types = get_column_types(json_data[0])
    for obj in json_data:
        temp = []
        for i in range(num_keys):
            key = key_list[i]
            column_type = column_types[i]
            val = obj[key]
            if column_type in ('INTEGER',):
                if val is None:
                    temp.append('null')
                else:
                    temp.append(str(val))
            elif val is None:
                temp.append("''")
            elif column_type in ('DATE',):
                try:
                    d = datetime.strptime(val, "%d/%m/%y")
                    temp.append("'%s'" % val)
                except:
                    temp.append("null")
            else:
                temp.append("'%s'" % val.replace("'", "''"))
        values.append('(%s)' % ','.join(temp))
    records_to_insert = ",\n".join(values)
    
    debug = '''
    for value in values:
        query = """
        INSERT INTO projects (%s)
        VALUES %s
        
        """ % (columns_joined, value)
        print(column_types)
        print(query)
        cur.execute(query)
    '''
    query = """
        INSERT INTO projects (%s)
        VALUES %s
    """ % (columns_joined, records_to_insert)
    
    cur.execute(query)

if __name__ == '__main__':
    main()