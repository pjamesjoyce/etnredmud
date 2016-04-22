from django.shortcuts import render
from django.http import HttpResponse
from forms import BibDataUploadForm


# Create your views here.
def upload_file(request):
    args={}

    upload_form = BibDataUploadForm()

    args['upload_form'] = upload_form

    return render(request, 'bib_upload_file.html', args)


def process_upload(request):

    if request.method == 'POST':
        uploaded_form = BibDataUploadForm(request.POST, request.FILES)

        if uploaded_form.is_valid():
            uploaded_form.save()

        bibfile = uploaded_form.cleaned_data.get('data_file')

        bibname = '.'.join(bibfile.name.split('.')[:-1])
        bibextension = bibfile.name.split('.')[-1]

        if bibextension == "bib":
            data = convertBibToTxt(bibfile)
            response = HttpResponse(data, content_type='text/plain')
            response['Content-Disposition'] = 'attachment;filename="' + str(bibname)+ '.txt"'
        else:
            args={}

            upload_form = BibDataUploadForm()

            args['upload_form'] = upload_form
            args['prompts'] = 'Please choose a valid .bib file'

            response =  render(request, 'bib_upload_file.html', args)



        return response



def convertBibToTxt(file):
    info = []
    stream = 'Index\tTitle\tAuthors\tSource\tType\tdoi\n'
    itemdict = {}
    keepItems = ['author','title','pages','doi','journal','number','volume','year','url']
    i = 1



    #with open(file) as f:
    for line in file:
        #print line
        l = line.strip()

        if line[0]=="@": # this is a new item, set up the dictionary
            if itemdict != {}: # if there's something in the item info
                info.append(itemdict) # add it to the info list

            itemdict = {}   #reset the item

                                                            # strip the line break
            split = l.find("{")                                             # find the split between type and id
            itemType = l[1:split]                                           # store the type
            itemID = l[split+1:len(l)-1]                                    # store the id
            itemIndex = i                                                   # get the index
            i+=1                                                            # increment i
            itemdict = {'index': itemIndex,'type':itemType,'id':itemID}     # begin the new dict
        elif l[0] != '}' :
            ls = l.split("=")
            item = ls[0].strip()
            content = ls[1].strip()[:-1].replace('{','').replace('}','').replace('\\','').replace('--','-')
            if item in keepItems:
                itemdict.update({item : content})

    if itemdict != {}: # if there's something in the item info
        info.append(itemdict) # add it to the info list
    #print info

    for item in info:
        citation = ""
        if item['type'] == 'article':
            if 'journal' in item.keys():
                citation += item['journal'] + " "
            if 'volume' in item.keys():
                citation += item['volume']+ " "
            if 'number' in item.keys():
                citation += "(" + item['number'] + ") "
            if 'pages' in item.keys():
                citation += item['pages']
        else:
            citation = ""#item['type']

        if 'doi' in item.keys():
            doi = item['doi']
        else:
            doi = ''

        author = authorParse(item['author'])

        stream += '{}\t{}\t{}\t{}\t{}\t{}\n'.format(item['index'],item['title'],author,citation,item['type'],doi)

    return stream

def authorParse(authorList):

    sl = authorList.split(' ')
    andCount = sl.count('and')
    andCheck = 0

    for i,a in enumerate(sl):
        if a == 'and':
            andCheck+=1
            if andCheck!=andCount:
                sl[i] = ', '
    return ' '.join(sl)
