import random
import time
from datetime import datetime

def random_delay():
    time.sleep(random.uniform(8, 15))

def today():
    return datetime.now().strftime("%Y-%m-%d")
import time
import random
from datetime import datetime

def random_delay(min_s=8, max_s=15):
    time.sleep(random.uniform(min_s, max_s))

def today():
    return datetime.now().strftime("%Y-%m-%d")
