from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
import flowdata.models as m
import flowdata.forms as f
from django.core.context_processors import  csrf

from messenger.views import check_messages
from messenger.models import InternalMessage

from django.contrib.auth.decorators import login_required

# <<<<=========== PROCESSES ===========>>>> #

# Create your views here.
@login_required
def all_systems(request):

    args={}
    # <<<=== CHECK FOR MESSAGES ===>>> #
    if request.user.is_authenticated():
        myMessages = check_messages(request.user)
        args.update(myMessages)
    # <<<==========================>>> #

    systems = m.FlowSystem.objects.filter(owner=request.user)

    args['systems']=systems

    return render(request, 'systems.html', args)


#<=============================== SYSTEMS =====================================>

def newSystem(request):

    args={}

    return render(request, 'newSystem.html', args)

def createSystem(request):
    systemName = request.POST['systemName']
    newSystem = m.FlowSystem(name=systemName, owner = request.user)
    newSystem.save()

    newProcess = m.FlowTransformation(name = "%s First process (click to edit)" % systemName, author = request.user)
    newProcess.save()
    newProcess.partOfSystem.add(newSystem)
    newProcess.save()

    BRdefault = m.FlowInputSubstance.objects.get(name="Bauxite Residue Slurry")

    newInput = m.FlowInputMembership(transformation = newProcess,inputsubstance = BRdefault, amount_required = 1000, partOfSystem = newSystem, note = 'Default input of 1000 kg Bauxite residue')

    newInput.save()

    return setSystem(request, newSystem.id)


def chooseSystem(request):
    args={}
    systems = m.FlowSystem.objects.all()
    args['systems']=systems

    return render(request, 'chooseSystem.html', args)

def setSystem(request,system_id):
    #systemInfo = request.POST['system'].split("|")
    #print systemInfo
    system = m.FlowSystem.objects.get(id=system_id)
    request.session['currentSystemName']=system.name
    request.session['currentSystemID']=system_id#systemInfo[0]
    return HttpResponseRedirect('/flow/scan/')

def deleteSystem(request, system_id):
    thisSystem = m.FlowSystem.objects.get(id=system_id)
    thisSystem.delete()
    return HttpResponseRedirect('/flow/systems/')

#<=============================================================================>

def scantree(system_id):


    system  = m.FlowSystem.objects.get(id=system_id)

    processList = {} #initialise the process list output
    processNames, techOutputNames = {}, {}

    for checknum,process in enumerate(m.FlowTransformation.objects.all()): # for each process, set up the blank keys for inputs/outputs/tech inputs/tech outputs



        processList[process]={}
        processList[process]['Inputs']=[]
        processList[process]['Outputs']=[]
        processList[process]['Technosphere Inputs']=[]
        processList[process]['Technosphere Outputs']=[]
        inSystem = False # set inSystem to false to begin with

        for i in process.inputflows.all().distinct():
            input_meta = i.flowinputmembership_set.filter(transformation = process).filter(partOfSystem = system) # filter the flows by system and process
            #print input_meta
            for j in input_meta:
                processList[process]['Inputs'].append([i,j]) # append each input to the list
                inSystem = True # set the system flag to be true

        for i in process.outputflows.all().distinct():

            input_meta = i.flowoutputmembership_set.filter(transformation = process).filter(partOfSystem = system)

            #print input_meta
            for j in input_meta:
                processList[process]['Outputs'].append([i,j])
                inSystem = True

        for cn2, i in enumerate(process.technosphereInputs.all().distinct()):
            input_meta = i.flowtechnospheremembershipinput_set.filter(transformation = process).filter(partOfSystem = system)
            for j in input_meta:
                processList[process]['Technosphere Inputs'].append([i,j])
                inSystem = True

        for i in process.technosphereOutputs.all().distinct():

            input_meta = i.flowtechnospheremembershipoutput_set.filter(transformation = process).filter(partOfSystem = system)

            #print input_meta
            for j in input_meta:
                #print j
                processList[process]['Technosphere Outputs'].append([i,j])
                techOutputNames.update({i.id:i.name})
                inSystem = True

        inSystemExplicit = system in process.partOfSystem.all()

        if inSystemExplicit == False and inSystem == False: # if none of the flags have been set, pop the process
            processList.pop(process,None)
        else:
            processNames.update({process.id:process.name})

    #print processList
    return processList, processNames, techOutputNames

def getDotString(processList, system_id):

    system  = m.FlowSystem.objects.get(id=system_id)
    # to switch orientation add rankdir=LR; between '{' and 'node'
    dotString = 'digraph "%s" {splines=ortho;bgcolor=white;ranksep = "1";node [fontname="Quicksand" fontsize=12 margin="0.3,0.055" style=filled shape=box]; edge [fontname="Quicksand" fontsize=12 color=Gray]' % system.name
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

def systemScan(request):

    args = {}
    system_id = int(request.session['currentSystemID'])
    system = m.FlowSystem.objects.get(id=system_id)
    processList, processNames, techOutputNames  = scantree(system_id)

    args['processList']=processList
    args['processNames'] = processNames
    args['techOutputNames'] = techOutputNames
    print processList, processNames, techOutputNames
    args['dotString'] = getDotString(processList, system_id)
    args['system'] = system

    #print request.session['currentSystemName']

    return render(request, 'processList.html', args)


def parseAction(request, action_id, item_type, item_name, item_id):
    print "Action ID : %s" % action_id
    print "Item type : %s" % item_type
    print "Item name : %s" % item_name
    print "Item ID : %s" % item_id

    if action_id == "Delete":
        if item_type == "Input":
            return deleteInput(item_id)
        elif item_type == "Output":
            return deleteOutput(item_id)
        elif item_type == "Process":
            return deleteProcess(request, item_id)
        elif item_type == "TechInput":
            return deleteTechInput(item_id)
        elif item_type == "TechOutput":
            return deleteTechOutput(item_id)

    elif action_id == "Edit_amount":
        if item_type == "Input":
            return editInputSetup(request,item_id)
        elif item_type == "Output":
            return editOutputSetup(request,item_id)

    elif action_id =="Add_input":
        return addInputSetup(request, item_id)
    elif action_id =="Add_output":
        return addOutputSetup(request, item_id)
    elif action_id == "Add_Tech_Output":
        return addTechOutputSetup(request, item_id)

    elif action_id == "linkProcess":
        return linkProcessSetup(request,item_id)

    elif action_id == "addProcess":
        return createProcessSetup(request)
    elif action_id == "Edit_process":
        return  editProcessSetup(request, item_id)

    else:
        print 'No command found'
        return HttpResponseRedirect('/flow/scan/')



def deleteInput(item_id):
    i = m.FlowInputMembership.objects.get(id=item_id)
    i.delete()
    return HttpResponseRedirect('/flow/scan/')

def deleteOutput(item_id):
    i = m.FlowOutputMembership.objects.get(id=item_id)
    i.delete()
    return HttpResponseRedirect('/flow/scan/')

def deleteTechInput(item_id):
    i = m.FlowTechnosphereMembershipInput.objects.get(id=item_id)
    i.delete()
    return HttpResponseRedirect('/flow/scan/')

def deleteTechOutput(item_id):
    i = m.FlowTechnosphereMembershipOutput.objects.get(id=item_id)
    i.delete()
    return HttpResponseRedirect('/flow/scan/')

def deleteProcess(request, item_id):
    system_id = request.session['currentSystemID']
    system = m.FlowSystem.objects.get(id=system_id)
    i = m.FlowTransformation.objects.get(id=item_id)

    for j in i.flowinputmembership_set.all():
        if j.partOfSystem == system:
            print "Deleting %s" % j
            j.delete()

    for j in i.flowoutputmembership_set.all():
        if j.partOfSystem == system:
            print "Deleting %s" % j
            j.delete()

    for j in i.flowtechnospheremembershipinput_set.all():
        if j.partOfSystem == system:
            print "Deleting %s" % j
            j.delete()

    for j in i.flowtechnospheremembershipoutput_set.all():
        if j.partOfSystem == system:
            print "Deleting %s" % j
            j.delete()

    i.partOfSystem.remove(system)

    return HttpResponseRedirect('/flow/scan/')

def createProcessSetup(request):

    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))
    args = {}
    args.update(csrf(request))

    form = f.CreateTransformationForm(initial = {'partOfSystem':[system], 'author':request.user})

    args['form'] = form
    args['action']="add"
    args['type'] = "Process"

    #processList = getSingleProcess(item_id,system.id)
    #args['processList']=processList
    #args['dotString'] = getDotString(processList,system.id)

    return render(request, 'addEditProcess.html', args)
    return HttpResponseRedirect('/flow/scan/')

def editProcessSetup(request, item_id):

    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))
    item = m.FlowTransformation.objects.get(id=item_id)
    args = {}
    args.update(csrf(request))
    form = f.CreateTransformationForm(instance=item)
    args['form'] = form
    args['action']="edit"
    args['type'] = "Process"
    args['editID'] = item.id

    #processList = getSingleProcess(process.id,system.id)
    #args['processList']=processList
    #args['dotString'] = getDotString(processList,system.id)

    return render(request, 'addEditProcess.html', args)

def addProcessConfirm(request):
    if request.method == 'POST':
        form = f.CreateTransformationForm(request.POST)
        sendTo = request.POST['sendTo']
        if form.is_valid():
            newitem=form.save()
        else:
            print request.POST
            print form.errors
            print 'Form Not Saved'
    return HttpResponseRedirect("%s?i=%s" % (sendTo, newitem.id))


def editProcessConfirm(request, edit_id):
    if request.method == 'POST':
        item = m.FlowTransformation.objects.get(id=edit_id)
        form = f.CreateTransformationForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        else:
            print request.POST
            print form.errors
            print 'Form Not Saved'
    return HttpResponseRedirect('/flow/scan/')

# <-- Inputs -->

def addInputSetup(request, item_id):

    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))
    process = m.FlowTransformation.objects.get(id=item_id)
    ###<<<< CHECK THIS BIT!!!>>>>###
    args = {}
    args.update(csrf(request))
    form = f.AddInputForm(initial = {'partOfSystem':system, 'transformation':process})

    if 'i' in request.GET:
        item = m.FlowInputSubstance.objects.get(id=request.GET['i'])
        form.fields['inputsubstance'].initial = item

    args['form'] = form
    args['action']="add"
    args['type'] = "Input"

    dropDown = m.FlowInputSubstance.objects.all()
    args['dropDown'] = dropDown

    processList = getSingleProcess(item_id,system.id)
    args['processList']=processList
    args['dotString'] = getDotString(processList,system.id)

    return render(request, 'addIO.html', args)

def addInputConfirm(request):
    if request.method == 'POST':
        form = f.AddInputForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect('/flow/scan/')

def editInputSetup(request, item_id):

    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))
    item=m.FlowInputMembership.objects.get(id=item_id)
    process = item.transformation

    args = {}
    args.update(csrf(request))
    form = f.AddInputForm(instance=item)
    args['form'] = form
    args['action']="edit"
    args['type'] = "Input"
    args['editID'] = item.id

    dropDown = m.FlowInputSubstance.objects.all()
    args['dropDown'] = dropDown

    processList = getSingleProcess(process.id,system.id)
    args['processList']=processList
    args['dotString'] = getDotString(processList,system.id)

    return render(request, 'addIO.html', args)

def editInputConfirm(request,edit_id):
    if request.method == 'POST':
        item = m.FlowInputMembership.objects.get(id=edit_id)
        form = f.AddInputForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect('/flow/scan/')

# <-- Outputs -->

def addOutputSetup(request, item_id):

    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))
    process = m.FlowTransformation.objects.get(id=item_id)



    args = {}
    args.update(csrf(request))
    form = f.AddOutputForm(initial = {'partOfSystem':system, 'transformation':process})

    if 'i' in request.GET:
        item = m.FlowInputSubstance.objects.get(id=request.GET['i'])
        form.fields['outputsubstance'].initial = item

    args['form'] = form
    args['action']="add"
    args['type'] = "Output"

    dropDown = m.FlowOutputSubstance.objects.all()
    args['dropDown'] = dropDown

    processList = getSingleProcess(item_id,system.id)
    args['processList']=processList
    args['dotString'] = getDotString(processList,system.id)

    return render(request, 'addIO.html', args)

def addOutputConfirm(request):
    if request.method == 'POST':
        form = f.AddOutputForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect('/flow/scan/')

def editOutputSetup(request, item_id):

    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))
    item=m.FlowOutputMembership.objects.get(id=item_id)
    process = item.transformation

    args = {}
    args.update(csrf(request))
    form = f.AddOutputForm(instance=item)
    args['form'] = form
    args['action']="edit"
    args['type'] = "Output"
    args['editID'] = item.id

    dropDown = m.FlowOutputSubstance.objects.all()
    args['dropDown'] = dropDown

    processList = getSingleProcess(process.id,system.id)
    args['processList']=processList
    args['dotString'] = getDotString(processList,system.id)

    return render(request, 'addIO.html', args)

def editOutputConfirm(request,edit_id):

    if request.method == 'POST':
        item = m.FlowOutputMembership.objects.get(id=edit_id)
        form = f.AddOutputForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect('/flow/scan/')



#<-- Technosphere Outputs -->

def addTechOutputSetup(request, item_id):

    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))
    process = m.FlowTransformation.objects.get(id=item_id)

    args = {}
    args.update(csrf(request))
    form = f.AddTechOutputForm(initial = {'partOfSystem':system, 'transformation':process})

    if 'i' in request.GET:
        print "Found the GET"
        item = m.FlowTechnosphere.objects.get(id=request.GET['i'])
        form.fields['techFlow'].initial = item

    args['form'] = form
    args['action']="add"
    args['type'] = "TechOutput"

    dropDown = m.FlowTechnosphere.objects.all()
    args['dropDown'] = dropDown

    processList = getSingleProcess(item_id,system.id)
    args['processList']=processList
    args['dotString'] = getDotString(processList,system.id)



    return render(request, 'addIO.html', args)

def addTechOutputConfirm(request):
    if request.method == 'POST':
        form = f.AddTechOutputForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect('/flow/scan/')

#<-- Helpers -->

def getSingleProcess(item_id, system_id):

    system  = m.FlowSystem.objects.get(id=system_id)
    processList = {} #initialise the process list output

    process = m.FlowTransformation.objects.get(id=item_id) # for each process, set up the blank keys for inputs/outputs/tech inputs/tech outputs

    processList[process]={}
    processList[process]['Inputs']=[]
    processList[process]['Outputs']=[]
    processList[process]['Technosphere Inputs']=[]
    processList[process]['Technosphere Outputs']=[]

    for i in process.inputflows.all().distinct():
        input_meta = i.flowinputmembership_set.filter(transformation = process).filter(partOfSystem = system).distinct() # filter the flows by system and process
        for j in input_meta:
            processList[process]['Inputs'].append([i,j]) # append each input to the list
            inSystem = True # set the system flag to be true

    for i in process.outputflows.all().distinct():

        input_meta = i.flowoutputmembership_set.filter(transformation = process).filter(partOfSystem = system).distinct()

        #print input_meta
        for j in input_meta:
            processList[process]['Outputs'].append([i,j])
            inSystem = True

    for i in process.technosphereInputs.all().distinct():
        input_meta = i.flowtechnospheremembershipinput_set.filter(transformation = process).filter(partOfSystem = system).distinct()
        #print input_meta
        for j in input_meta:
            processList[process]['Technosphere Inputs'].append([i,j])
            inSystem = True

    for i in process.technosphereOutputs.all().distinct():

        input_meta = i.flowtechnospheremembershipoutput_set.filter(transformation = process).filter(partOfSystem = system).distinct()

        #print input_meta
        for j in input_meta:
            processList[process]['Technosphere Outputs'].append([i,j])
            inSystem = True

    return processList


#<----- CREATE THINGS ------>

def createTechFlowSetup(request):

    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))

    args = {}
    args.update(csrf(request))
    form = f.CreateTechFlowForm()
    args['form'] = form
    args['action']="create"
    args['type'] = "TechFlow"

    return render(request, 'createItem.html', args)

def createTechFlowConfirm(request):
    if request.method == 'POST':
        form = f.CreateTechFlowForm(request.POST)
        sendTo = request.POST['sendTo']
        if form.is_valid():
            newitem=form.save()

    return HttpResponseRedirect("%s?i=%s" % (sendTo, newitem.id))

def createInputSetup(request):

    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))

    args = {}
    args.update(csrf(request))
    form = f.CreateInputForm()
    args['form'] = form
    args['action']="create"
    args['type'] = "Input"

    return render(request, 'createItem.html', args)

def createInputConfirm(request):
    if request.method == 'POST':
        form = f.CreateInputForm(request.POST)
        sendTo = request.POST['sendTo']
        if form.is_valid():
            newitem=form.save()

    return HttpResponseRedirect("%s?i=%s" % (sendTo, newitem.id))

def createOutputSetup(request):

    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))

    args = {}
    args.update(csrf(request))
    form = f.CreateOutputForm()
    args['form'] = form
    args['action']="create"
    args['type'] = "Output"

    return render(request, 'createItem.html', args)

def createOutputConfirm(request):
    if request.method == 'POST':
        form = f.CreateOutputForm(request.POST)
        sendTo = request.POST['sendTo']
        if form.is_valid():
            newitem=form.save()

    return HttpResponseRedirect("%s?i=%s" % (sendTo, newitem.id))

def createSystemSetup(request):
    owner = request.user
    args={}
    args.update(csrf(request))
    form = f.CreateSystemForm()
    args['form']=form
    args['action'] = "create"
    args['type']="System"

    return render(request, 'createItem.html', args)

def createSystemConfirm(request):
    if request.method == 'POST':
        form = f.CreateSystemForm(request.POST)
        sendTo = request.POST['sendTo']
        if form.is_valid():
            newitem=form.save()

    return HttpResponseRedirect("%s?i=%s" % (sendTo, newitem.id))


def linkProcessSetup(request, item_id):
    system  = m.FlowSystem.objects.get(id=int(request.session['currentSystemID']))
    item = m.FlowTechnosphere.objects.get(id=item_id)
    print item
    args = {}
    args.update(csrf(request))
    form = f.AddTechInputForm(initial={'techFlow':item, 'partOfSystem':system})

    if 'i' in request.GET:
        print "Found the GET"
        olditem = m.FlowTransformation.objects.get(id=request.GET['i'])
        form.fields['transformation'].initial = olditem

    args['form'] = form
    args['action']="add"
    args['type'] = "TechInput"

    dropDown = m.FlowTransformation.objects.all()
    args['dropDown'] = dropDown

    lastLink = 0
    memberset =  m.FlowTechnosphereMembershipOutput.objects.filter(techFlow=item).filter(partOfSystem=system)
    for i in memberset:
        print i.transformation
        lastLink=i.transformation.id

    memberset2 = m.FlowTechnosphereMembershipInput.objects.filter(techFlow=item).filter(partOfSystem=system)
    for i in memberset2:
        print i.transformation
        if lastLink == 0:
            lastLink=i.transformation.id

    if lastLink != 0:
        processList = getSingleProcess(lastLink,system.id)
        args['processList']=processList
        args['dotString'] = getDotString(processList,system.id)

    print "go to linkProcess.html"
    return render(request, 'linkProcess.html', args)

def addTechInputConfirm(request):
    if request.method == 'POST':
        form = f.AddTechInputForm(request.POST)
        if form.is_valid():
            newitem=form.save()
        else:
            print form.errors
    return HttpResponseRedirect("/flow/scan")
