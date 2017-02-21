#crawler
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.error
import requests
import http.client
#ref y bein
from xlsxwriter.workbook import Workbook
import io
import time
from django.utils import timezone
from django.shortcuts import render, redirect
from _compact import JsonResponse
from django.core.files.uploadhandler import (MemoryFileUploadHandler, TemporaryFileUploadHandler)
from django.core.files.uploadedfile import (InMemoryUploadedFile, TemporaryUploadedFile)
from django.contrib import messages
#from archivos.forms import UploadForm
from archivos.models import Document
from django_pandas.io import read_frame
from winn.models import Conductor,Referido,Condiciones, CondicionesRef, HistoricoBienvenida
from django.http import HttpResponseBadRequest, HttpResponse, StreamingHttpResponse
import openpyxl
#from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
import django_excel as excel
import pandas as pd
from xlrd.sheet import ctype_text
import xlrd
import pyexcel as pe
from django import forms
import datetime as dt
import sqlite3
from pandas.io import sql

#from django.http import HttpResponse

# Create your views here.

def subhistorico():
    Hso=HistoricoBienvenida()
    con=sqlite3.connect(':memory:')
    if request.method=='POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            filex=request.FILES['filex']
            data=pd.read_excel(filex, header=0)
            #fech = request.POST.get('data')
            #date = time.strptime(request.POST['data'], "%m/%d/%y")
            #ISO_date = '{}-{:02}-{:02}'.format(date.tm_year, date.tm_mon, date.tm_mday)
            #data=pd.DataFrame()
            print(len(data))
            #print(type(date))
            data["Driver_ID"]=data["Driver_ID"].astype('str')
            print(format(data.iloc[3][0]))
            cont = 0
            """
            while cont < len(data):
                Hso.driver_id=format(data.iloc[cont][0])
                #Hso.date=timezone.now()
                Hso.monto_pago=0
                Hso.save()
                cont = cont+1
            #"""
            #data.to_sql(name='historicoB', con=con, if_exists='append')
            """
            filename = filex.name
            extension = filename.split(".")[-1]
            #content = request.FILES['filex'].read()
            sheet = pe.get_sheet(file_type=extension, file_content=filex.read())
            print(len(sheet))
            cont = 0
            while cont < sheet.number_of_rows():
                c=HistoricoBienvenida(driver_id=format(sheet[cont, 0]),fecha_emitido=date)
                c.save()
                cont = cont+1
            """
            return excel.make_response_from_a_table(HistoricoBienvenida, 'xlsx', file_name="sheet")
    else:
        form=UploadForm()
    return render(request, 'winn/basic.html',{'form':form})

def HistoricoBExcel():
    sio = io.BytesIO()
    qs = HistoricoBienvenida.objects.all()
    df = read_frame(qs,index_col="driver_id")
    pd.to_datetime(df["date"],format="%d/%m/%Y")
    print(type(df["date"]))
    df["date"] = df["date"].astype('str')
    print(list(df))
    writer=pd.ExcelWriter(sio, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='HistoricoBienvenida')
    writer.save()
    sio.seek(0)
    workbook=sio.getvalue()
    response = HttpResponse(workbook, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="historicoBienvenida.xlsx"'
    return response

def delet(data,column):
    data[column] = data[column].astype('str')
    num=0
    for row in data[column]:
        data.loc[:, column][num]=row.replace(" ","")
        num=num+1
    return data

def deletel(data,column):
    data[column] = data[column].astype('str')
    num=0
    for row in data[column]:
        data.loc[:, column][num]=row.replace(".","")
        num=num+1
    return data

def deletl(data,column):
    data[column] = data[column].astype('str')
    num=0
    for row in data[column]:
        data.loc[:, column][num]=row.replace("-","")
        num=num+1
    return data

def index(request):
    W="HOLA CO"
    return render(request, 'winn/header.html')
#    return HttpResponse(W)

class UploadForm(forms.Form):
    filex = forms.FileField(label='Selecione su archivo')

def testurl(str):
    try:
        urlopen(str)
        return True
    except urllib.error.URLError:
        return False

def TwtterRestriccion():
    #abre pagina de twitter
    webpage=urlopen("https://twitter.com/RestriccionHoy")
    #lee la pagina
    html=webpage.read()
    #lista de numeros de twitt
    ffind=re.findall('data-tweet-id="(\d+)"',format(html))
    i=0
    lista=[]
    #ciclo para mostrar links de twiter
    while i!=len(ffind):
        link="https://twitter.com/RestriccionHoy/status/"+ffind[i]
        if testurl(format(link)):
            lista.append(link)
        else:
            print ("Dosent excits link")
        i=i+1
    return lista

def TwitterUOCT():
    #abre pagina de twitter
    webpage=urlopen("https://twitter.com/UOCT_RM")
    #lee la pagina
    html=webpage.read()
    #lista de numeros de twitt
    ffind=re.findall('data-tweet-id="(\d+)"',format(html))
    i=0
    lista=[]
    #ciclo para mostrar links de twiter
    while i!=len(ffind):
        link="https://twitter.com/UOCT_RM/status/"+ffind[i]
        if testurl(format(link)):
            lista.append(link)
        else:
            print ("Dosent excits link")
        i=i+1
    return lista

def TwitterRadioCarab():
    #abre pagina de twitter
    webpage=urlopen("https://twitter.com/radiocarab")
    #lee la pagina
    html=webpage.read()
    #lista de numeros de twitt
    ffind=re.findall('data-tweet-id="(\d+)"',format(html))
    i=0
    lista=[]
    #ciclo para mostrar links de twiter
    while i!=len(ffind):
        link="https://twitter.com/radiocarab/status/"+ffind[i]
        if testurl(format(link)):
            lista.append(link)
        else:
            print ("Dosent excits link")
        i=i+1
    return lista

def TwitterAutopCentral():
    #abre pagina de twitter
    webpage=urlopen("https://twitter.com/AutopCentral")
    #lee la pagina
    html=webpage.read()
    #lista de numeros de twitt
    ffind=re.findall('data-tweet-id="(\d+)"',format(html))
    i=0
    lista=[]
    #ciclo para mostrar links de twiter
    while i!=len(ffind):
        link="https://twitter.com/AutopCentral/status/"+ffind[i]
        if testurl(format(link)):
            lista.append(link)
        else:
            print ("Dosent excits link")
        i=i+1
    return lista

def TwitterVespucio_Sur():
    #abre pagina de twitter
    webpage=urlopen("https://twitter.com/Vespucio_Sur")
    #lee la pagina
    html=webpage.read()
    #lista de numeros de twitt
    ffind=re.findall('data-tweet-id="(\d+)"',format(html))
    i=0
    lista=[]
    #ciclo para mostrar links de twiter
    while i!=len(ffind):
        link="https://twitter.com/Vespucio_Sur/status/"+ffind[i]
        if testurl(format(link)):
            lista.append(link)
        else:
            print ("Dosent excits link")
        i=i+1
    return lista

def TwitterVespucio_Norte():
    #abre pagina de twitter
    webpage=urlopen("https://twitter.com/Vespucio_Norte")
    #lee la pagina
    html=webpage.read()
    #lista de numeros de twitt
    ffind=re.findall('data-tweet-id="(\d+)"',format(html))
    i=0
    lista=[]
    #ciclo para mostrar links de twiter
    while i!=6:
        link="https://twitter.com/Vespucio_Norte/status/"+ffind[i]
        if testurl(format(link)):
            lista.append(link)
        else:
            print ("Dosent excits link")
        i=i+1
    return lista

def TwitterCostaneraNorte():
    #abre pagina de twitter
    webpage=urlopen("https://twitter.com/CostaneraNorte_")
    #lee la pagina
    html=webpage.read()
    #lista de numeros de twitt
    ffind=re.findall('data-tweet-id="(\d+)"',format(html))
    i=0
    lista=[]
    #ciclo para mostrar links de twiter
    while i!=len(ffind):
        link="https://twitter.com/CostaneraNorte_/status/"+ffind[i]
        if testurl(format(link)):
            lista.append(link)
        else:
            print ("Dosent excits link")
        i=i+1
    return lista

def cooperativa():
    #abre pagina de cooperativa
    webpage=urlopen("http://www.cooperativa.cl/noticias/site/tax/port/all/taxport_3_88_642_1.html")
    #lee la pagina
    html=webpage.read()
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    #lista de links de la noticia, no incluye "http://www.cooperativa.cl" 
    ffind=re.findall(r'(?:href=["])([:/.A-z?<_&\s=>0-9;-]+)" class="titular"',format(html))
    #intento de obtener el titular de la noticia, aqui fracasa todo 'Noticias de Combustibles\n([:/.A-z?<_&\s=>0-9;-]+)[^\|]' \n*(\d{8}).+\n
    fnd=re.findall(r'(?:Noticias de Combustibles)([ñÑáéíóúÁÉÍÓÚ:,/.A-z?<_&\s=>0-9;-\|]+)Ver más en:',text)
    time=re.findall(r'(\d{10}:\d{2})',fnd[0])
    titu=re.findall(r'[\|]\n(.*)\n',fnd[0])
    #largo de lista de links noticias cooperativa
    print(len(ffind))
    #largo de lista de titulares de noticias, por ahora 0
    print(len(titu))
    i=0
    lista=[]
    #ciclo para mostrar links de noticias cooperativa
    while i!=len(ffind):
        link="http://www.cooperativa.cl"+ffind[i]
        if testurl(format(link)):
            lista.append(link)
            lista.append(titu[i])
        else:
            print ("Dosent excits link: ",link)
        i=i+1
    return lista

def contact(request):
    w2=TwitterUOCT()
    w3=TwitterAutopCentral()
    w=TwitterRadioCarab()
    w1=TwtterRestriccion()
    w4=TwitterVespucio_Sur()
    w5=TwitterVespucio_Norte()
    w6=TwitterCostaneraNorte()
    w7=cooperativa()
    return render(request, 'winn/basic.html',{'content':[w,w1,w2,w3,w4,w5,w6,w7]})

def metas(data, meta):
    if(meta==1):
        data["meta"]=data["day_00"]
        return data
    elif(meta==2):
        data["meta"]=data["day_01"]+data["day_00"]
        return data
    elif(meta==3):
        data["meta"]=data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==4):
        data["meta"]=data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==5):
        data["meta"]=data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==6):
        data["meta"]=data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==7):
        data["meta"]=data[['day_06','day_05','day_04','day_03','day_02','day_01','day_00']].sum(axis=1)
        return data
    elif(meta==8):
        data["meta"]=data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==9):
        data["meta"]=data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==10):
        data["meta"]=data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==11):
        data["meta"]=data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==12):
        data["meta"]=data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==13):
        data["meta"]=data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==14):
        data["meta"]=data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==15):
        data["meta"]=data[["day_14","day_13","day_12","day_11","day_10","day_09","day_08","day_07","day_06","day_05","day_04","day_03","day_02","day_01","day_00"]].sum(axis=1)
        #data["meta"]=data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==16):
        data["meta"]=data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==17):
        data["meta"]=data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==18):
        data["meta"]=data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==19):
        data["meta"]=data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==20):
        data["meta"]=data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==21):
        data["meta"]=data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==22):
        data["meta"]=data["day_21"]+data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==23):
        data["meta"]=data["day_22"]+data["day_21"]+data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==24):
        data["meta"]=data["day_23"]+data["day_22"]+data["day_21"]+data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==25):
        data["meta"]=data["day_24"]+data["day_23"]+data["day_22"]+data["day_21"]+data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==26):
        data["meta"]=data["day_25"]+data["day_24"]+data["day_23"]+data["day_22"]+data["day_21"]+data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==27):
        data["meta"]=data["day_26"]+data["day_25"]+data["day_24"]+data["day_23"]+data["day_22"]+data["day_21"]+data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==28):
        data["meta"]=data["day_27"]+data["day_26"]+data["day_25"]+data["day_24"]+data["day_23"]+data["day_22"]+data["day_21"]+data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==29):
        data["meta"]=data["day_28"]+data["day_27"]+data["day_26"]+data["day_25"]+data["day_24"]+data["day_23"]+data["day_22"]+data["day_21"]+data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==30):
        data["meta"]=data["day_29"]+data["day_28"]+data["day_27"]+data["day_26"]+data["day_25"]+data["day_24"]+data["day_23"]+data["day_22"]+data["day_21"]+data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data
    elif(meta==31):
        data["meta"]=data["day_30"]+data["day_29"]+data["day_28"]+data["day_27"]+data["day_26"]+data["day_25"]+data["day_24"]+data["day_23"]+data["day_22"]+data["day_21"]+data["day_20"]+data["day_19"]+data["day_18"]+data["day_17"]+data["day_16"]+data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
        return data

def upload_file(request):
    if request.method=='POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            Tdo=Condiciones.objects.all()
            Tda=CondicionesRef.objects.all()
            sio = io.BytesIO()
            #book = Workbook(sio, {'in_memory': True})
            filex=request.FILES['filex']
            data=pd.read_excel(filex, index_col=0)
            #data=data[(data['is_active']==True) & (data["day_00"].notnull())]
            dos=pd.DataFrame()
            datos=data
            df=pd.DataFrame()
            data=data[(data["is_active"]==True)]
            # & (data["day_00"].notnull())
            #data["is_active"]=data.is_active.convert_objects(convert_numeric=True)
            del data['country_code']
            #del data['car_license_plate']
            del data['time_activ']
            del data['suma_total']
            num=0
            while num < len(Tda):
                if format(Tda[num].Modalidad)=="todas":
                    cuat=data[(data["city_code"].map(lambda x: x.startswith(format(Tda[num]))))]                   
                else:
                    cuat=data[(data["city_code"].map(lambda x: x.startswith(format(Tda[num])))) & (data["car_service"].map(lambda y: y.startswith(format(Tda[num].Modalidad))))]             
                cuat=metas(cuat,int(Tda[num].Plazo))
                if format(Tda[num].ReferidoEspecial)=="":
                    cuat=cuat[cuat["meta"]>int(Tda[num].NumCarreras)-1]
                else:
                    cuat=cuat[cuat["meta"]>int(Tda[num].NumCarrerasEspecial)-1]
                df=pd.concat([df,cuat])
                num=num+1
            #df["driv_referral"]=df.driv_referral.convert_objects(convert_numeric=True)
            df=delet(df,"driv_referral")
            df=deletel(df,"driv_referral")
            df=deletl(df,"driv_referral")
            df=df[df["driv_referral"].notnull()]
            ref=df[df["driv_referral"].map(lambda x: x.startswith(format(Tda[0].ReferidoEspecial)))]
            datos=datos[df["driv_referral"].isin(datos["driver_rut"])]
            #cuat=cuat[cuat["driver_rut"].isin(cuat["driv_referral"])]
            writer=pd.ExcelWriter(sio, engine='xlsxwriter')
            ref.to_excel(writer,sheet_name='Referidos',columns=['city_code','driver_name','driv_referral','driver_rut','meta'])
            worksheet = writer.sheets['Referidos']
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 10)
            worksheet.set_column('C:C', 40)
            worksheet.set_column('D:D', 40)
            worksheet.set_column('E:E', 20)
            #pd.DataFrame()
            num=0
            while num < len(Tdo):
                if format(Tdo[num].Modalidad)=="Todas":
                    tres=data[(data["city_code"].map(lambda x: x.startswith(format(Tdo[num]))))]                   
                else:
                    tres=data[(data["city_code"].map(lambda x: x.startswith(format(Tdo[num])))) & (data["car_service"].map(lambda y: y.startswith(format(Tdo[num].Modalidad))))] 
                tres=metas(tres,int(Tdo[num].Plazo))
                if format(Tda[num].ReferidoEspecial)=="":
                    cuat=cuat[cuat["meta"]>int(Tda[num].NumCarreras)-1]
                else:
                    cuat=cuat[cuat["meta"]>int(Tda[num].NumCarrerasEspecial)-1]
                dos=pd.concat([dos,tres])
                num=num+1
            dos.to_excel(writer,sheet_name='Bienvenida',columns=['city_code','driver_name','driver_email','driver_phone','meta','is_active'])
            worksheet = writer.sheets['Bienvenida']
            #worksheet = writer.sheets['Referidos']
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 10)
            worksheet.set_column('C:C', 40)
            worksheet.set_column('D:D', 40)
            worksheet.set_column('E:E', 15)
            #data["driv_referral"]=data.driv_referral.convert_objects(convert_numeric=True)
            #data=data[data["is_active"]==True].fillna(0)
            #data=pd.DataFrame()
            data=datos
            writer.save()           
            #tres["esp"]=tres["day_15"]+tres["day_14"]+tres["day_13"]+tres["day_12"]+tres["day_11"]+tres["day_10"]+tres["day_09"]+tres["day_08"]+tres["day_07"]+tres["day_06"]+tres["day_05"]+tres["day_04"]+tres["day_03"]+tres["day_02"]+tres["day_01"]+tres["day_00"]
            #tres["tot"]=(tres,int(Tdo[0].NumCarreras))
            #data["meta"]=data["day_15"]+data["day_14"]+data["day_13"]+data["day_12"]+data["day_11"]+data["day_10"]+data["day_09"]+data["day_08"]+data["day_07"]+data["day_06"]+data["day_05"]+data["day_04"]+data["day_03"]+data["day_02"]+data["day_01"]+data["day_00"]
            #dos=data[(data["city_code"].map(lambda x: x.startswith(format(Tdo[0])))) & (data["parc"]>(Tdo[0].NumCarreras-1))]
            #sheet=writer.sheets['Bienvenida']
            #book.close()
            #worksheet = workbook.active()
            #worksheet.write(0, 0, 'Hello, world!')
            #workbook.close()
            #tres.to_excel(writer,'ganadores')
            sio.seek(0)
            workbook=sio.getvalue()
            #book = pe.get_book(bookdict=filex.read())
            #hoja=book.sheet_by_index(0)
            #filex.open('self')
            #filex.read()
            """
            filename = filex.name
            extension = filename.split(".")[-1]
            #content = request.FILES['filex'].read()
            sheet = pe.get_sheet(file_type=extension, file_content=filex.read())
            sheet.name_columns_by_row(0)
            cont = 0
            while cont < sheet.number_of_rows():
                c=Conductor(d_id=sheet[cont, "driverID"],d_cityc=sheet[cont, "city_code"],d_name=sheet[cont, "driver_name"],d_fone=sheet[cont, "driver_phone"],d_email=sheet[cont, "driver_email"],d_active=sheet[cont, "is_active"],d_date=sheet[cont, "date_activ"],total_c=0)
                c.save()
                cont = cont+1
            """
            #c=Conductor(d_id=sheet[2, "driverID"],d_cityc=sheet[2, "city_code"],d_name=sheet[2, "driver_name"],d_fone=sheet[2, "driver_phone"],d_email=sheet[2, "driver_email"],d_active=sheet[2, "is_active"],d_date=sheet[2, "date_activ"],total_c=0)
            #c.save()
            #sheet.save_to_django_model(Conductor,initializer=None,mapdict=['d_id','d_cityc','d_name','d_fone','d_email','d_active','d_date'])
            messages.add_message(request, messages.INFO, type(data))
            #return redirect("uploads")
            #output.seek(0)
            response = HttpResponse(workbook, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="winer.xlsx"' 
            return response
            ##return excel.make_response(sheet, "xlsx",file_name="download")
    else:
        form=UploadForm()
    return render(request, 'winn/upload.html',{'form':form})




def import_data(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            arch=request.FILES['filex']
            arch.open('self')
            arch.chunks('self')
            c=Conductor()
            r=Referido()
            arch.save_book_to_database(
                models=[Conductor, Referido],
                initializer=[None],
                mapdict=[
                    ['d_id','d_cityc','d_name','d_fone','d_email','d_active','d_date'],
                    ['r_id','r_name','r_name','r_fone','r_active','r_rut']]
                )
            return HttpResponse("OK", status=200)
        else:
            return HttpResponseBadRequest()
    else:
        form = UploadForm()
    return render(request,'winn/upload.html',{'form': form})


def mostrar(request):
    return render(request, 'winn/tabla.html')
