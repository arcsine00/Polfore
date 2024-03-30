import time
import schedule

import generators

GRAPHEE = {}
file = 'lib/data.json'
ARRAY_FOR_PLOT = []

schedule.every(20).seconds.do(generators.dataGrabber, GRAPHEE, file, ARRAY_FOR_PLOT, 'www/test.html')

while True:
    schedule.run_pending()
    time.sleep(1)
