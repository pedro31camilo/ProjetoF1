# %%
import argparse
import random
import string
import os
import fastf1
import pandas as pd
import time
pd.set_option('display.max_columns', None)

random_user = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@email.com"
random_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

os.environ['F1_USERNAME'] = random_user
os.environ['F1_PASSWORD'] = random_pass
# %%
class Collect:

    def __init__(self, year=[2021, 2022, 2023], modes=['R', 'S']):
        self.year = year
        self.modes = modes

    def get_data(self, year, gp, mode) ->pd.DataFrame:
        try:
            session = fastf1.get_session(year, gp, mode)
        except ValueError as err:
            print(err)
            return pd.DataFrame()
        session._load_drivers_results()
        df = session.results
        df['Mode'] = session.name
        df['Year'] = session.date.year
        df['Date'] = session.date
        df['RoundNumber'] = session.event['RoundNumber']
        df['OfficialEventName'] = session.event['OfficialEventName']
        df['EventName'] = session.event['EventName']
        df['Country'] = session.event['Country']
        df['Location'] = session.event['Location']
        return df

    def save_data(self, df:pd.DataFrame, year:int, gp:int, mode:str):
        filename = f'data/{year}_{gp:02d}_{mode}.parquet'
        df.to_parquet(filename, index=False)

    def process(self, year, gp, mode):
        df = self.get_data(year, gp, mode)
        if df.empty:
            return False
        self.save_data(df, year, gp, mode)
        time.sleep(2)
        return True

    def process_year_modes(self, year):
        for gp in range(1, 50):
            for mode in self.modes:
                if not self.process(year, gp, mode) and mode == 'R':
                    return

    def process_years(self):
        for year in self.year:
            print(f'Coletando dados do ano {year}')
            self.process_year_modes(year)
            time.sleep(10)
# %%
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int)
    parser.add_argument('--stop', type=int)
    parser.add_argument('--years', '-y', nargs='+', type=int)
    parser.add_argument('--modes', '-m', nargs='+', type=str, default=['R', 'S'])

    args = parser.parse_args()

    if args.years:
        collect = Collect(args.years, args.modes)
    elif args.start and args.stop:
        years = list(range(args.start, args.stop + 1))
        collect = Collect(years, args.modes)
    collect.process_years()
# %%
