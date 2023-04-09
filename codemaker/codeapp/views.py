from django.shortcuts import render
from django.contrib import messages
import os
import openai
def home(request):
    print(os.getenv('API_KEY'))
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'css-extras', 'dart', 'django', 'fsharp', 'go', 'go-module', 'gradle', 'graphql', 'groovy', 'java', 'javadoc', 'javadoclike', 'javascript', 'json', 'json5', 'jsonp', 'jsx', 'markup', 'markup-templating', 'nginx', 'objectivec', 'perl', 'php', 'phpdoc', 'plsql', 'powershell', 'python', 'r', 'ruby', 'rust', 'sas', 'sass', 'scala', 'scss', 'sql', 'tcl', 'tsx', 'typescript', 'typoscript', 'xml-doc', 'yaml']
    if request.method == 'POST':
        code = request.POST.get('code')
        lang = request.POST.get('lang')

        if lang == "Select Programming Language":
            messages.success(request, 'Please select a programming language')
            return render(request, 'home.html', {'code': code, 'lang': lang, 'lang_list': lang_list})

        #OPENAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.Model.list()
        try:
            response = openai.Completion.create(
                engine = "text-davinci-003",
                prompt = f"Respond only with code. Fix this {lang} code: {code}",
                temperature = 0,
                max_tokens = 1000,
                top_p = 1.0,
                frequency_penalty = 0.0,
                presence_penalty = 0.0,
            )

            response = response['choices'][0]['text']

            return render(request, 'home.html', {'lang_list':lang_list, 'response':response, 'lang':lang})
        except Exception as e:
            print(e)
            return render(request, 'home.html', {'lang_list':lang_list, 'response':e, 'lang':lang})

    return render(request, 'home.html', {'lang_list': lang_list})

def suggest(request):
    print(os.getenv('API_KEY'))
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'css-extras', 'dart', 'django', 'fsharp', 'go', 'go-module', 'gradle', 'graphql', 'groovy', 'java', 'javadoc', 'javadoclike', 'javascript', 'json', 'json5', 'jsonp', 'jsx', 'markup', 'markup-templating', 'nginx', 'objectivec', 'perl', 'php', 'phpdoc', 'plsql', 'powershell', 'python', 'r', 'ruby', 'rust', 'sas', 'sass', 'scala', 'scss', 'sql', 'tcl', 'tsx', 'typescript', 'typoscript', 'xml-doc', 'yaml']
    if request.method == 'POST':
        code = request.POST.get('code')
        lang = request.POST.get('lang')

        if lang == "Select Programming Language":
            messages.success(request, 'Please select a programming language')
            return render(request, 'suggest.html', {'code': code, 'lang': lang, 'lang_list': lang_list})

        #OPENAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.Model.list()
        try:
            response = openai.Completion.create(
                engine = "text-davinci-003",
                prompt = f"Respond only with code. {code}",
                temperature = 0,
                max_tokens = 1000,
                top_p = 1.0,
                frequency_penalty = 0.0,
                presence_penalty = 0.0,
            )

            response = response['choices'][0]['text']

            return render(request, 'suggest.html', {'lang_list':lang_list, 'response':response, 'lang':lang})
        except Exception as e:
            print(e)
            return render(request, 'suggest.html', {'lang_list':lang_list, 'response':e, 'lang':lang})

    return render(request, 'suggest.html', {'lang_list': lang_list})