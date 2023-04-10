from django.shortcuts import render, redirect
from django.contrib import messages
import os
import openai
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Snippet
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
            code_snippet = Snippet(user=request.user, question=code, code_snippet=response, language=lang)
            code_snippet.save()
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
            code_snippet = Snippet(user=request.user, question=code, code_snippet=response, language=lang)
            code_snippet.save()

            return render(request, 'suggest.html', {'lang_list':lang_list, 'response':response, 'lang':lang})
        except Exception as e:
            print(e)
            return render(request, 'suggest.html', {'lang_list':lang_list, 'response':e, 'lang':lang})

    return render(request, 'suggest.html', {'lang_list': lang_list})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user)
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('home')
        else:
            messages.success(request, 'Error logging in')
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('home')

def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def history(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        snippets = Snippet.objects.filter(user_id=request.user.id)
        return render(request, 'history.html', {'snippets': snippets})

def delete_snippet(request, question_id):
    if not request.user.is_authenticated:
        return redirect('home')
    else:
        snippet = Snippet.objects.get(pk=question_id)
        snippet.delete()
        messages.success(request, 'Snippet deleted successfully...')
        return redirect('history')

def images(request):
    print(os.getenv('API_KEY'))
    if request.method == 'POST':
        code = request.POST.get('code')

        #OPENAI
        openai.api_key = os.getenv('OPENAI_API_KEY')
        openai.Model.list()
        try:
            print("code: ", code)
            response = openai.Image.create(
                prompt="{code}",
                n=1,
                size="256x256"
            )
            image_dir_name = "images"
            #image_dir = os.path.join(os.curdir, image_dir_name)
            #image_dir = "/Users/avitenzer/Documents/_workspace/codemaker/codemaker/codeapp/images"


            current_directory = os.getcwd()
            image_dir = os.path.join(current_directory,image_dir_name)
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            generated_image_name = "generated_image1.png"  # any name you like; the filetype should be .png
            generated_image_filepath = os.path.join(image_dir, generated_image_name)

            generated_image_url = response["data"][0]["url"]  # extract image URL from response
            generated_image = requests.get(generated_image_url).content  # download the image

            with open(generated_image_filepath, "wb") as image_file:
                image_file.write(generated_image)
            # response = response['choices'][0]['text']
            # code_snippet = Snippet(user=request.user, question=code, code_snippet=response, language=lang)
            # code_snippet.save()

            return render(request, 'images.html', {'response':generated_image_url})
        except Exception as e:
            print(e)
            return render(request, 'images.html', { 'response':e})

    return render(request, 'images.html', {})