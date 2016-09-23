from pyramid.view import view_config
import os
import uuid
import shutil
import csv
from gas_station_problem.gasstation import GasStation

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'gas_station_problem'}


@view_config(route_name='result', renderer='templates/result.pt')
def gas_station_view(request):

    input_file = request.POST['input_file'].file

    file_path = os.path.join('/tmp', '%s.csv' % uuid.uuid4())

    temp_file_path = file_path + '~'

    input_file.seek(0)
    with open(temp_file_path, 'wb') as output_file:
        shutil.copyfileobj(input_file, output_file)

    os.rename(temp_file_path, file_path)

    list_input = parse_file(file_path)

    result = []

    for l in list_input:
        result.append(GasStation(l))

    return {'result': result}


def parse_file(file_path):

    results = []
    with open(file_path, newline='') as input_file:
        for row in csv.reader(input_file):
            results.append(row)

    return results
