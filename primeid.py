import sys
from time import sleep
import requests as rq
from tqdm import tqdm
import random
import re
import os
import numpy as np
import subprocess
from datetime import datetime as dt

sys.setrecursionlimit(100000)
worker, nodes = sys.argv[1:]
PATH = os.path.join(os.path.abspath(os.curdir),'data')

fieldsOfStudy = [
    'Computer Science',
    'Medicine',
    'Chemistry',
    'Biology',
    'Materials Science',
    'Physics',
    'Geology',
    'Psychology',
    'Art',
    'History',
    'Geography',
    'Sociology',
    'Business',
    'Political Science',
    'Economics',
    'Philosophy',
    'Mathematics',
    'Engineering',
    'Environmental Science',
    'Agricultural and Food Sciences',
    'Education',
    'Law',
    'Linguistics'
]

years = [
    '-2010',
    '2011-2016',
    '2017-2021',
    '2022-'
]

def start_proxy_server():
    tor_port = 9050 + int(worker) + 10*int(worker)

    tor_conf = f'''SocksPort {tor_port}
ControlPort {tor_port-1}
DataDirectory /var/lib/tor{worker}
Log notice file /var/log/tor{worker}.log'''

    with open(os.path.join(PATH,'configs',f'tor_{worker}.conf'), 'w') as f:
        f.write(tor_conf)

    dante_conf = f'''logoutput: stderr
internal: 0.0.0.0 port = {tor_port}
external: eat5G

method: username none
user.notprivileged: nobody

client pass {{
    from: 0.0.0.0/0 to: 0.0.0.0/0
    log: connect disconnect
}}

socks pass {{
    from: 0.0.0.0/0 to: 0.0.0.0/0
    log: connect disconnect
}}'''

    with open(os.path.join(PATH,'configs',f'dante_{worker}.conf'), 'w') as f:
        f.write(dante_conf)

    tor_command = f'sudo tor -f {os.path.join(PATH,'configs',f'tor_{worker}.conf')}'
    tor_process = subprocess.Popen(tor_command, shell=True, stdout=open(os.path.join(PATH,'proxies',f'torlog_{worker}.txt'), 'a'), stderr=open(os.path.join(PATH,'proxies',f'torerr_{worker}.txt'), 'a'))

    dante_command = f'sudo sockd -f {os.path.join(PATH,'configs',f'dante_{worker}.conf')}'
    dante_process = subprocess.Popen(dante_command, shell=True, stdout=open(os.path.join(PATH,'proxies',f'dantelog_{worker}.txt'), 'a'), stderr=open(os.path.join(PATH,'proxies',f'danterr_{worker}.txt'), 'a'))

    proxy_headers = {"http":f"socks5h://127.0.0.1:{tor_port}","https":f"socks5h://127.0.0.1:{tor_port}"}

    print(f"[Proxy {worker} started on port {tor_port}]\n")
    return proxy_headers,tor_process,dante_process

proxy,tor,dante = start_proxy_server()

def connection_test():
    try:
        rq.get("https://www.google.com", proxies=proxy,timeout=(5,15))
        return True
    except:
        return False
    
def request (url, delay=1, attempt=1, max_attempt=10, tol=60):
    # Asegura continuación ante saturaciones de red.
    try:
        sleep(delay)
        response = rq.get(url,proxies=proxy,timeout=(5,15))
        if response.status_code == 200:
            # Retorno de los resultados de la API.
            with open(f'data/logs/delaylog_{worker}.txt','a') as f:
                f.write(f"{delay},{attempt},{url}\n")
                # TEMPORAL: Quiero analizar la saturación de requests al API en su rate limit de 1000 resultados.

            return response.json()
        elif response.status_code != 200 and attempt!=max_attempt:
            # Principalmente maneja errores 429 y 504.
            # Si yo supero el rate limit o el server no responde a tiempo, se aplica exponential backoff + reintento recursivo.
            delay = min(2 ** attempt + random.uniform(0,1), 1024)
            return request(url, delay, attempt=attempt+1, max_attempt=max_attempt)
        else:
            # Registro de error y devolución de bandera 'None'.
            with open(f'data/logs/erroridslog_{worker}.txt','a') as f:
                f.write(f'ERROR {response.status_code} at attempt {attempt}: {url}\n')
            
            return None
        
    # Detiene la función hasta que se haya reconexión.
    except rq.exceptions.RequestException as e:
        with open(f'data/logs/connectionlog_{worker}.txt','a') as f:
            f.write(f'[{dt.now()}] Lost connection. Awaiting reconnection. ({e})\n')
        
        while not connection_test():
            sleep(tol)

        with open(f'data/logs/connectionlog_{worker}.txt','a') as f:
            f.write(f'[{dt.now()}] Reconnected.\n')

        return request(url,delay=delay,attempt=attempt,max_attempt=max_attempt,tol=tol)
    
def stream_overview(response,field,year):
    total = response['total']
    print(f'field: {field}\nyears: {year}\ntotal results: {total}\nestimated amount of paginations: {total//1000 + 1}\nleast amount of processing hours: {(total//1000 + 1)//3600 + 1}')
    
    return tqdm(total=total//1000 + 1,desc='crawled paginations',initial=1,position=1,leave=True)

def fetchIDs(field,year,token=None,pags=None):
    url = f'https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=*&fieldsOfStudy={field}&year={year}' + (f'&token={token}' if token!=None else '')
    response = request(url,max_attempt=20)
    
    if response is not None:        
        # Solo corrido en la primera iteración. De ahí, deriva la barra de progreso recursivamente.
        if pags is None:
            pags = stream_overview(response,field,year)
        else:
            pags.update(1)
        
        # Registro de IDs
        with open(f'data/ids/paperIds_{worker}.txt','a') as f:
            f.write('\n'.join(re.findall(r"\{'paperId': .+?, 'title': '.+?'\}",str(response['data']),re.DOTALL)) + '\n')
        
        # Encontrar nuevo token de paginación, si hay, y continuar recursivamente.
        next_token = response.get('token') 
        if next_token:
            fetchIDs(field,year,token=next_token,pags=pags)
        else:
            pags.close()

if __name__ == '__main__':
    fields = fieldsOfStudy[np.linspace(0,len(fieldsOfStudy),int(nodes)+1,dtype=int)[int(worker)]:np.linspace(0,len(fieldsOfStudy),int(nodes)+1,dtype=int)[int(worker)+1]]

    with tqdm(total=len(fields)*len(years),desc='bulk searches') as pbar:
        for field in fields:
            for year in years:
                fetchIDs(field,year)
                pbar.update(1)

    print('Finished ID retrieval.')

    tor.terminate()
    tor.wait()

    dante.terminate()
    dante.wait()
    print('Dante and Tor process ended.')
    