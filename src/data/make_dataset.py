# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import numpy as np


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    
    logger.info('iniciando análise de arquivo original')

    df = pd.read_csv(input_filepath)

    logger.info('transformando texto em caixa baixa')

    df_transformed = df.copy()
    df_transformed = df_transformed.astype(str).apply(lambda x: x.str.lower())

    df_transformed.drop('rating', axis=1, inplace=True)
    df_transformed.drop('Number of Ratings', axis=1, inplace=True)
    df_transformed.drop('Number of Reviews', axis=1, inplace=True)
    df_transformed.drop('msoffice', axis=1, inplace=True)
    df_transformed.drop('processor_gnrtn', axis=1, inplace=True)

    df_transformed['ram_gb'] = df_transformed['ram_gb'].replace({' gb':''}, regex=True)
    df_transformed['ssd'] = df_transformed['ssd'].replace({' gb':''}, regex=True)
    df_transformed['graphic_card_gb'] = df_transformed['graphic_card_gb'].replace({' gb':''}, regex=True)
    df_transformed['hdd'] = df_transformed['hdd'].replace({' gb':''}, regex=True)

    df_transformed['warranty'] = df_transformed['warranty'].replace({' (years|year)':''}, regex=True)

    df_transformed['warranty'] = df_transformed['warranty'].replace({'no warranty':'0'}, regex=True)
    df_transformed['Touchscreen'] = df_transformed['Touchscreen'].replace({'no':'0'}, regex=True)
    df_transformed['Touchscreen'] = df_transformed['Touchscreen'].replace({'yes':'1'}, regex=True)

    df_transformed['ram_gb'] = pd.to_numeric(df_transformed['ram_gb'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['hdd'] = pd.to_numeric(df_transformed['hdd'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['ssd'] = pd.to_numeric(df_transformed['ssd'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['graphic_card_gb'] = pd.to_numeric(df_transformed['graphic_card_gb'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['warranty'] = pd.to_numeric(df_transformed['warranty'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['Touchscreen'] = pd.to_numeric(df_transformed['Touchscreen'], errors='coerce').fillna(0).astype(np.int64)
    df_transformed['Price'] = pd.to_numeric(df_transformed['Price'], errors='coerce').fillna(0).astype(np.int64)

    replace_dict = {'mac': 'other', 'dos': 'other'}
    df_transformed['os'].replace(replace_dict, inplace=True)

    replace_dict = {'lpddr4x': 'other', 'lpddr4': 'other', 'lpddr3': 'other', 'ddr5': 'other', 'ddr3': 'other'}
    df_transformed['ram_type'].replace(replace_dict, inplace=True)

    replace_dict = {'core i9': 'other', 'pentium quad': 'other', 'm1': 'other', 'celeron dual': 'other', 'ryzen 9': 'other', 'ryzen 3': 'other'}
    df_transformed['processor_name'].replace(replace_dict, inplace=True)

    replace_dict = {'acer': 'other', 'msi': 'other', 'apple': 'other', 'avita': 'other'}
    df_transformed['brand'].replace(replace_dict, inplace=True)

    df_transformed.drop_duplicates(inplace=True)

    df_transformed.to_csv(output_filepath, index=False)

    logger.info('processo concluído')

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
