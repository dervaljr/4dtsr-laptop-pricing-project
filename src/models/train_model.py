# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, LinearRegression
import joblib
import matplotlib.pyplot as plt
from dvclive import Live


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    with Live() as live:

        logger = logging.getLogger(__name__)
        
        df_transformed = pd.read_csv(input_filepath)
        
        features = list(df_transformed.columns)
        features.remove('Price')

        X = df_transformed[features]
        y = df_transformed['Price']

        X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=0.3, random_state=42)

        model = Ridge()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        live.log_metric('mse', mse, timestamp=True, plot=True)
        live.log_metric('mae', mae, timestamp=True, plot=True)
        live.log_metric('r2', r2, timestamp=True, plot=True)

        plt.scatter(y_test, predictions)
        plt.savefig('./reports/figures/true_vs_prediction.png', dpi=88)

        joblib.dump(model, output_filepath)

        live.log_artifact(output_filepath, type='model', name='laptop-pricing', desc='Modelo de predição de preço de laptop', labels=['regressão'] )

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
