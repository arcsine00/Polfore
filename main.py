import time
import schedule

from generators import *

serviceList = [['partyApprovalRatings', party_space]]
initList = [initChartBox(i[0], i[1]) for i in serviceList]

schedule.every(3).minutes.do(updateChartBox, initList[0], [0.25, 0.25, 0.25, 0.25])

while True:
    schedule.run_pending()
    time.sleep(1)
