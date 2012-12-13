import colander
import deform
import deform_jquery_file_upload
from pyramid.view import view_config

tmpstore = {}

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'jquery_file_upload_project'}

@view_config(route_name="test", renderer='templates/test.pt')
def test(request):
    class Schema(colander.Schema):
        upload = colander.SchemaNode(
                deform.FileData(),
                widget=deform_jquery_file_upload.JqueryFileUploadWidget(tmpstore)
                )
    schema = Schema()
    form = deform.Form(schema, buttons=('submit',))
    return render_form(form, success=tmpstore.clear)
