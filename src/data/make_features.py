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

    df_transformed = df.copy()

    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['brand'], prefix='brand')
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['processor_brand'], prefix='processor_brand')
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['processor_name'], prefix='processor_name')

    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['os'], prefix='os')
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['weight'], prefix='weight')
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['warranty'], prefix='warranty')
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['Touchscreen'], prefix='Touchscreen')
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['ram_gb'], prefix='ram_gb')

    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['hdd'], prefix='hdd')
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['ssd'], prefix='ssd')

    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['graphic_card_gb'], prefix='graphic_card_gb')
    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['ram_type'], prefix='ram_type')

    df_transformed = pd.get_dummies(df_transformed, dtype=int, columns=['os_bit'], prefix='os_bit')


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
