from django.shortcuts import render
from django.contrib import messages
def home(request):
    lang_list = ['c', 'clike', 'cpp', 'csharp', 'css', 'css-extras', 'dart', 'django', 'fsharp', 'go', 'go-module', 'gradle', 'graphql', 'groovy', 'java', 'javadoc', 'javadoclike', 'javascript', 'json', 'json5', 'jsonp', 'jsx', 'markup', 'markup-templating', 'nginx', 'objectivec', 'perl', 'php', 'phpdoc', 'plsql', 'powershell', 'python', 'r', 'ruby', 'rust', 'sas', 'sass', 'scala', 'scss', 'sql', 'tcl', 'tsx', 'typescript', 'typoscript', 'xml-doc', 'yaml']
    if request.method == 'POST':
        code = request.POST.get('code')
        lang = request.POST.get('lang')

        if lang == "Select Programming Language":
            messages.success(request, 'Please select a programming language')
            return render(request, 'home.html', {'code': code, 'lang': lang, 'lang_list': lang_list})

        return render(request, 'home.html', {'code': code, 'lang': lang, 'lang_list': lang_list})

    return render(request, 'home.html', {'lang_list': lang_list})