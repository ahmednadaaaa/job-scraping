import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate ,login  , logout 
from django.contrib.auth.decorators import  login_required
from django.contrib.auth.models import Group
from .forms import CreateNewUser
from project import settings




def search_page(request):
    return render(request, 'index.html')

def scrape_jobs(request, search_job="", page_num=0):
    search_query = request.GET.get('searchname', search_job)

    if not search_query:
        return redirect('job_search_page')

    url1 = f"https://wuzzuf.net/search/jobs/?a=hpb&q={search_query}&start={page_num}"
    url2 = f"https://eg.indeed.com/jobs?q={search_query}&start={page_num}"
    url3 = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&start={page_num}"

    result1 = requests.get(url1).content
    result2 = requests.get(url2).content
    result3 = requests.get(url3).content

    soup1 = BeautifulSoup(result1, "lxml")
    soup2 = BeautifulSoup(result2, "lxml")
    soup3 = BeautifulSoup(result3, "lxml")

    job_titles1 = soup1.find_all("h2", {"class": "css-m604qf"})
    company_names1 = soup1.find_all("div", {"class": "css-d7j1kk"})
    location_names1 = soup1.find_all("span", {"class": "css-5wys0k"})
    job_links1 = soup1.find_all("a", {"class": "css-o171kl"})

    job_titles2 = soup2.find_all("h2", {"class": "jobTitle"})
    company_names2 = soup2.find_all("span", {"class": "companyName"})
    location_names2 = soup2.find_all("div", {"class": "companyLocation"})
    job_links2 = soup2.find_all("a", {"class": "jcs-JobTitle"})

    job_titles3 = soup3.find_all("span", {"class": "sr-only"})
    company_names3 = soup3.find_all("h4", {"class": "base-search-card__subtitle"})
    location_names3 = soup3.find_all("span", {"class": "job-search-card__location"})
    job_links3 = soup3.find_all("a", {"class": "base-card__full-link"})

    jobs = []
    for i in range(len(job_titles1)):
        jobs.append({
            "title": job_titles1[i].text,
            "company": company_names1[i].text,
            "location": location_names1[i].text,
            "platform": "Wuzzuf",
            "link": f"{job_links1[i]['href']}"
        })

    for i in range(len(job_titles2)):
        jobs.append({
            "title": job_titles2[i].text.strip(),
            "company": company_names2[i].text.strip(),
            "location": location_names2[i].text.strip(),
            "platform": "Indeed",
            "link": f"https://eg.indeed.com{job_links2[i]['href']}"
        })

    for i in range(len(job_titles3)):
        jobs.append({
            "title": job_titles3[i].text.strip(),
            "company": company_names3[i].text.strip(),
            "location": location_names3[i].text.strip(),
            "platform": "LinkedIn",
            "link": job_links3[i]['href']
        })

    prev_page_num = page_num - 1 if page_num > 0 else 0
    next_page_num = page_num + 1

    context = {
        'jobs': jobs,
        'search_job': search_query,
        'page_num': page_num,
        'prev_page_num': prev_page_num,
        'next_page_num': next_page_num,
    }
    return render(request, 'job_list.html', context)



def register(request):   
            form = CreateNewUser()
            if request.method == 'POST': 
                   form = CreateNewUser(request.POST)
                   if form.is_valid():

                       recaptcha_response = request.POST.get('g-recaptcha-response')
                       data = {
                           'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                           'response' : recaptcha_response
                       }
                       r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                       result = r.json()
                       if result['success']:
                           user = form.save()
                           username = form.cleaned_data.get('username')
                           messages.success(request , username + ' Created Successfully !')
                           return redirect('login')
                       else:
                          messages.error(request ,  ' invalid Recaptcha please try again!')  
 
        
            context = {'form':form}

            return render(request , 'register.html', context )


def userLogin(request):  
  
        if request.method == 'POST': 
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request , username=username, password=password)
            if user is not None:
             login(request, user)
             return redirect('job_search_page')
            else:
                messages.info(request, 'Credentials error')
    
        context = {}

        return render(request , 'login.html', context )


def userLogout(request):  
    logout(request)
    return redirect('login') 


def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def index(request):
    return render(request, "index.html")