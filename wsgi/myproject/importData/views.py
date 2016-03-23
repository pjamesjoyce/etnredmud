from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

import flowdata.models as m

from forms import DataUploadForm
from pprint import pprint

import json

# Create your views here.

def upload_file(request):
    args={}

    upload_form = DataUploadForm()

    args['upload_form'] = upload_form

    return render(request, 'upload_file.html', args)

def process_upload(request):

    if request.method == 'POST':
		uploaded_form = DataUploadForm(request.POST, request.FILES)

		if uploaded_form.is_valid():
			uploaded_form.save()

    data = []
    for i in range(1,7):
        print i
        data.append(xlsx(uploaded_form.cleaned_data.get('data_file'),i))

    args = {}
    input_substances = 0
    output_substances = 0
    techFlows = 0
    systems = 0
    transformations = 0
    inputflows = 0
    outputflows = 0
    techLinks = 0


    for i, d in enumerate(data[0]):  # Inputs/Outputs
        if i == 0:
            pass # skip the title row
        else:
            if d['A'] == "input":
                values = {'name' : d['B'], 'emission_factor' : d['C'], 'unit' : d['D'], 'simaPro_id' : d['E']}
                obj, created = m.FlowInputSubstance.objects.update_or_create(name=d['B'], defaults=values)
                input_substances += 1

            elif d['A']=="output":
                values = {'name' : d['B'], 'emission_factor' : d['C'], 'unit' : d['D'], 'simaPro_id' : d['E']}
                obj, created = m.FlowOutputSubstance.objects.update_or_create(name=d['B'], defaults=values)
                output_substances += 1



    for i, d in enumerate(data[1]):  # TechFlows
        if i == 0:
            pass # skip the title row
        else:
            if d['A'] == "techFlow":
                values = {'name' : d['B'], 'unit' : d['C']}
                obj, created = m.FlowTechnosphere.objects.update_or_create(name=d['B'], defaults=values)
                techFlows += 1

    for i, d in enumerate(data[2]):  # Systems
        if i == 0:
            pass # skip the title row
        else:
            if d['A'] == "system":
                thisUser = User.objects.get(username = d['B'])
                values = {'owner' : thisUser , 'name' : d['C']}
                obj, created = m.FlowSystem.objects.update_or_create(name=d['C'], defaults=values)
                systems += 1

    for i, d in enumerate(data[3]):  # Systems
        if i == 0:
            pass # skip the title row
        else:
            if d['A'] == "transformation":
                thisAuthor = User.objects.get(username = d['E'])
                thisSystem = m.FlowSystem.objects.get(name = d['F'])

                values = {'name' : d['B'], 'unit': d['C'], 'category' : d['D'], 'author':thisAuthor, 'uuid': d['G']}
                obj, created = m.FlowTransformation.objects.update_or_create(uuid=d['G'], defaults=values)
                obj.partOfSystem.add(thisSystem)
                transformations += 1

    for i, d in enumerate(data[4]):  # Systems
        if i == 0:
            pass # skip the title row
        else:
            if d['A'] == "input":
                thisSystem = m.FlowSystem.objects.get(name = d['F'])
                thisTransformation = m.FlowTransformation.objects.get(uuid = d['C'])
                thisSubstance = m.FlowInputSubstance.objects.get(name=d['D'])

                values = {'transformation' : thisTransformation, 'inputsubstance': thisSubstance, 'amount_required':d['E'], 'partOfSystem': thisSystem, 'note': d['G'], 'uuid': d['H']}
                obj, created = m.FlowInputMembership.objects.update_or_create(uuid=d['H'], defaults=values)

                inputflows += 1

            if d['A'] == "output":
                thisSystem = m.FlowSystem.objects.get(name = d['F'])
                thisTransformation = m.FlowTransformation.objects.get(uuid = d['C'])
                thisSubstance = m.FlowOutputSubstance.objects.get(name=d['D'])

                values = {'transformation' : thisTransformation, 'outputsubstance': thisSubstance, 'amount_required':d['E'], 'partOfSystem': thisSystem, 'note': d['G'], 'uuid': d['H']}
                obj, created = m.FlowOutputMembership.objects.update_or_create(uuid=d['H'], defaults=values)

                outputflows += 1

    for i, d in enumerate(data[5]):  # Systems
        if i == 0:
            pass # skip the title row
        else:
            if d['A'] == "techLink":
                print d['H']
                thisSystem = m.FlowSystem.objects.get(name = d['H'])
                thisTransformationFrom = m.FlowTransformation.objects.get(uuid = d['C'])
                thisTransformationTo = m.FlowTransformation.objects.get(uuid = d['E'])
                thisFlow = m.FlowTechnosphere.objects.get(name = d['F'])

                valuesAsOutput = {'transformation' : thisTransformationFrom, 'techFlow': thisFlow, 'amount_required':d['G'], 'partOfSystem': thisSystem, 'note': d['I'], 'uuid': d['J']}
                valuesAsInput = {'transformation' : thisTransformationTo, 'techFlow': thisFlow, 'amount_required':d['G'], 'partOfSystem': thisSystem, 'note': d['I'], 'uuid': d['J']}
                obj, created = m.FlowTechnosphereMembershipOutput.objects.update_or_create(uuid=d['H'], defaults=valuesAsOutput)
                obj, created = m.FlowTechnosphereMembershipInput.objects.update_or_create(uuid=d['H'], defaults=valuesAsInput)

                techLinks += 1

    args['input_substances'] = input_substances
    args['output_substances'] = output_substances
    args['techFlows'] = techFlows
    args['systems'] = systems
    args['transformations'] = transformations
    args['inputflows'] = inputflows
    args['outputflows'] = outputflows
    args['techLinks'] = techLinks

    return render(request,'upload_info.html',args)

def xlsx(fname, sheetNo):
    import zipfile
    from xml.etree.ElementTree import iterparse
    z = zipfile.ZipFile(fname)
    strings = [el.text for e, el in iterparse(z.open('xl/sharedStrings.xml')) if el.tag.endswith('}t')]
    rows = []
    row = {}
    value = ''
    for e, el in iterparse(z.open('xl/worksheets/sheet%s.xml' % sheetNo)):
        if el.tag.endswith('}v'): # <v>84</v>
            value = el.text
        if el.tag.endswith('}c'): # <c r="A3" t="s"><v>84</v></c>
            if el.attrib.get('t') == 's':
                value = strings[int(value)]
            letter = el.attrib['r'] # AZ22
            while letter[-1].isdigit():
                letter = letter[:-1]
            row[letter] = value
            value = ''
        if el.tag.endswith('}row'):
            rows.append(row)
            row = {}
    return rows
