# %%
import dotenv
import os
import datetime
from collect import Collect
from sender import Sender
import time

dotenv.load_dotenv()
BUCKET_NAME = os.getenv('BUCKET_NAME')
# %%

while True:
    print('Iniciando processo...')
    print('Coletando dados...')
    colect_data = Collect(year=[datetime.datetime.now().year])
    colect_data.process_years()
    print('Enviando dados...')
    send_data = Sender(bucket_name=BUCKET_NAME, bucket_folder='f1/results')
    send_data.process_folder('data')
    print('Iteração finalizada.')
    time.sleep(60*60*6)
# %%
