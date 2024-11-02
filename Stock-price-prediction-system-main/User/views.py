from django.shortcuts import render, redirect
#from .models import DoctorReg, predictions, Regdb
from django.contrib import messages
from django.contrib.auth.models import User, auth
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


# Create your views here.

def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save();
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'password not matching')
            return redirect('register')
        return redirect('/')
    else:
        return render(request, 'register.html')



def login(request):
    if request.method == 'POST':
        #v = DoctorReg.objects.all()
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'data.html')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def data(request):
    return render(request,"data.html")


def predict(request):
    if (request.method == 'POST'):
        open = request.POST['open']
        high = request.POST['high']
        low= request.POST['low']
        last = request.POST['last']
        close = request.POST['close']
        trade=request.POST['trade']

        df = pd.read_csv(r"static/datasets/Stock.csv")
        df.dropna(inplace=True)
        df.isnull().sum()
        X_train = df[['Open','High','Low','Last','Close','Total Trade Quantity']]

        Y_train = df[['Turnover (Lacs)']]
        tree = DecisionTreeRegressor()
        tree.fit(X_train, Y_train)

        prediction = tree.predict([[open,high,low,last,close,trade]])

        return render(request, 'predict.html',
                      {"data": prediction, 'open': open,  'high': high,
                       'close': close, 'last': last,"low":low,'trade':trade
                       })


    else:
        return render(request, 'predict.html')

def logout(request):
    return render(request,"logout.html")