from stem.control import Controller
import subprocess
from stem import Signal
from threading import Thread
import queue
import requests
import time
from datetime import datetime
import random
import os
from pymongo import MongoClient
import sys

path, threads, mongo = sys.argv[1], sys.argv[2], sys.argv[3]
client = MongoClient(mongo)
db = client['state']
collection = db['papers']


def generator(path):
    with open(path, 'r') as f:
        for line in f:
            yield dict(line)['paperId']

def initTor(N):
    for i in range(N):
        port = 9050 + 10 * i

        conf = f'''SocksPort {port}
ControlPort {port + 1}
DataDirectory /var/lib/tor{1}
Log notice file /var/log/tor{1}.log'''
        
        with open(os.path.join(os.path.abspath(os.curdir),'data','retrieval','proxies','configs',f'tor_{i}.conf'), 'w') as f:
            f.write(conf)

        tor_command = f'sudo tor -f {os.path.join(os.path.abspath(os.curdir),'data','retrieval','proxies','configs',f'tor_{i}.conf')}'
        subprocess.Popen(tor_command, shell=True, stdout=open(os.path.join(os.path.abspath(os.curdir),'data','retrieval','proxies','logs',f'tor{i}.txt'), 'a'), stderr=open(os.path.join(os.path.abspath(os.curdir),'data','retrieval','proxies','errors',f'tor{i}.txt'), 'a'))

    print('All TOR ports opened.')

class TorThread(Thread):
    def __init__(self, taskq, _id):
        Thread.__init__(self)
        self._id = _id
        self.taskq = taskq
        self.port = (9050 + 10 * _id)
        self.proxy ={"http" : "socks5://localhost:" + str(self.port), "https":"socks5://localhost:"+ str(self.port)}
        self.daemon = True

    def ipchange(self):
        """ Open Tor controller to change IP """
        with Controller.from_port(port = self.port + 1) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

    def request(self, url, attempt=1):
        try:
            time.sleep(2 ** attempt + random.uniform(0,1))
            response = requests.get(url,proxies=self.proxy)
            if response.status_code == 200: 
                return True, None, response.json()
        except Exception as e:
            with open(f'data/retrieval/error/{self._id}.txt','a') as f:
                f.write(f'[{self._id} - {datetime.now()}] {e}')
            return False, attempt + 1, None

    def pipeline(self, url):
        SUCCESS = False
        attempt = 1

        while not SUCCESS:
            if attempt > 5:
                attempt = 1
                self.ipchange()
                print(f'[WARNING - {self._id} - {datetime.now()}] Loop on pipeline.')

            SUCCESS, attempt, response = self.request(f'https://api.semanticscholar.org/graph/v1/paper/{url}?fields=externalIds,url,title,abstract,venue,publicationVenue,year,referenceCount,citationCount,influentialCitationCount,isOpenAccess,fieldsOfStudy,s2FieldsOfStudy,publicationTypes,publicationDate,journal,authors,citations.paperId,references.paperId,embedding.specter_v2',attempt)

        collection.insert_one(response)
        with open(f'data/retrieval/log/{self._id}.txt') as f:
            f.write('%s - THREAD: %s - PORT: %s' % (datetime.now(), self._id, self.port))
        
    def run(self):
        while True:
            try:
                url = self.taskq.get(timeout=1)  # Wait for item
            except queue.Empty:
                break  # Exit if no item for 1 sec

            self.pipeline(url)
            self.taskq.task_done()
            self.ipchange()

class ThreadManager:
    def __init__(self, urls, N):
        self.taskq = queue.Queue()
        self.threads = []
        self.N = N
        for url in urls:
            self.taskq.put(url)

    def start(self):
        for i in range(self.N):
            thread = TorThread(self.taskq,i)
            thread.start()
            self.threads.append(thread)

        self.taskq.join()  

if __name__ == "__main__":
    os.system('sudo killall tor')
    os.system(r'mkdir -p data/retrieval/{error,log,proxies} data/retrieval/proxies/{error,log}')

    initTor(int(threads))
    manager = ThreadManager(generator(path),N=int(threads))
    manager.start()
        
    os.system('sudo killall tor')
    print("Press \"CTRL + C\" to exit")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass