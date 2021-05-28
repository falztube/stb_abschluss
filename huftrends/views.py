#django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from .forms import OrderForm, CreateUserForm


#models
from .models import TrendValue15Minutes
#plotly
from plotly.offline import plot
import plotly_express as px
import plotly.graph_objects as go

# pandas
import pandas as pd

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password incorrect')
            
    context={}
    return render (request, 'components/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def register_view(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + user)
            return redirect('login')


    context={'form':form}
    return render (request, 'components/register.html', context)


@login_required(login_url='login')
def home_view(request):
    return render(request, 'base2.html')

    


#Beginn Raum Views

plot_width = 2260
plot_height = 1240
paper_bgcolor = '#dddee6'
plot_bgcolor = '#c9d7e8'
line_width = 1.25
dtick=5


@login_required(login_url='login')
@allowed_users(allowed_roles=['LB','TGM'])
def raum1_view(request):  
    
    #Abfrage Trenddaten
    raumvar= 'Raum_01' 
    
    df=pd.DataFrame(TrendValue15Minutes.objects.using('meineDB')
    .filter(plaintext__startswith=raumvar)
    .values('timestamp', 'plaintext', 'value', 'unit'))

    #abgefragte Trenddaten pivotieren, NULL Werte mit letztem gültigen Wert ersetzen
    df_piv=pd.pivot(df,index='timestamp', columns='plaintext', values='value')
    df_piv=df_piv.fillna(method='bfill')


    #Durchschnittswerte aller 4 Temp, bzw. Feuchtewerte ermitteln
    #zunächst Temp und Feuchte voneinander trennen
    just_temp = df_piv.filter(regex='_Temp')
    just_feucht = df_piv.filter(regex='_Feucht')   

    #mit denn getrennten Werten jeweils den Durchschnitt ermitteln lassen
    avg_temp=just_temp.mean(axis=1)
    avg_feucht=just_feucht.mean(axis=1)
    
    #Plot mit allen Werten erzeugen
    raw_val_plot=px.line(df_piv, x=df_piv.index, y=df_piv.columns,width=plot_width, height=plot_height)
    
    #Plot mit Durchschnittswerten erzeugen
    avg_val_plot=px.line(df_piv, x=df_piv.index, y=[avg_temp,avg_feucht],width=plot_width, height=plot_height)
    
    #Beide Plots zu einem kombinieren 
    plot1 = go.Figure(data=avg_val_plot.data + raw_val_plot.data)
    
    #Layout für Plot1
    plot1.update_layout(
        {'paper_bgcolor': paper_bgcolor,
        'plot_bgcolor': plot_bgcolor},
        width=plot_width,
        height=plot_height,
        autosize=True,
        title=raumvar)
    
    #Achsbeschriftung und Skaleneinteilung
    plot1.update_yaxes(title_font=dict(size=18, family='Arial', color='black'),dtick=5)
    plot1.update_xaxes(title_font=dict(size=18, family='Arial', color='black'))
    
    #Linienstärke anpassen
    plot1.update_traces(line={"width": line_width})
    
    #Buttons für Zeitbereich hinzufügen (direkt von Plotly Webseite und angepasst)
    plot1.update_layout(xaxis=dict(rangeselector=dict(buttons=([
                dict(count=1,
                     label="hour",
                     step="hour",
                     stepmode="backward"),
                dict(count=1,
                     label="day",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="7d",
                     step="day",
                     stepmode="todate"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        )
        
    )
)
    

    plot1_div=plot(plot1, output_type='div', include_plotlyjs=False)
    return render(request, "values.html", context={'plot1_div': plot1_div})
    
                   
                     
@login_required(login_url='login')
@allowed_users(allowed_roles=['HUF','TGM'])
def raum2_view(request):  
    
    
    raumvar= 'Raum_02' 
    #Abfrage Trenddaten
    df=pd.DataFrame(TrendValue15Minutes.objects.using('meineDB')
    .filter(plaintext__startswith=raumvar)
    .values('timestamp', 'plaintext', 'value', 'unit'))

       
    

    #abgefragte Trenddaten pivotieren, NULL Werte mit letztem gültigen Wert ersetzen
    df_piv=pd.pivot(df,index='timestamp', columns='plaintext', values='value')
    df_piv=df_piv.fillna(method='bfill')


    #Durchschnittswerte aller 4 Temp, bzw. Feuchtewerte ermitteln
    #zunächst Temp und Feuchte voneinander trennen
    just_temp = df_piv.filter(regex='_Temp')
    just_feucht = df_piv.filter(regex='_Feucht')   

    #mit denn getrennten Werten jeweils den Durchschnitt ermitteln lassen
    avg_temp=just_temp.mean(axis=1)
    avg_feucht=just_feucht.mean(axis=1)
    
    #Plot mit allen Daten erzeugen
    fig3=px.line(df_piv, x=df_piv.index, y=df_piv.columns,width=plot_width, height=plot_height,title=raumvar)
    
    #Plot mit Durchschnittswerten erzeugen
    avg_val_plot=px.line(df_piv, x=df_piv.index, y=[avg_temp,avg_feucht],width=plot_width, height=plot_height,title='Durchschnittswerte')
    
    #Beide Plots zu einem kombinieren (geht bestimmt auch einfacher)
    plot1 = go.Figure(data=avg_val_plot.data + fig3.data)
    
    #Layout für Plot1
    plot1_layout = plot1.update_layout(
        {'paper_bgcolor': paper_bgcolor,
        'plot_bgcolor': plot_bgcolor},
        width=plot_width,
        height=plot_height,
        autosize=True,
        title=raumvar)
    
    
    plot1.update_yaxes(title_font=dict(size=18, family='Arial', color='black'),tick0=0,dtick=5)
    plot1.update_xaxes(title_font=dict(size=18, family='Arial', color='black'))
    
    #Linienstärke anpassen
    plot1.update_traces(line={"width": line_width})
    
    #Buttons für Zeitbereich hinzufügen (direkt von Plotly Webseite und angepasst)
    plot1.update_layout(xaxis=dict(rangeselector=dict(buttons=([
                dict(count=1,
                     label="hour",
                     step="hour",
                     stepmode="backward"),
                dict(count=1,
                     label="today",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="7d",
                     step="day",
                     stepmode="todate"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        )
        
    )
)
    
    
    plot1_div=plot(plot1, output_type='div', include_plotlyjs=False)  
    
    return render(request, "values.html", context={'plot1_div': plot1_div})
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['SMB','TGM'])
def raum3_view(request):  
    
    
    raumvar= 'Raum_03' 
    #Abfrage Trenddaten
    df=pd.DataFrame(TrendValue15Minutes.objects.using('meineDB')
    .filter(plaintext__startswith=raumvar)
    .values('timestamp', 'plaintext', 'value', 'unit'))

       
    

    #abgefragte Trenddaten pivotieren, NULL Werte mit letztem gültigen Wert ersetzen
    df_piv=pd.pivot(df,index='timestamp', columns='plaintext', values='value')
    df_piv=df_piv.fillna(method='bfill')


    #Durchschnittswerte aller 4 Temp, bzw. Feuchtewerte ermitteln
    #zunächst Temp und Feuchte voneinander trennen
    just_temp = df_piv.filter(regex='_Temp')
    just_feucht = df_piv.filter(regex='_Feucht')   

    #mit denn getrennten Werten jeweils den Durchschnitt ermitteln lassen
    avg_temp=just_temp.mean(axis=1)
    avg_feucht=just_feucht.mean(axis=1)
    
    #Plot mit allen Daten erzeugen
    fig3=px.line(df_piv, x=df_piv.index, y=df_piv.columns,width=plot_width, height=plot_height,title=raumvar)
    
    #Plot mit Durchschnittswerten erzeugen
    avg_val_plot=px.line(df_piv, x=df_piv.index, y=[avg_temp,avg_feucht],width=plot_width, height=plot_height,title='Durchschnittswerte')
    
    #Beide Plots zu einem kombinieren (geht bestimmt auch einfacher)
    plot1 = go.Figure(data=avg_val_plot.data + fig3.data)
    
    #Layout für Plot1
    plot1_layout = plot1.update_layout(
        {'paper_bgcolor': paper_bgcolor,
        'plot_bgcolor': plot_bgcolor},
        width=plot_width,
        height=plot_height,
        autosize=True,
        title=raumvar)
    
    
    plot1.update_yaxes(title_font=dict(size=18, family='Arial', color='black'),tick0=0,dtick=5)
    plot1.update_xaxes(title_font=dict(size=18, family='Arial', color='black'))
    
    #Linienstärke anpassen
    plot1.update_traces(line={"width": line_width})
    
    #Buttons für Zeitbereich hinzufügen (direkt von Plotly Webseite und angepasst)
    plot1.update_layout(xaxis=dict(rangeselector=dict(buttons=([
                dict(count=1,
                     label="hour",
                     step="hour",
                     stepmode="backward"),
                dict(count=1,
                     label="today",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="7d",
                     step="day",
                     stepmode="todate"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        )
        
    )
)
    
    
    plot1_div=plot(plot1, output_type='div', include_plotlyjs=False)  
    
    return render(request, "values.html", context={'plot1_div': plot1_div})
    


@login_required(login_url='login')
@allowed_users(allowed_roles=['SMB','TGM'])
def raum4_view(request):  
    
    
    raumvar= 'Raum_04' 
    #Abfrage Trenddaten
    df=pd.DataFrame(TrendValue15Minutes.objects.using('meineDB')
    .filter(plaintext__startswith=raumvar)
    .values('timestamp', 'plaintext', 'value', 'unit'))

       
    

    #abgefragte Trenddaten pivotieren, NULL Werte mit letztem gültigen Wert ersetzen
    df_piv=pd.pivot(df,index='timestamp', columns='plaintext', values='value')
    df_piv=df_piv.fillna(method='bfill')


    #Durchschnittswerte aller 4 Temp, bzw. Feuchtewerte ermitteln
    #zunächst Temp und Feuchte voneinander trennen
    just_temp = df_piv.filter(regex='_Temp')
    just_feucht = df_piv.filter(regex='_Feucht')   

    #mit denn getrennten Werten jeweils den Durchschnitt ermitteln lassen
    avg_temp=just_temp.mean(axis=1)
    avg_feucht=just_feucht.mean(axis=1)
    
    #Plot mit allen Daten erzeugen
    fig3=px.line(df_piv, x=df_piv.index, y=df_piv.columns,width=plot_width, height=plot_height,title=raumvar)
    
    #Plot mit Durchschnittswerten erzeugen
    avg_val_plot=px.line(df_piv, x=df_piv.index, y=[avg_temp,avg_feucht],width=plot_width, height=plot_height,title='Durchschnittswerte')
    
    #Beide Plots zu einem kombinieren (geht bestimmt auch einfacher)
    plot1 = go.Figure(data=avg_val_plot.data + fig3.data)
    
    #Layout für Plot1
    plot1_layout = plot1.update_layout(
        {'paper_bgcolor': paper_bgcolor,
        'plot_bgcolor': plot_bgcolor},
        width=plot_width,
        height=plot_height,
        autosize=True,
        title=raumvar)
    
    
    plot1.update_yaxes(title_font=dict(size=18, family='Arial', color='black'),tick0=0,dtick=5)
    plot1.update_xaxes(title_font=dict(size=18, family='Arial', color='black'))
    
    #Linienstärke anpassen
    plot1.update_traces(line={"width": line_width})
    
    #Buttons für Zeitbereich hinzufügen (direkt von Plotly Webseite und angepasst)
    plot1.update_layout(xaxis=dict(rangeselector=dict(buttons=([
                dict(count=1,
                     label="hour",
                     step="hour",
                     stepmode="backward"),
                dict(count=1,
                     label="today",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="7d",
                     step="day",
                     stepmode="todate"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        )
        
    )
)
    
    
    plot1_div=plot(plot1, output_type='div', include_plotlyjs=False)  
    
    return render(request, "values.html", context={'plot1_div': plot1_div})
 





    
    
 




       
    

    

