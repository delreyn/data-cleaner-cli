'''
Author: reyne Jasson
date: 10/10/2021

Meu modulo cli

'''

import pandas as pd
import click



def load_data(file:str,encond:str) -> pd.DataFrame:
    '''Reads a csv of given enconding and returns the dataframe'''
    dataframe_autos = pd.read_csv(file,encoding=encond)

    return dataframe_autos.copy()

autos = load_data('autos.csv',encond='Latin-1')

autos.rename(columns=dict(yearOfRegistration = 'registration_year',
                         monthOfRegistration = 'registration_month',
                         notRepairedDamage = 'unrepaired_damage',
                         dateCreated = 'ad_created',
                         odometer = 'odometer_km'), inplace=True)



autos.replace(to_replace=r'[,$km]',value='',inplace=True,regex=True)


autos['odometer'] = pd.to_numeric(autos['odometer'])
autos['price'] = pd.to_numeric(autos['price'])


##

autos = autos[autos["price"].between(1,351000)]
autos = autos[autos["registration_year"].between(1900,2016)]

## Most common brands
brand_counts = autos["brand"].value_counts(normalize=True)
selected_brands = brand_counts[brand_counts > .05].index

autos = autos.query('brand in @selected_brands')

mean_prices = autos.groupby('brand')\
                .mean()['price'].to_dict()

mean_mileage = autos.groupby('brand')\
                .mean()['price'].to_dict()

mean_mileage = pd.Series(mean_mileage)

autos_infos = pd.DataFrame(mean_mileage,columns=['mean_mileage'])




