from datetime import datetime, timedelta
from pytz import timezone
import pytz

x = datetime.strptime("Jan 31 2018 14:40:00", "%b %d %Y %H:%M:%S")
y = datetime.strptime("Mar 31 2018 14:40:00", "%b %d %Y %H:%M:%S")

central = timezone("US/Central")
print x
print central.localize(x)

print y
print central.localize(y)
# print y.astimezone(central)