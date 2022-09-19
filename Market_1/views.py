from tkinter import EXCEPTION
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def gotoindex(request):
    return HttpResponseRedirect("/index")