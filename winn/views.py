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
#from openpyxl import Workbook
import django_excel as excel
import pandas as pd
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


def contact(request):
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
    return render(request, 'winn/basic.html',{'content':["lol"]})

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
            Hist=HistoricoBienvenida.objects.all()
            Hdb=HistoricoBienvenida()
            sio = io.BytesIO()
            #book = Workbook(sio, {'in_memory': True})
            daf = read_frame(Hist,index_col="driver_id")
            filex=request.FILES['filex']
            data=pd.read_excel(filex, index_col=0)
            data=data[(data['is_active']==True) & (data["day_00"].notnull())]
            dos=pd.DataFrame()
            df=pd.DataFrame()
            #data=data[(data["is_active"]==True)]
            # & (data["day_00"].notnull())
            #data["is_active"]=data.is_active.convert_objects(convert_numeric=True)
            del data['country_code']
            #del data['car_license_plate']
            del data['time_activ']
            del data['suma_total']
            datos=data
            num=0
            while num < len(Tdo):
                if format(Tdo[num].Modalidad)=="Todas":
                    tres=data[(data["city_code"].map(lambda x: x.startswith(format(Tdo[num]))))]
                else:
                    tres=data[(data["city_code"].map(lambda x: x.startswith(format(Tdo[num])))) & (data["car_service"].map(lambda y: y.startswith(format(Tdo[num].Modalidad))))] 
                cuat=metas(tres,int(Tdo[num].Plazo))
                if format(Tdo[num].ReferidoEspecial)=="":
                    cuat=cuat[cuat["meta"]>int(Tdo[num].NumCarreras)-1]
                else:
                    cuat=cuat[cuat["meta"]>int(Tdo[num].NumCarrerasEspecial)-1]
                dos=pd.concat([dos,cuat])
                num=num+1
            hi=dos[~dos.index.isin(daf.index)]
            writer=pd.ExcelWriter(sio, engine='xlsxwriter')
            hi.to_excel(writer,sheet_name='Bienvenida',columns=['city_code','driver_name','driver_email','driver_phone','meta'])
            worksheet = writer.sheets['Bienvenida']
            i=0    
            while i < len(hi):
                n=0
                Hdb.driver_id=format(hi.index[i])
                Hdb.date=timezone.now()
                while n < len(Tdo):
                    if hi["city_code"][i]==format(Tdo[n]):
                        Hdb.monto_pago=Tdo[n].Premio
                    n=n+1
                Hdb.save()
                i=i+1
            #worksheet = writer.sheets['Referidos']
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 10)
            worksheet.set_column('C:C', 40)
            worksheet.set_column('D:D', 40)
            worksheet.set_column('E:E', 15)
            """
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
            #datos=datos[df["driv_referral"].isin(datos["driver_rut"])]
            #cuat=cuat[cuat["driver_rut"].isin(cuat["driv_referral"])]
            ref.to_excel(writer,sheet_name='Referidos',columns=['city_code','driver_name','driv_referral','driver_rut','meta'])
            worksheet = writer.sheets['Referidos']
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 10)
            worksheet.set_column('C:C', 40)
            worksheet.set_column('D:D', 40)
            worksheet.set_column('E:E', 20)
            """
            #pd.DataFrame()
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
            messages.add_message(request, messages.INFO, "Dato actualizados")
            #return redirect("uploads")
            #output.seek(0)
            response = HttpResponse(workbook, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Ganadores.xlsx"' 
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
