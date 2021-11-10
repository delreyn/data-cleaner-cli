#!/usr/bin/python3
'''
Author: reyne Jasson
date: 10/10/2021

A CLI module using click for simple dataset exploration with the dataquest.io webscraped dataset
'''

import pandas as pd
import click

def load_data(file:str = 'autos.csv',encond:str='Latin-1') -> pd.DataFrame:
    '''Reads a csv of given enconding and returns the dataframe'''
    dataframe_autos = pd.read_csv(file,encoding=encond)

    return dataframe_autos.copy()


@click.command()
@click.option("--encond",default="Latin-1",type=str,
                help="Provide the char .csv enconding",show_default=True)
@click.option("--file",default="autos.csv",type=str,
                help="provide the dataset csv",show_default=True)
def process(encond="Latin-1",file="autos.csv"):
    """The data will be processed and info will be displayed"""

    autos = load_data(file,encond)

    autos.replace(to_replace=r'([,$])|km' ,value='',
                    inplace=True,regex=True)

    autos.rename(columns=dict(yearOfRegistration = 'registration_year',
                            monthOfRegistration = 'registration_month',
                            notRepairedDamage = 'unrepaired_damage',
                            dateCreated = 'ad_created',
                            odometer = 'odometer_km'), inplace=True)

    autos['odometer_km'] = pd.to_numeric(autos['odometer_km'])
    autos['price'] = pd.to_numeric(autos['price'])

    ##

    autos = autos[autos["price"].between(1,351000)]
    autos = autos[autos["registration_year"].between(1900,2016)]
    ## Most common brands
    brand_counts = autos["brand"].value_counts(normalize=True)


    selected_brands = brand_counts[brand_counts >= .05].index

    print(f"The brands are: {selected_brands}")

    autos = autos.query('brand in @selected_brands')


    mean_prices = autos.groupby('brand')\
                    .mean()['price'].to_dict()

    mean_mileage = autos.groupby('brand')\
                    .mean()['odometer_km'].to_dict()


    mean_mileage = pd.Series(mean_mileage)
    mean_prices = pd.Series(mean_prices)

    autos_infos = pd.DataFrame(mean_mileage,columns=['mean_mileage'])
    autos_infos.insert(1,"mean_prices",mean_prices,True)

    print("here's the data:\n")
    print(autos_infos.to_string()+"\n")

    convert_flag  = click.confirm("Convert data to csv?",default=True)


    if convert_flag:
        autos.to_csv('autos_infos.csv',index=False)



    #print(autos_infos.to_string())

process()
