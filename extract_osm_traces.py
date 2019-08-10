from requests import get
import os

ENDPOINT = 'https://api.openstreetmap.org/api/0.6/trackpoints?bbox={}&page={}'
DATA_DIR = 'data/'

# coordinates
LEFT_BOTTOM = (35.6060, 51.2086)
RIGHT_TOP = (35.8056, 51.5753)

def get_traces(pages=10):
    area = ','.join(map(str, LEFT_BOTTOM + RIGHT_TOP))
    for i in range(pages):
        url = ENDPOINT.format(area, i)
        rsp = get(url)
        path = os.path.join(DATA_DIR, 'tehran_{}.gpx'.format(i))

        with open(path, 'wb') as f:
            f.write(rsp.content)
        
if __name__ == '__main__':
    get_traces(1)
