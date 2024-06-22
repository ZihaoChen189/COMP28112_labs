"""The description of the mysession1.py:
(By the way, the word "common" in the code and comments during this file meant "the slot held by both hotel and band")
To run this client, a folder containing api.ini, exception.py, reservationapi.py, mysession1.py and mysession2.py should be opened in the terminal.
Then, using "python3 mysession1.py" started this python client.

Firstly, get_slots_held() and release_slot() were used to simply check whether the client already had the reservation.
If the extra reservation was found, just delete them; or skip this operation.
Then, check available slots, those could be reserved, and return the length of them using get_slots_available().
After that, reserving two slots from these available slots, using reserve_slot(), through the random seed.
When the slot successfully reserved, a list would save it and its length was increased by one to control the time of while loop.
This reservation operation (while loop) would be terminated, when the lenght of this temporary list reached "2".
Finally, using get_slots_held() again and print reserved slots one by one.
"""

import reservationapi
import configparser
import time
import random  
from exceptions import SlotUnavailableError

# Load the configuration file containing the URLs and keys
config = configparser.ConfigParser()
config.read("api.ini")

# Create an API object to communicate with the hotel API
hotel  = reservationapi.ReservationApi(config['hotel']['url'],
                                       config['hotel']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))

random.seed(time.time())  # set the random seed

# get_slots_held() and release_slot() were used #
print("[INFO] check whether this client reservation was clean...")
current_slots = hotel.get_slots_held() 
if len(current_slots) != 0:  # already held
    # delete extra and useless ones before reservation
    for slot in current_slots:  # for loop
        print(f"[INFO] releasing the slot {slot}...")  # .format()
        hotel.release_slot(slot)  # DELETE them one by one before reservation
else:
    print("[INFO] no reservation found, skip release operation")
    
# get_slots_available() was used #
print("[INFO] check current available slots...")
available_slots = hotel.get_slots_available()  # how many available slots do we have
print(f"[INFO] there are {len(available_slots)} slots available")
list = []  # store the information used to control the while loop 

# reserve_slot() was used #
print(f"[INFO] reserve two slots...")
# extra and useless slots had been released before the formal operation!
while True:
        if len(list) == 2:  
            break  # BREAK the while loop if this client already finished two reservations
        
        random_one = random.choice(available_slots)  # just do a random choice for the Task 1 from available slots
        if random_one in list:
            continue  # CONTINUE the while loop, if this slot had been occupied
        
        # reserving......
        try:
            print(f"[INFO] try to reserve the hotel slot: {random_one}")
            hotel.reserve_slot(random_one)  # REAL program for the reservation operation 
        except SlotUnavailableError as e:
            pass
        else:
            list.append(random_one)  # list length++

# get_slots_held() was used # again
print("[INFO] finally check current reservations held by this client...")
solution = hotel.get_slots_held()
for slot in solution:
    print(f"[INFO] final hotel slot held by this client: {slot}")  # print results one by one
