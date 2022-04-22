from app import main
import requests
import inspect
import sys

def unit_testing():
    tests = [obj for name,obj in inspect.getmembers(sys.modules[__name__]) 
                     if (inspect.isfunction(obj) and name.startswith('testing'))]
    total_passed = 0
    total_tests = len(tests)
    for test in tests:
        print(test.__name__)
        result = test()
        if result:
            total_passed += 1
            print('Passed')
        else:
            print('Failed')
    print('Done testing. %d/%d tests passed' % (total_passed, total_tests))

def testing_ping():
    url = 'http://127.0.0.1:8080/api/ping'
    print('\t', url)
    response = requests.get(url)
    response_status_code = response.status_code
    response_json = response.json()
    print('\t', response)
    print('\t', 'Response Code:', response_status_code)
    print('\t', 'Response JSON:', response_json)
    if (response_status_code == 200 
            and response_json.get('success', False) == True):
        return True
    return False
    
def testing_search():
    url = 'http://127.0.0.1:8080/api/search'
    print('\t', url)
    response = requests.get(url)
    response_status_code = response.status_code
    response_json = response.json()
    #print('\t', response)
    print('\t', 'Response Code:', response_status_code)
    #print('\t', 'Response JSON:', response_json)
    print('\t', 'count', response_json['count'])
    print('\t', response_json['results'][0])
    if (response_status_code == 200 
            and response_json['count'] == 8185):
        return True
    return False
    
def testing_search_pagination():
    url = 'http://127.0.0.1:8080/api/search?limit=25'
    print('\t', url)
    response = requests.get(url)
    response_status_code = response.status_code
    response_json = response.json()
    #print('\t', response)
    print('\t', 'Response Code:', response_status_code)
    #print('\t', 'Response JSON:', response_json)
    print('\t', 'count', response_json['count'])
    print('\t', response_json['results'][0])
    if (response_status_code == 200 
            and response_json['count'] == 25):
        return True
    return False
    
def testing_search_pagination2():
    url = 'http://127.0.0.1:8080/api/search?limit=25&offset=25'
    print('\t', url)
    response = requests.get(url)
    response_status_code = response.status_code
    response_json = response.json()
    #print('\t', response)
    print('\t', 'Response Code:', response_status_code)
    #print('\t', 'Response JSON:', response_json)
    print('\t', 'count', response_json['count'])
    print('\t', response_json['results'][0])
    if (response_status_code == 200 
            and response_json['count'] == 25):
        return True
    return False

OPTIONAL_PARAMETER_MAP = {
    'startDate': 'project_phase_actual_start_date',
    'endDate': 'project_phase_planned_end_date',
    'budgetAmount': 'project_budget',
    'finalEstimate': 'final_estimate_of_actual_costs_through_end_of_phase_amount',
    'spendingAmount': 'total_phase_actual_spending_amount'
}

def testing_search_parameters():
    url = 'http://127.0.0.1:8080/api/search?projectSchoolName=P.S.%20279%20-%20BRONX&projectDescription=WATER%20PENETRATION/ROOFS'
    
    response = requests.get(url)
    response_status_code = response.status_code
    response_json = response.json()
    #print('\t', response)
    print('\t', 'Response Code:', response_status_code)
    #print('\t', 'Response JSON:', response_json)
    print('\t', 'count', response_json['count'])
    print('\t', response_json['results'][0])
    if (response_status_code == 200 
            and response_json['count'] == 4):
        return True
    return False

if __name__ == '__main__':
    import threading
    threading.Thread(target=unit_testing, daemon=True).start()
    main()