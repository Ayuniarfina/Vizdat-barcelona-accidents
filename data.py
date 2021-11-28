import pandas as pd
import numpy as np

def praprocess(df):
    df['isWeekend'] = df['Weekday'].apply(lambda x : 1 if x in ['Saturday', 'Sunday'] else 0)
    
    month = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    df['month'] = df['Month'].map(month)
    df['Month'] = pd.Categorical(df['Month'], categories=month, ordered=True)
    df.sort_values(by=['Month'], inplace=True)
    df['year'] = 2017
    df['Date'] = pd.to_datetime(df[['year', 'month', 'Day']])
    
    index_names = df[ df['District Name'] == 'Unknown' ].index
  
    # drop these row indexes
    # from dataFrame
    df.drop(index_names, inplace = True)
    df = df.replace('Sant Martí','Sant Marti')
    df = df.replace('Sants-Montjuïc','Sants-Montjuic')
    df = df.replace('Sarrià-Sant Gervasi','Sarria-Sant Gervasi')
    df = df.replace('Gràcia','Gracia')
    df = df.replace('Horta-Guinardó','Horta-Guinardo')

    return df

def trend_year(df):    
    g_year = df[['Month', 'Mild injuries', 'Serious injuries', 'Victims']].groupby(['Month']).sum().reset_index()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    g_year['Month'] = pd.Categorical(g_year['Month'], categories=months, ordered=True)
    g_year.sort_values(by=['Month'], inplace=True)
    return g_year
    # plt.figure(figsize=(20,10))

    # plt.style.use('ggplot')
    # g_year.plot('Month', ['Mild injuries', 'Serious injuries', 'Victims'], figsize=(20, 10))
    # plt.title("Trend Kecelakaan di Barcelona pada Tahun 2017")
    # plt.xticks(np.arange(12), months)
    # plt.ylabel('Jumlah Kecelakaan')
    # plt.show()

def trend_month(df, district, month):
    if (district=='All District'):
        if (month=='All'):
            temp = df[['Month', 'Mild injuries', 'Serious injuries', 'Victims']].groupby(['Month']).sum().reset_index()
            # months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            # temp['Month'] = pd.Categorical(temp['Month'], categories=months, ordered=True)
            # temp.sort_values(by=['Month'], inplace=True)
        else:
            temp = df[df['Month']==month]
            temp = temp[['Day', 'Mild injuries', 'Serious injuries', 'Victims']].groupby(['Day']).sum().reset_index()
    else:
        if (month=='All'):
            temp = df[df['District Name']==district]
            temp = temp[['Month', 'Mild injuries', 'Serious injuries', 'Victims']].groupby(['Month']).sum().reset_index()
        else:
            temp = df[(df['Month']==month) & (df['District Name']==district)]
            temp = temp[['Day', 'Mild injuries', 'Serious injuries', 'Victims']].groupby(['Day']).sum().reset_index()

        
        
    temp['total_injuries'] = temp['Mild injuries'] + temp['Serious injuries']
    return temp
    # plt.style.use('ggplot')
    # plt.figure(figsize=(20,10))
    # temp.plot('Day', ['Mild injuries', 'Serious injuries'], figsize=(20, 10))
    # plt.title("Trend Kecelakaan di Barcelona pada Bulan" + month + "Tahun 2017")
    # plt.xticks(df['Day'])
    # plt.ylabel('Jumlah Kecelakaan')
    # plt.show()

def trend_day(df, month, day) :
    temp = df[(df['Month']==month) & (df['Day']==day)]
    temp = temp[['Hour', 'Mild injuries', 'Serious injuries']].groupby(['Hour']).sum().reset_index()
    return temp

    # plt.style.use('ggplot')
    # plt.figure(figsize=(20,10))
    # temp.plot('Hour', ['Mild injuries', 'Serious injuries'], figsize=(20, 10))
    # plt.title("Trend Kecelakaan di Barcelona pada Tanggal " + str(day) + " Bulan " + month + " Tahun 2017")
    # plt.xticks(df['Hour'])
    # plt.ylabel('Jumlah Kecelakaan')
    # plt.show()
    