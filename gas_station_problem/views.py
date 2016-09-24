from pyramid.view import view_config
from pyramid.response import Response

import os
import uuid
import shutil
import csv
from gas_station_problem.gasstation import GasStation
import colander
import deform.widget


def parse_file(file_path):
    '''
        Gets the content of the file uploaded
    '''
    results = []
    with open(file_path, newline='') as input_file:
        for row in csv.reader(input_file):
            results.append(row)

    return results


class MemoryTmpStore(dict):
    def preview_url(self, uid):
        return None


tmpstore = MemoryTmpStore()


class FileInput(colander.MappingSchema):
    input_file = colander.SchemaNode(
        deform.FileData(),
        widget=deform.widget.FileUploadWidget(tmpstore)
    )


class View(object):
    def __init__(self, request):
        self.request = request

    @property
    def file_form(self):
        schema = FileInput()
        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.file_form.get_widget_resources()

    @view_config(route_name='index_view',
                 renderer='templates/mytemplate.pt')
    def index_view(self):
        form = self.file_form.render()

        if 'submit' in self.request.params:
            #form submission

            try:
                #try to validate the form

                controls = self.request.POST.items()

                values = self.file_form.validate(controls)

                print(values)
                # input_file = self.request.POST['input_file'].file

                input_file = values['input_file']['fp']

                result = []

                file_path = os.path.join('/tmp', '%s.csv' % uuid.uuid4())

                temp_file_path = file_path + '~'

                input_file.seek(0)
                with open(temp_file_path, 'wb') as output_file:
                    shutil.copyfileobj(input_file, output_file)

                os.rename(temp_file_path, file_path)

                list_input = parse_file(file_path)

                for l in list_input:
                    result.append(GasStation(l))

                return Response('%s' % result)

            except deform.ValidationFailure as e:
                #form is not valid
                return dict(form=e.render())

        else:
            #simple form rendering
            return dict(form=form)
