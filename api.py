from flask import jsonify, make_response, request
import requests
from db import get_connection, get_data_dict

def ping():
    response = {'success': True}
    return make_response(jsonify(response), 200)

def search(school_name, description, additional_params, limit, offset):
    conn = get_connection()
    cur = conn.cursor()
    query_params = []
    if school_name is not None:
        query_params.append("project_school_name = '%s'" % school_name)
    if description is not None:
        query_params.append("project_description = '%s'" % description)
    for param, value in additional_params:
        query_params.append("%s > %s" % (param, value))
    where_clause = ""
    if query_params:
        where_clause = "WHERE %s" % (' AND '.join(query_params))
    query = """
        SELECT * FROM projects
        %s
        LIMIT %s OFFSET %s
    """ % (where_clause, limit, offset)
    # use mogrify to sanitize later
    print(query)
    try:
        results = get_data_dict(cur, query)
        response = {
            'count': len(results),
            'results': results
        }
        response_code = 200
    except:
        response = 'Unable to process request'
        response_code = 400
    return make_response(jsonify(response), response_code)
