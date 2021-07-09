from django.shortcuts import render
import pandas as pd
import datetime
import numpy as np
from joblib import load
from CChurn.models import FormDataFile,UserTable
from django.contrib import messages
from sklearn import preprocessing
import sklearn
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
# from sklearn.pandas import DataFrameMapper
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import json
from sklearn.preprocessing import Normalizer
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


# Create your viewsz here.
def Form(request):
    if request.POST:
        print(request.POST)
        State = request.POST['State']
        #State = 35
        AccountLength = request.POST['AccountLength']
        AreaCode = request.POST['AreaCode']
        InternationalPlan = request.POST['InternationalPlan']
        VoiceMail = request.POST['VoiceMail']
        TotalDayMinutes = request.POST['TotalDayMinutes']
        TotalDayCalls = request.POST['TotalDayCalls']
        NumberVoiceMail = request.POST['NumberVoiceMail']
        TotalDayCharge = request.POST['TotalDayCharge']
        TotalEveningCalls = request.POST['TotalEveningCalls']
        TotalEveningMinutes = request.POST['TotalEveningMinutes']
        TotalEveningCharge = request.POST['TotalEveningCharge']
        TotalNightMinute = request.POST['TotalNightMinute']
        TotalNightCalls = request.POST['TotalNightCalls']
        TotalNightCharge = request.POST['TotalNightCharge']
        TotalInternationalCall = request.POST['TotalInternationalCall']
        TotalInternationalMinute = request.POST['TotalInternationalMinute']
        TotalInternationalCharge = request.POST['TotalInternationalCharge']
        NumberCustomer = request.POST['NumberCustomer']

#LOAD DATA

        Data_train = pd.read_csv('CChurn/Customerchurn.csv')
        #prediction_data = pd.read_csv('whatever.csv')

#FORMAT DATA

        Data_train['state'] = Data_train['state'].astype('category')
        Data_train['area_code'] = Data_train['area_code'].astype('category')
        Data_train['international_plan'] = Data_train['international_plan'].astype('category')
        Data_train['voice_mail_plan'] = Data_train['voice_mail_plan'].astype('category')

#DEFINING CATEGORICAL COLS

        categoricalColumns = ['state', 'area_code', 'international_plan', 'voice_mail_plan']
        categorical_columns = []
        categorical_ix = Data_train.select_dtypes(include=['object', 'bool']).columns

        onehotCategorical = preprocessing.OneHotEncoder(handle_unknown='ignore', categories='auto', sparse=False)
        #dump(onehotCategorical, 'onehotCategorical.joblib')
        categorical_transformer = Pipeline(steps=[('onehot', onehotCategorical)])

        cols = ['area_code', 'international_plan', 'voice_mail_plan']
        Data_categorical = Data_train.loc[:, cols]
        Data_categorical['churn'] = Data_train['churn']

        Data_categorical['churn'].replace(to_replace='yes', value=1, inplace=True)
        Data_categorical['churn'].replace(to_replace='no', value=0, inplace=True)

#ENCODING DATA

        Data_dummies = Data_train.apply(LabelEncoder().fit_transform)
        Data_dummies['churn'] = Data_categorical['churn']

#DEFINING NUMERICAL COLS

        numericalColumns = Data_train.select_dtypes(include=[np.float, np.int]).columns
        scaler_numerical = StandardScaler()
        numerical_transformer = Pipeline(steps=[('scale', scaler_numerical)])



        preproc = ColumnTransformer(transformers=[('cat', categorical_transformer, categoricalColumns),
                                                   ('num', numerical_transformer, numericalColumns)],
                                     remainder="passthrough")
        Data_churn_pd = preproc.fit_transform(Data_train)

#DEFINING X AND Y

        X = []
        X = Data_dummies.drop(['churn'], axis=1)
        # X = pd.DataFrame(Data_churn_pd).iloc[:,:-1]

        #labebl_churn = pd.DataFrame(Data_train, columns=['churn'])
        le = LabelEncoder()
        label = Data_train['churn']
        y = le.fit_transform(label)

#SCALING

        # scaler = load('standard_scalar.joblib')
        scaler = StandardScaler()
        scaler.fit(X)
        X_scaled = scaler.transform(X)

#TRAIN TEST SPLIT

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.33, random_state=42)

#MODEL FITTING

        model_name = "Random Forest Classifier"
        RFClassifier = RandomForestClassifier(n_estimators=400, min_samples_split=5, min_samples_leaf=1,
                                                         max_features='sqrt', max_depth=780, criterion='gini',
                                                         random_state=100)
        rfc_model = Pipeline(steps=[('classifier', RFClassifier)])
        rfc_model.fit(X_train, y_train)

#PREDICTIONS

        pred = [State, AccountLength, AreaCode, InternationalPlan, VoiceMail, NumberVoiceMail, TotalDayMinutes,
                TotalDayCalls, TotalDayCharge, TotalEveningMinutes, TotalEveningCalls, TotalEveningCharge,
                TotalNightMinute, TotalNightCalls, TotalNightCharge, TotalInternationalMinute, TotalInternationalCall,
                TotalInternationalCharge, NumberCustomer]

        pred_df = pd.DataFrame([pred], columns=Data_train.columns[:-1])
        pred_df = preproc.fit_transform(pred_df)
        #prediction_data = preproc.fit_transform(prediction_data)
        predictions = rfc_model.predict(scaler.transform(pred_df)) #if pred_df else rfc_model.predict(scaler.transform(prediction_data))
        print(predictions)
    return render(request, 'form1.html', context={})


def FormFileUpload(request):
    upload_file =None
    uploadFile = None
    if request.POST:
        print(request.FILES)

        # LOAD DATA


        Data_train = pd.read_csv('CChurn/Customerchurn.csv')
        # prediction_data = pd.read_csv('whatever.csv')

        # FORMAT DATA

        Data_train['state'] = Data_train['state'].astype('category')
        Data_train['area_code'] = Data_train['area_code'].astype('category')
        Data_train['international_plan'] = Data_train['international_plan'].astype('category')
        Data_train['voice_mail_plan'] = Data_train['voice_mail_plan'].astype('category')

        # DEFINING CATEGORICAL COLS

        categoricalColumns = ['state', 'area_code', 'international_plan', 'voice_mail_plan']
        categorical_columns = []
        categorical_ix = Data_train.select_dtypes(include=['object', 'bool']).columns

        onehotCategorical = preprocessing.OneHotEncoder(handle_unknown='ignore', categories='auto', sparse=False)
        # dump(onehotCategorical, 'onehotCategorical.joblib')
        categorical_transformer = Pipeline(steps=[('onehot', onehotCategorical)])

        cols = ['area_code', 'international_plan', 'voice_mail_plan']
        Data_categorical = Data_train.loc[:, cols]
        Data_categorical['churn'] = Data_train['churn']

        Data_categorical['churn'].replace(to_replace='yes', value=1, inplace=True)
        Data_categorical['churn'].replace(to_replace='no', value=0, inplace=True)

        # ENCODING DATA

        Data_dummies = Data_train.apply(LabelEncoder().fit_transform)
        Data_dummies['churn'] = Data_categorical['churn']

        # DEFINING NUMERICAL COLS

        numericalColumns = Data_train.select_dtypes(include=[np.float, np.int]).columns
        scaler_numerical = StandardScaler()
        numerical_transformer = Pipeline(steps=[('scale', scaler_numerical)])

        preproc = ColumnTransformer(transformers=[('cat', categorical_transformer, categoricalColumns),
                                                  ('num', numerical_transformer, numericalColumns)],
                                    remainder="passthrough")
        Data_churn_pd = preproc.fit_transform(Data_train)

        # DEFINING X AND Y

        X = []
        X = Data_dummies.drop(['churn'], axis=1)
        # X = pd.DataFrame(Data_churn_pd).iloc[:,:-1]

        # labebl_churn = pd.DataFrame(Data_train, columns=['churn'])
        le = LabelEncoder()
        label = Data_train['churn']
        y = le.fit_transform(label)

        # SCALING

        # scaler = load('standard_scalar.joblib')
        scaler = StandardScaler()
        scaler.fit(X)
        X_scaled = scaler.transform(X)

        # TRAIN TEST SPLIT

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.33, random_state=42)

        # MODEL FITTING

        model_name = "Random Forest Classifier"
        RFClassifier = RandomForestClassifier(n_estimators=400, min_samples_split=5, min_samples_leaf=1,
                                              max_features='sqrt', max_depth=780, criterion='gini',
                                              random_state=100)
        rfc_model = Pipeline(steps=[('classifier', RFClassifier)])
        rfc_model.fit(X_train, y_train)

        #UPLOAD DATA
        upload_file = request.FILES['file']
        Data_upload_file = pd.read_csv(upload_file)

        dict_new_upload = []
        for foo in range(0,len(Data_upload_file)):
            dict_new_upload_single ={}
            Data_upload = Data_upload_file.iloc[foo]
            # PREDICTIONS

            pred = [Data_upload['state'], Data_upload['account_length'],Data_upload['area_code'], Data_upload['international_plan'], Data_upload['voice_mail_plan'], Data_upload['number_vmail_messages'], Data_upload['total_day_minutes'],
                    Data_upload['total_day_calls'], Data_upload['total_day_charge'], Data_upload['total_eve_minutes'], Data_upload['total_eve_calls'], Data_upload['total_eve_charge'],
                    Data_upload['total_night_minutes'], Data_upload['total_night_calls'], Data_upload['total_night_charge'], Data_upload['total_intl_minutes'], Data_upload['total_intl_calls'],
                    Data_upload['total_intl_charge'], Data_upload['number_customer_service_calls']]
            #
            print(pred)
            pred_df = pd.DataFrame([pred], columns=Data_train.columns[:-1])
            pred_df = preproc.fit_transform(pred_df)
            # prediction_data = preproc.fit_transform(prediction_data)
            predictions = rfc_model.predict(
                scaler.transform(pred_df))  # if pred_df else rfc_model.predict(scaler.transform(prediction_data))
            print(predictions)
            dict_new_upload_single = {'state':str(Data_upload['state']),'account_length':str(Data_upload['account_length']),'area_code':str(Data_upload['area_code']),'international_plan':str(Data_upload['international_plan']),'voice_mail_plan':str(Data_upload['voice_mail_plan']),
                                      'number_vmail_messages':str(Data_upload['number_vmail_messages']),'total_day_minutes': str(Data_upload['total_day_minutes']), 'total_day_calls' : str(Data_upload['total_day_calls']), 'total_day_charge' :str(Data_upload['total_day_charge']),
                                      'total_eve_minutes' : str(Data_upload['total_eve_minutes']),'total_eve_calls' :  str(Data_upload['total_eve_calls']), 'total_eve_charge' :str(Data_upload['total_eve_charge']),'total_night_minutes' : str(Data_upload['total_night_minutes']),
                                      'total_night_calls' : str(Data_upload['total_night_calls']), 'total_night_charge' : str(Data_upload['total_night_charge']), 'total_intl_minutes' : str(Data_upload['total_intl_minutes']),'total_intl_calls' : str(Data_upload['total_intl_calls']),
                                      'total_intl_charge' : str(Data_upload['total_intl_charge']), 'number_customer_service_calls':str(Data_upload['number_customer_service_calls']),'predictions':str(predictions)}
            dict_new_upload.append(dict_new_upload_single)
        print(dict_new_upload)
        json_format = json.dumps(dict_new_upload)
        json_df = pd.read_json(json_format)
        json_df.to_csv('media/file2.csv',index=False)
        user = UserTable.objects.get(User=request.user)

        uploadFile = FormDataFile.objects.create(UserID=user,File='file2.csv',DateImputed=datetime.datetime.now())

    print(uploadFile)
    return render(request, 'form1.html', context={'uploadFile':uploadFile,'file':upload_file})

def Analysis(request):
    if request.POST:
        print(request.POST)
        uploadFile = FormDataFile.objects.get(id = request.POST['filePath'])
        pd_file = pd.read_csv(uploadFile.File)
        Yes_no = Yes_No(pd_file['predictions'])
        total = len(pd_file)
        totalChurn = Yes_no['yes'] /total*100
        mail_plan_YN = mail_plan(pd_file['voice_mail_plan'])
        theloop = Loop(pd_file)
        print(theloop)
    return render(request, 'chart.html', context={'Yes_no':Yes_no,'total':total,'totalChurn':totalChurn,'mail_plan_YN':mail_plan_YN, 'DataLoop':theloop})

def Yes_No(pd_file):
    print('hello')
    no=0
    yes = 0
    for foo in pd_file:
        if foo =='[0]':
            no = no+1
        elif foo == '[1]':
            yes = yes + 1
    return {
        'no':no,
        'yes':yes
    }
def mail_plan(pd_file):
    print('hello')
    no=0
    yes = 0
    for foo in pd_file:
        foo = foo.lower()
        if foo =='yes':
            no = no+1
        elif foo == 'no':
            yes = yes + 1
    return {
        'no':no,
        'yes':yes
    }

def Loop(pd):
    i = 0
    Day = 0
    Evening=0
    Night=0
    International=0
    CallDay = 0
    CallEvening=0
    CallNight=0
    CallInternational=0
    International_plan_Yes=0
    International_plan_No=0
    for i in range(len(pd)):
        Data = pd.iloc[i]
        Day = Day + Data['total_day_charge']
        Evening = Evening + Data['total_eve_charge']
        Night = Night + Data['total_night_charge']
        International = International + Data['total_intl_charge']
        CallDay = CallDay + Data['total_day_calls']
        CallEvening = CallEvening + Data['total_eve_calls']
        CallNight = CallNight + Data['total_night_calls']
        CallInternational = CallInternational + Data['total_intl_calls']
        mailtolower = Data['international_plan'].lower()
        if mailtolower == 'yes':
            International_plan_Yes =International_plan_Yes+1
        elif mailtolower =='no':
            International_plan_No = International_plan_No +  1
    return {
        'charge'  : {
            'Day': Day,
            'Evening':Evening,
            'Night':Night,
            'International':International
        },
        'calls'  : {
            'Day': CallDay,
            'Evening':CallEvening,
            'Night':CallNight,
            'International':CallInternational
        },
        'International_plan': {
            'yes':International_plan_Yes,
            'no':International_plan_No
        }
    }