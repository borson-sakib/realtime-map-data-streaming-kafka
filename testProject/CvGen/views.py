from django.shortcuts import render
from django.http import HttpResponse
import requests

url_repo_upper='https://api.github.com/users/'
url_repo_lower='/repos'
# Create your views here.

def index(request):
    if (request.method == 'POST'):
        url_repo_middle= str(request.POST.get('user_git'))
        
        url = url_repo_upper + url_repo_middle + url_repo_lower
        response=requests.get(url).json()
        
        return render(request,'base.html',{'response':response,'username':url_repo_middle})
        
        # return render(request, 'base.html')

def forms(request):
    # response=requests.get('https://api.github.com/users/borson-sakib/repos').json()
    
    # return render(request,'base.html',{'response':response})
    
    return render(request, 'form.html')

def resume(request):
    response=requests.get('https://api.github.com/users/borson-sakib/repos').json()

    return render(request, 'index.html',{'response':response})