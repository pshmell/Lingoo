from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from word.forms import *
from word.models import *
from django.core.context_processors import csrf
import json_factory


#############################BROWSING###################################
def upload_page(request):
    """
    NOTE: SOLID DO NOT CHANGE

    upload page is the main page
    add any file and it will up load the file and add a row to word_text table in the db

    """
    print "TEST PAGE: upload page call"

    # protect against cross site forgery using token c... required in django when posting to a form
    c = {}
    c.update(csrf(request))

    ajax = 'ajax' in request.GET

    if request.method == 'POST':
        print "TEST: request method is post"
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            print "TEST: form.is_valid returned True"
            filename = save(form, request)
            #
            #
            #
            return HttpResponseRedirect('analysis/' + str(filename))
        else:
            print "TEST: form.is_valid returned False"
            if ajax:
                print "ajax\t" + repr(ajax)
                return HttpResponse("failure")
    elif 'file' in request.GET:
        print "TEST: 'file' in request.GET returned True"
        file = request.GET['file']
        try:
            print "TEST: try: path  = Text.objects.get(path= file.__name__)"
        except Text.DoesNotExist:
            print "TEST: except Text.DoesNotExist pass"
            pass
        form = UploadForm({
            'file' : file,
            })
    else:
        print "TEST: method is not POST and there is no file in request.GET"
        form  = UploadForm()
    variables = RequestContext(request, {
        'form': form
    })
    if ajax:
        print "TEST: ajax True - render to response upload_page_form"
        return render_to_response('upload_page_form.html', c, variables)
    else:
        print "TEST: ajax False - render to response upload_page"
        return render_to_response('upload_page.html', c, variables)


def analysis_page(request, filename):
    """get json and display it"""
    print "TEST PAGE: analysis_page call"
    json_path = 'uploads/' + filename + '.important.json'
    f = open(json_path, 'rb')
    data_string = f.readline()
    data_string = data_string.replace('{\"','{tag: \"')
    data_string = data_string.replace('\",','\", count: ')

    print "TEST: data string is" + str(data_string)

    #if request.method == 'POST':
        #print "TEST: request method is POST"
        #json = request.POST['json']
        #print "TEST json: " + repr(json)
    #else:
        #print "TEST: request method is not POST"
        #json = request.GET['json']
        #print "TEST json: " + repr(json)
    variables = RequestContext(request, {
        'json': data_string,
        'file': filename,
        })
    print "TEST variables: " + repr(variables)
    return render_to_response('analysis.html', variables)


def cloud_page(request, file):
    """currently a place holder with some funkay junk"""
    print "TEST PAGE: cloud_page call"
    json_path = 'uploads/' + file
    print str(json_path)
    f = open(json_path, 'rb')
    data_string = f.readline()
    data_string = data_string.replace('{\"','{tag: \"')
    data_string = data_string.replace('\",','\", count: ')

    variables = RequestContext(request, {
        'file': file,
        'json': data_string,
        })

    return render_to_response('cloud.html', variables)


def text_page(request):
    """currently a place holder"""
    print "TEST PAGE: text_page call"
    return render_to_response('text.html', RequestContext(request))


#############################HANDLING#####################################
def save(form, request):
    """

    get file f and call handle_file() to write it to uploads
    make a text object with id and path, if it already exists just get it
    use json_factory.process() to generate the json for later display
    """
    print "TEST FCN: save call"
    complete_path, filename = handle_file(request.FILES['file'])
    # get or create a corpus
    text, created = Text.objects.get_or_create(
        path = complete_path,
    )
    print repr(text.path)
    # create json
    json = json_factory.process(text.path)
    # save corpus to database and return it
    text.save()
    print "TEST: text.save()"
    print "TEST: text_list = " + repr(Text.objects.all())

    #variables = RequestContext(request, {
        #'json': analysisJSON,
        #})
    #print "TEST: variables set to " + repr(variables)
    return filename


def handle_file(f):
    """

    NOTE:
    SOLID, LEAVE BE

    handle_file pseudo code:
    set upload path
    open the file destination and write the uploaded file to the destination chunk by chunk
    close destination
    """
    print "TEST FCN: handle_file call"

    path = 'uploads/' # todo: delete if redundant considering settings defines the same upload path
    complete_path = path + f.name
    destination = open((complete_path), 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

    print "TEST: file has been written to " + repr(destination)
    return complete_path, f.name
