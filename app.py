from flask import Flask, request

from api import ping, search

app = Flask(__name__)

@app.route('/api/ping', methods=['GET'])
def do_ping():
    return ping()

@app.route('/api/search', methods=['GET'])
def do_search():
    school_name = request.args.get('projectSchoolName', None)
    description = request.args.get('projectDescription', None)
    limit = request.args.get('limit', -1)
    offset = request.args.get('offset', 0)
    
    OPTIONAL_PARAMETER_MAP = {
        'startDate': 'project_phase_actual_start_date',
        'endDate': 'project_phase_planned_end_date',
        'budgetAmount': 'project_budget',
        'finalEstimate': 'final_estimate_of_actual_costs_through_end_of_phase_amount',
        'spendingAmount': 'total_phase_actual_spending_amount'
    }
    
    optional_parameters = []
    for key in OPTIONAL_PARAMETER_MAP:
        col_name = OPTIONAL_PARAMETER_MAP[key]
        value = request.args.get(key, None)
        if value is not None:
            optional_parameters.append((col_name, value))
    
    return search(school_name, description, optional_parameters, limit, offset)


def main():
    #import asyncio
    #import platform
    #if platform.system()=='Windows':
    #    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    from waitress import serve
    serve(app, host="127.0.0.1", port=8080, threads=16)

if __name__ == '__main__':
    main()