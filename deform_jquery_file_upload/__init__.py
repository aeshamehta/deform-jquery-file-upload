from pkg_resources import resource_filename
import random

from colander import null

import deform
from deform.compat import uppercase, string
from deform.widget import FileUploadWidget, filedict


def includeme(config, deform=deform):
    """Call this function to enable the widget (more precisely,
    register the widget templates) or add "deform_jquery_file_upload" in
    the ``pyramid.includes`` directive of your Pyramid configuration
    file.

    The ``deform`` argument should only be used in tests.
    """
    search_path = list(deform.Form.default_renderer.loader.search_path)
    path = resource_filename('deform_jquery_file_upload', 'templates')
    search_path.append(path)
    deform.Form.default_renderer.loader.search_path = search_path


class JqueryFileUploadWidget(FileUploadWidget):
    """
    Represent a file upload.  Meant to work with a
    :class:`deform.FileData` schema node.

    This widget accepts a single required positional argument in its
    constructor: ``tmpstore``.  This argument should be passed an
    instance of an object that implements the
    :class:`deform.interfaces.FileUploadTempStore` interface.  Such an
    instance will hold on to file upload data during the validation
    process, so the user doesn't need to reupload files if other parts
    of the form rendering fail validation.  See also
    :class:`deform.interfaces.FileUploadTempStore`.

    **Attributes/Arguments**

    template
        The template name used to render the widget.  Default:
        ``file_upload``.

    readonly_template
        The template name used to render the widget in read-only mode.
        Default: ``readonly/file_upload``.

    size
        The ``size`` attribute of the input field (default ``None``).
    """
    template = 'jquery_file_upload'
    readonly_template = 'readonly/jquery_file_upload'
    size = None
    requirements = ( ('jquery', '1.8.3'), )

    def __init__(self, tmpstore, **kw):
        FileUploadWidget.__init__(self, **kw)
        self.tmpstore = tmpstore

    def random_id(self):
        return ''.join(
            [random.choice(uppercase+string.digits) for i in range(10)])

    def serialize(self, field, cstruct, **kw):
        if cstruct in (null, None):
            cstruct = {}
        if cstruct:
            uid = cstruct['uid']
            if not uid in self.tmpstore:
                self.tmpstore[uid] = cstruct

        readonly = kw.get('readonly', self.readonly)
        template = readonly and self.readonly_template or self.template
        values = self.get_template_values(field, cstruct, kw)
        return field.renderer(template, **values)

    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null

        upload = pstruct.get('upload')
        uid = pstruct.get('uid')

        if hasattr(upload, 'file'):
            # the upload control had a file selected
            data = filedict()
            data['fp'] = upload.file
            filename = upload.filename
            # sanitize IE whole-path filenames
            filename = filename[filename.rfind('\\')+1:].strip()
            data['filename'] = filename
            data['mimetype'] = upload.type
            data['size']  = upload.length
            if uid is None:
                # no previous file exists
                while 1:
                    uid = self.random_id()
                    if self.tmpstore.get(uid) is None:
                        data['uid'] = uid
                        self.tmpstore[uid] = data
                        preview_url = self.tmpstore.preview_url(uid)
                        self.tmpstore[uid]['preview_url'] = preview_url
                        break
            else:
                # a previous file exists
                data['uid'] = uid
                self.tmpstore[uid] = data
                preview_url = self.tmpstore.preview_url(uid)
                self.tmpstore[uid]['preview_url'] = preview_url
        else:
            # the upload control had no file selected
            if uid is None:
                # no previous file exists
                return null
            else:
                # a previous file should exist
                data = self.tmpstore.get(uid)
                # but if it doesn't, don't blow up
                if data is None:
                    return null

        return data
    """
    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (null, None):
            cstruct = ''
        options = {}
        if not self.delay:
            # set default delay if None
            options['delay'] = (
                isinstance(self.values, string_types) and 400) or 10
        options['minLength'] = self.min_length
        options = json.dumps(options)
        values = json.dumps(self.values)
        template = readonly and self.readonly_template or self.template
        visible_cstruct = self.display_value(field, cstruct)
        return field.renderer(template,
                              cstruct=cstruct,  # hidden field
                              visible_cstruct=visible_cstruct,
                              field=field,
                              options=options,
                              values=values)


    def deserialize(self, field, pstruct):
        if pstruct is null:
            return null
        return pstruct.get(field.name) or null
    """
