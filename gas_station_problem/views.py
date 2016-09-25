import os
import uuid
import shutil
import csv

from pyramid.view import view_config
from gas_station_problem.gasstation import GasStationClass
import colander
import deform.widget


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
        submit = deform.Button(name='submit', css_class='btn btn-primary')
        return deform.Form(schema, buttons=(submit,))

    @property
    def reqts(self):
        return self.file_form.get_widget_resources()


    def read_and_parse_file(self, input_file):
        '''
            Get the file uploaded, save in a temporary folder and return the content
        '''
        file_path = os.path.join('/tmp', '%s.csv' % uuid.uuid4())

        temp_file_path = file_path + '~'

        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        os.rename(temp_file_path, file_path)

        #Read the content
        results = []
        with open(file_path, newline='') as input_file:
            for row in csv.reader(input_file, skipinitialspace=True):
                results.append(row)

        return results

    @view_config(route_name='index_view', renderer='templates/mytemplate.pt')
    def index_view(self):

        if 'submit' in self.request.params:
            #form submission

            try:
                #validate the form, read the content of uploaded file and call algorithm

                controls = self.request.POST.items()

                values = self.file_form.validate(controls)

                input_file = values['input_file']['fp']

                list_input = self.read_and_parse_file(input_file)

                result = []

                gasStationObj = GasStationClass()
                for l in list_input:
                    result.append(gasStationObj.GasStation(l))

                form = self.file_form.render()
                return dict(form=form, response_text=result)

            except deform.ValidationFailure as e:
                #form is not valid
                return dict(form=e.render(), response_text='')

        else:
            #simple form rendering

            form = self.file_form.render()
            return dict(form=form, response_text='')
