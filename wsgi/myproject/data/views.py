from django.shortcuts import render

# Create your views here.

import json

from django.http import HttpResponseRedirect, HttpResponse
from models import Process, ProcessMembership, SubProcess, InputMembership, OutputMembership, InputSubstance, OutputSubstance
from django.template import RequestContext, loader, Context
from django.contrib import messages
from myproject import settings
from forms import ProcessForm, SubProcessForm, SubProcessFormSet, InputFormSet, OutputFormSet, InputForm, OutputForm
from django.core.context_processors import  csrf

from django.contrib.auth.decorators import login_required

from messenger.views import check_messages

from random import randint

# <<<<=========== HELPER FUNCTIONS ===========>>>> #

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# <<<<=========== PROCESSES ===========>>>> #

# Create your views here.
@login_required
def all_processes(request):

    args={}
    # <<<=== CHECK FOR MESSAGES ===>>> #
    if request.user.is_authenticated():
        myMessages = check_messages(request.user)
        args.update(myMessages)
    # <<<==========================>>> #

    processes = Process.objects.filter(owner=request.user)
    print processes

    args['processes']=processes

    return render(request, 'processes.html', args)

@login_required
def create_edit_process(request, process_id=None):

    if request.method == 'POST':
        if process_id != None:
            process = Process.objects.get(id=process_id)
            form = ProcessForm(request.POST, instance = process)
            formset = SubProcessFormSet(request.POST, request.FILES, instance = process)
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                messages.success(request, "Process updated")
            else:
                messages.add_message(request,
                                    settings.DISALLOWED_MESSAGE,
                                    "Hold on, somethings not right there...")
                return render(request, 'create_edit_process.html', {'form': form, 'formset': formset, 'process':process})
            return HttpResponseRedirect('/data/process/all')
        else:
            form = ProcessForm(request.POST)
            formset = SubProcessFormSet(request.POST, request.FILES)

            if form.is_valid():
                new_process = form.save()
                messages.success(request, "Process added - you can now add subprocesses")
            else:
                messages.add_message(request,
                                    settings.DISALLOWED_MESSAGE,
                                    "Hold on, somethings not right there...")
                return render(request,'create_edit_process.html', {'form': form})

            return HttpResponseRedirect('/data/process/edit/' + str(new_process.id))
    else:

        args ={}
        args.update(csrf(request))

        if process_id is None:
            form = ProcessForm(initial = {'owner': request.user})
            spformset = SubProcessFormSet()
        else:
            process_instance = Process.objects.get(id=process_id)
            if process_instance.user_can_edit(request.user):
                args['process']=process_instance
                form = ProcessForm(instance = process_instance)
                spformset = SubProcessFormSet(instance=process_instance)
            else:
                messages.add_message(request,
                                    settings.DISALLOWED_MESSAGE,
                                    "Sorry, you don't have access to that...")
                return HttpResponseRedirect('/data/process/all/')

        args['form'] = form
        args['formset'] = spformset
        return render(request, 'create_edit_process.html', args)


@login_required
def delete_process(request,process_id):
    process_to_go = Process.objects.get(id=process_id)
    name = process_to_go.name
    process_to_go.delete()
    messages.success(request, name + ' deleted')
    return HttpResponseRedirect('/data/process/all/')



# <<<<=========== SUBPROCESSES ===========>>>> #


@login_required
def all_subprocesses(request):

    args={}
    # <<<=== CHECK FOR MESSAGES ===>>> #
    if request.user.is_authenticated():
        myMessages = check_messages(request.user)
        args.update(myMessages)
    # <<<==========================>>> #

    subprocesses = SubProcess.objects.order_by('category')

    args['subprocesses']=subprocesses

    return render(request, 'subprocesses.html', args)

@login_required
def create_edit_subprocess(request, subprocess_id=None):
    if request.method == 'POST':

        if subprocess_id != None:
            subprocess = SubProcess.objects.get(id=subprocess_id)
            form = SubProcessForm(request.POST, instance = subprocess)
            inputformset = InputFormSet(request.POST, request.FILES, instance = subprocess)
            outputformset = OutputFormSet(request.POST, request.FILES, instance = subprocess)
            if form.is_valid() and inputformset.is_valid() and outputformset.is_valid():
                form.save()
                inputformset.save()
                outputformset.save()
                messages.success(request, "Subprocess updated")
            else:
                messages.add_message(request,
                                    settings.DISALLOWED_MESSAGE,
                                    "Hold on, somethings not right there...")
                return render(request, 'create_edit_subprocess.html', {'form': form, 'inputformset': inputformset, 'outputformset': outputformset, 'subprocess':subprocess})
            return HttpResponseRedirect('/data/subprocess/all')
        else:
            form = SubProcessForm(request.POST)

            if form.is_valid():
                new_subprocess = form.save()
                messages.success(request, "Subprocess added - you can now add inputs and outputs")
            else:
                messages.add_message(request,
                                    settings.DISALLOWED_MESSAGE,
                                    "Hold on, somethings not right there...")
                return render(request,'create_edit_subprocess.html', {'form': form})

            return HttpResponseRedirect('/data/subprocess/edit/' + str(new_subprocess.id))
    else:

        args ={}
        args.update(csrf(request))

        if subprocess_id is None:
            form = SubProcessForm(initial = {'author': request.user})
            inputformset = InputFormSet()
            outputformset = OutputFormSet()
        else:
            subprocess_instance = SubProcess.objects.get(id=subprocess_id)
            args['subprocess']=subprocess_instance
            form = SubProcessForm(instance = subprocess_instance)
            inputformset = InputFormSet(instance=subprocess_instance)
            outputformset = OutputFormSet(instance=subprocess_instance)
            if request.user != subprocess_instance.author:
                args['readonly']=True

        args['form'] = form
        args['inputformset'] = inputformset
        args['outputformset'] = outputformset

        return render(request, 'create_edit_subprocess.html', args)

@login_required
def delete_subprocess(request,subprocess_id):
    subprocess_to_go = SubProcess.objects.get(id=subprocess_id)
    name = subprocess_to_go.name
    subprocess_to_go.delete()
    messages.success(request, name + ' deleted')
    return HttpResponseRedirect('/data/subprocess/all/')


@login_required
def duplicate_subprocess(request, subprocess_id):
    subprocess = SubProcess.objects.get(id=subprocess_id)
    duplicate = SubProcess(name = subprocess.name, unit = subprocess.unit, category = subprocess.category)
    duplicate.author = request.user
    duplicate.name += " (%s's copy)" % request.user.first_name
    duplicate.save()

    for inputset in subprocess.inputmembership_set.all():
        inputset.pk = None
        inputset.subprocess_id = duplicate.id
        inputset.save()

    for outputset in subprocess.outputmembership_set.all():
        outputset.pk = None
        outputset.subprocess_id = duplicate.id
        outputset.save()

    messages.success(request, 'Duplicate created')
    return HttpResponseRedirect('/data/subprocess/edit/%s' % duplicate.id)



# <<<<=========== INPUTS ===========>>>> #


@login_required
def all_inputs(request):

    args={}
    # <<<=== CHECK FOR MESSAGES ===>>> #
    if request.user.is_authenticated():
        myMessages = check_messages(request.user)
        args.update(myMessages)
    # <<<==========================>>> #

    inputs = InputSubstance.objects.order_by('name')


    args['inputs']=inputs

    return render(request, 'inputs.html', args)

@login_required
def create_edit_input(request, input_id=None):

    if request.method == 'POST':
        if input_id != None:
            thisinput = InputSubstance.objects.get(id=input_id)
            form = InputForm(request.POST, instance = thisinput)
            if form.is_valid():
                form.save()
                messages.success(request, "Input updated")
            else:
                messages.add_message(request,
                                    settings.DISALLOWED_MESSAGE,
                                    "Hold on, somethings not right there...")
                return render(request, 'create_edit_input.html', {'form': form, 'input':thisinput})
            return HttpResponseRedirect('/data/input/all')
        else:
            form = InputForm(request.POST)

            if form.is_valid():
                new_input = form.save()
                messages.success(request, "Input added")
            else:
                messages.add_message(request,
                                    settings.DISALLOWED_MESSAGE,
                                    "Hold on, somethings not right there...")
                return render(request,'create_edit_input.html', {'form': form})

            return HttpResponseRedirect('/data/input/all/')
    else:

        args ={}
        args.update(csrf(request))

        if input_id is None:
            form = InputForm()
        else:
            input_instance = InputSubstance.objects.get(id=input_id)
            args['input']=input_instance
            form = InputForm(instance = input_instance)

        args['form'] = form

        return render(request, 'create_edit_input.html', args)

@login_required
def delete_input(request,input_id):
    input_to_go = InputSubstance.objects.get(id=input_id)
    name = input_to_go.name
    input_to_go.delete()
    messages.success(request, name + ' deleted')
    return HttpResponseRedirect('/data/input/all/')


# <<<<=========== OUTPUTS ===========>>>> #


@login_required
def all_outputs(request):

    args={}

    # <<<=== CHECK FOR MESSAGES ===>>> #
    if request.user.is_authenticated():
        myMessages = check_messages(request.user)
        args.update(myMessages)
    # <<<==========================>>> #

    outputs = OutputSubstance.objects.order_by('name')



    args['outputs']=outputs

    return render(request, 'outputs.html', args)

@login_required
def create_edit_output(request, output_id=None):

    if request.method == 'POST':
        if output_id != None:
            output = OutputSubstance.objects.get(id=output_id)
            form = OutputForm(request.POST, instance = output)

            if form.is_valid():
                form.save()
                messages.success(request, "Output updated")
            else:
                messages.add_message(request,
                                    settings.DISALLOWED_MESSAGE,
                                    "Hold on, somethings not right there...")
                return render(request, 'create_edit_output.html', {'form': form, 'output':output})
            return HttpResponseRedirect('/data/output/all')
        else:
            form = OutputForm(request.POST)

            if form.is_valid():
                new_output = form.save()
                messages.success(request, "Output added")
            else:
                messages.add_message(request,
                                    settings.DISALLOWED_MESSAGE,
                                    "Hold on, somethings not right there...")
                return render(request,'create_edit_output.html', {'form': form})

            return HttpResponseRedirect('/data/output/all/')
    else:

        args ={}
        args.update(csrf(request))

        if output_id is None:
            form = OutputForm()
        else:
            output_instance = OutputSubstance.objects.get(id=output_id)
            args['output']=output_instance
            form = OutputForm(instance = output_instance)

        args['form'] = form

        return render(request, 'create_edit_output.html', args)

@login_required
def delete_output(request,output_id):
    output_to_go = OutputSubstance.objects.get(id=output_id)
    name = output_to_go.name
    output_to_go.delete()
    messages.success(request, name + ' deleted')
    return HttpResponseRedirect('/data/output/all/')

# <<<<<<  MODEL  >>>>>> #

def get_LCI(request, process_id):

# This is the new 'development version' which includes the tree

    args = get_LCI_data(process_id)

    return render(request,'lci.html',args)

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


def get_LCI_data(process_id):

    response = {}
    LCI = {}
    LCI_Tree={}

    process = Process.objects.get(id=process_id)

    print process.subprocesses.all()

    response['process']=process

    LCI_Tree.update({'name':process.name, 'children':[], 'level':1})

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
