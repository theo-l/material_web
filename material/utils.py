# encoding:utf-8

from material.models import Material




def material_file_process(fd):
    import re

    title_line_found = False
    name_index = None
    type_index = None

    for line in fd:
        fields = re.split('[, \t]', line)
        if not any(fields):
            continue

        if not title_line_found:
            name_index, type_index = parse_material_title_index(fields)
            if all([name_index, type_index]):
                title_line_found = True
            else:
                return
        process_material_file_line(fields, name_index, type_index)


def parse_material_title_index(fields):

    name_index, type_index = (None, None)
	
    for (index, field_name) in enumerate(fields):
        if field_name == u'材料名称':
            name_index = index
        if field_name == u'型号':
            type_index = index


    return (name_index, type_index)



def process_material_file_line(fields, name_index, type_index):
    material = Material.new_(fields[name_index], fields[type_index])
    material.save()

class ProcessFormMixin(object):

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.pre_form_valid()
            return self.form_valid(form)
        else:
            self.pre_form_invalid()
            return self.form_invalid(form)

    def pre_form_valid(self):
        pass

    def pre_form_invalid(self):
        pass