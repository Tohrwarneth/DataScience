import requests
import sched, time
from datetime import datetime
from pathlib import Path

s = sched.scheduler(time.time, time.sleep)
waittime = 60
Path("log/").mkdir(parents=True, exist_ok=True)


def requestCPU(sc):
    request = 'http://infbdt01.fh-trier.de:9090/api/v1/query?query=ipmi_temperatures%7bsensor=%20%27CPU%201%20Temp%27%7d'
    r = requests.get(request)

    if (r.status_code != 200):
        print("Webseite nicht erreichbar")
        exit(1)

    body = r.json()['data']

    date = datetime.now().strftime('%Y%m%d%H')
    filename = f'log/templog-{date}'
    f = open(filename, "a")
    f.write(datetime.now().strftime('%H:%M') + '\n')
    text = f'Instance\t\t\t\t\tTimestamp\t\tTemperature\n'
    f.write(text)

    for result in body['result']:
        metric = result['metric']
        instance = metric['instance']
        sensor = metric['sensor']
        timestamp = result['value'][0]
        temperature = result['value'][1]
        text = f'{instance}\t{timestamp}\t{temperature}'
        print(text)
        f.write(text + '\n')
    print('\n---------\n')
    f.write('\n')
    if sc:
        sc.enter(waittime, 1, requestCPU, (sc,))


requestCPU(None)
s.enter(waittime, 1, requestCPU, (s,))
s.run()
