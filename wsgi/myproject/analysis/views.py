from django.shortcuts import render
import flowdata.models as m
from flowdata.views import scantree
import json
# Create your views here.


# <<<<<<  MODEL  >>>>>> #

def get_System_LCI_data(system_id):

    response = {}
    LCI = {}
    barData=[]

    system = m.FlowSystem.objects.get(id=system_id)

    processList = scantree(system_id)

    #processText ='<table class="table">\n\t\t<th>ProcessName</th>\t<th>Inputs</th>\t<th>Outputs</th>\t<th>Technosphere Inputs</th>\t<th>Technosphere Outputs</th>\t<th>Impact</th>\n'
    processText ='<table class="table">\n\t\t<tr><th>Process Name</th>\t<th>Carbon Footprint<br>(kg CO<sub>2</sub>-eq)</th></tr>\n'

    textInputs = "<p>"
    textOutputs = "<p>"
    textTechInputs = "<p>"
    textTechOutputs = "<p>"

    allInputs = {}
    allOutputs = {}
    allTechInputs = {}
    allTechOutputs = {}
    techCheck = {}

    fullImpactData = {}
    impactByProcess = {}

    processImpact = 0

    for j, process in enumerate(processList):

        processImpact = 0

        textInputs = "</p><p>".join(["%s (%d %s)" % (i[0].name, i[1].amount_required, i[0].unit) for i in processList[process]['Inputs']])
        textInputs += "</p>"

        for i in processList[process]['Inputs']:
            allInputs.setdefault(i[0].name, []).append(i[1].amount_required)

            fullImpactData.setdefault(i[0].name, {'amounts':[], 'EF':0, 'simaPro_id':"", 'total_amount':0, 'total_footprint':0})
            fullImpactData[i[0].name]['amounts'].append(i[1].amount_required)
            fullImpactData[i[0].name]['EF'] = i[0].emission_factor
            fullImpactData[i[0].name]['simaPro_id'] = i[0].simaPro_id
            fullImpactData[i[0].name]['total_amount'] += i[1].amount_required
            fullImpactData[i[0].name]['total_footprint'] = fullImpactData[i[0].name]['total_amount'] * fullImpactData[i[0].name]['EF']

            processImpact += i[1].amount_required * i[0].emission_factor

            impactByProcess.setdefault(process.name,{}).update({i[0].name:fullImpactData[i[0].name]})

        textOutputs = "</p><p>".join(["%s (%d %s)" % (i[0].name, i[1].amount_required, i[0].unit) for i in processList[process]['Outputs']])
        textOutputs += "</p>"

        for i in processList[process]['Outputs']:
            allOutputs.setdefault(i[0].name, []).append(i[1].amount_required)

            fullImpactData.setdefault(i[0].name, {'amounts':[], 'EF':0, 'simaPro_id':"", 'total_amount':0, 'total_footprint':0})
            fullImpactData[i[0].name]['amounts'].append(i[1].amount_required)
            fullImpactData[i[0].name]['EF'] = i[0].emission_factor
            fullImpactData[i[0].name]['simaPro_id'] = i[0].simaPro_id
            fullImpactData[i[0].name]['total_amount'] += i[1].amount_required
            fullImpactData[i[0].name]['total_footprint'] = fullImpactData[i[0].name]['total_amount'] * fullImpactData[i[0].name]['EF']

            processImpact += i[1].amount_required * i[0].emission_factor

            impactByProcess.setdefault(process.name,{}).update({i[0].name:fullImpactData[i[0].name]})

        textTechInputs = "</p><p>".join(["%s (%d %s)" % (i[0].name, i[1].amount_required, i[0].unit) for i in processList[process]['Technosphere Inputs']])
        textTechInputs += "</p>"

        for i in processList[process]['Technosphere Inputs']:
            allTechInputs.setdefault(i[0].name, []).append(i[1].amount_required)
            techCheck.setdefault(i[0].name, []).append(i[1].amount_required*-1)

        textTechOutputs = "</p><p>".join(["%s (%d %s)" % (i[0].name, i[1].amount_required, i[0].unit) for i in processList[process]['Technosphere Outputs']])
        textTechOutputs += "</p>"

        for i in processList[process]['Technosphere Outputs']:
            allTechOutputs.setdefault(i[0].name, []).append(i[1].amount_required)
            techCheck.setdefault(i[0].name, []).append(i[1].amount_required)


        barData.append({'name':process.name, 'footprint':processImpact, 'order':j})

        #processText += "\t<tr>\n\t\t<td>%s</td>\t<td>%s</td>\t<td>%s</td>\t<td>%s</td>\t<td>%s</td>\t<td>%s</td>\n\t</tr>\n" % (process,  textInputs, textOutputs, textTechInputs, textTechOutputs, processImpact)
        processText += "\t<tr>\n\t\t<td>%s</td>\t<td>%s</td>\n\t</tr>\n" % (process.name,  processImpact)

    processText += '</table>'

    techWarnings = {}

    for i in techCheck:
        if sum(techCheck[i])!= 0:
            techWarnings.update({i:techCheck[i]})

    total_impact = sum([fullImpactData[i]['total_footprint'] for i in fullImpactData])

    response['LCI'] = processList
    response['processText'] = processText
    lists = []
    lists.append(allInputs)
    lists.append(allOutputs)
    lists.append(allTechInputs)
    lists.append(allTechOutputs)
    lists.append(techCheck)
    response['inputList'] = impactByProcess
    response['warnings'] = [fullImpactData[i]['total_footprint'] for i in fullImpactData]
    response['barData'] = json.dumps(barData)
    response['grand_total'] = total_impact

    return response

'''
    response['system']=system

    #LCI_Tree.update({'name':system.name, 'children':[], 'level':1})

    for i, subprocess in enumerate(process.subprocesses.all()):
        subprocess_meta =  subprocess.processmembership_set.get(process = process)
        print subprocess.name
        multiplier = subprocess_meta.amount_required
        LCI_Tree['children'].append({'name':subprocess.name, 'children':[], 'footprint':0, 'level':2, 'order':i})



        for thisinput in subprocess.inputs.all():
            input_meta = thisinput.inputmembership_set.get(subprocess = subprocess)
            print thisinput.name
            input_amount = input_meta.amount_required * multiplier
            print input_amount
            ef = thisinput.emission_factor

            LCI_Tree['children'][i]['children'].append({'name':thisinput.name, 'size':input_amount, 'footprint':input_amount * thisinput.emission_factor, 'level':3})
            LCI_Tree['children'][i]['footprint']+=input_amount*ef



            try:
                LCI[thisinput.name]['total_amount'] += input_amount
                LCI[thisinput.name]['total_footprint'] = LCI[thisinput.name]['total_amount'] * ef

            except KeyError:
                LCI[thisinput.name]={}
                LCI[thisinput.name]['total_amount'] = input_amount
                LCI[thisinput.name]['total_footprint'] = input_amount * ef
                LCI[thisinput.name]['simaPro_id'] = thisinput.simaPro_id
                LCI[thisinput.name]['unit'] = thisinput.unit

    grand_total = 0

    for item in LCI:
        print LCI[item]['total_footprint']
        grand_total += LCI[item]['total_footprint']

    response['grand_total']=grand_total

    LCI_Tree['footprint']=grand_total

    response['LCI'] = LCI
    print LCI

    response['LCI_Tree'] = json.dumps(LCI_Tree)

    return response

'''


def getDotString2(processList, system_id):

    system  = m.FlowSystem.objects.get(id=system_id)
    c = 1

    plist=[]

    #print processList

    for p in processList:
        plist.append(p)
        for i in processList[p]['Inputs']:
            dotString += '"%s|%s" -> "%s" [label="%s"]' % (i[0].name,i[1].id,p.name, str(i[1].amount_required) + " " + i[0].unit)
            dotString += '"%s|%s" [label="%s" id="input Input|%s|%s" width=0.5 height=0.25 shape=box style=filled]' % (i[0].name,i[1].id,i[0].name,i[0].name.replace(" ","_"), i[1].id)
            c+=1
        for i in processList[p]['Outputs']:
            dotString += '"%s" -> "%s|%s" [label="%s"]' % (p.name,i[0].name,i[1].id, str(i[1].amount_required) + " " + i[0].unit)
            dotString += '"%s|%s" [label="%s" id="output Output|%s|%s" width=0.5 height=0.25]' % (i[0].name,i[1].id,i[0].name,i[0].name.replace(" ","_"),i[1].id)
            c+=1
        for i in processList[p]['Technosphere Inputs']:
            dotString += '"%s" -> "%s" [label="%s"]' % (i[0].name,p.name, str(i[1].amount_required) + " " + i[0].unit)
            dotString += '"%s" [label="%s" id="intermediate TechInput|%s|%s" width=0.5 height=0.25]' % (i[0].name,i[0].name,i[0].name.replace(" ","_"),i[1].id)

        for i in processList[p]['Technosphere Outputs']:
            #print i[0].id
            dotString += '"%s" -> "%s" [label="%s"]' % (p.name, i[0].name, str(i[1].amount_required) + " " + i[0].unit)
            dotString += '"%s" [label="%s" id="intermediate TechOutput|%s|%s" width=0.5 height=0.25]' % (i[0].name,i[0].name,i[0].name.replace(" ","_"),i[0].id)#,i[1].id)

    for j, p in enumerate(plist):
        dotString += '"%s" [id="process Process|%s|%s" shape=box color=darkred style="rounded,filled" fontsize=12]' % (p.name, p.name.replace(" ","_"), p.id)


    dotString += '}'
    #print dotString
    return dotString




def get_System_LCI(request, system_id):

# This is the new 'development version' which includes the tree

    args = get_System_LCI_data(system_id)

    return render(request,'SystemLCI.html',args)

def output_csv(request, process_id):

    lci_dataset = get_LCI_data(process_id)
    process = lci_dataset['process']
    LCI = lci_dataset['LCI']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="SimaProOutput_Process_' + str(process.id) + '_' + process.name + '.csv"'

    identifier = random_with_N_digits(11)

    process_data ={'processname': process.output + ' from ' + process.name, 'unit': process.unit, 'output_amount':process.output_amount, 'identifier':identifier}

    lci_data=[]

    for item in LCI:

        lci_data.append({'simaPro_id': LCI[item]['simaPro_id'], 'unit': LCI[item]['unit'], 'amount_required':LCI[item]['total_amount'] })

    t = loader.get_template('csv_template.txt')
    c = Context({
        'process_data': process_data,
        'lci_data':lci_data,
    })

    response.write(t.render(c))

    return response
