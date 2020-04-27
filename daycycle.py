import time
import os

seconds_in_day = 86400
day_length = 7200

def clear(): return os.system('cls' if os.name == "nt" else 'clear')

# while True:
#     mins += 1
#     text = "Current time: \n"
#     text += time.strftime('%H:%M', time.gmtime(mins*60))
#     clear()
#     print(text)
#     time.sleep(sleep)


input("Next full cycle: " + time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime(time.time() + day_length)))
