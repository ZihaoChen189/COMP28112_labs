"""The description of the mysession2.py:
(By the way, the word "common" in the code and comments during this file meant "the slot held by both hotel and band")
To run this client, a folder containing api.ini, exception.py, reservationapi.py, mysession1.py and mysession2.py should be opened in the terminal.
Then, using "python3 mysession2.py" executed this python client and returned the earliest and common slot.

For the implementation, the COMMON requirement was satisfyed through the math interaction operation with sorted() function.
After importing configuration files and requesting the hotel and band objects:
Firstly, current held hotel slots and current held band slots were obtained through "hotel.get_slots_held()" and "band.get_slots_held()" and 
the main idea of finding the earliest and common slot was optimizing and updating them through better() function but with two times for the recheck,
then the interaction() was used to get that best reservation plan as the result.

In terms of detailed information for the better(), 
firstly, as requested, 
available hotel slots and available band slots were obtained, and we used interaction() and [:20] to catch the first 20 slots.
Secondly, we should check every slot in these 20 slots, since they are(pair) probably better than current common held slots and we could do the update,
or there just was not a reasonable reservation found in the current common held slots for hotel and band and we could do the add operation.
For each considered slot in these 20 ones: 
we need to delete useless slots for current held slots for hotel and band, which were not common, and remove them also on the arguemnt in TWO for loops.
If the two delete operation both on the server and on the argument were designed in one for loop, it may casue confused bugs.
Then, the first if statement was considered to catch the current common held slot(but it just work in few times because of hard condition but it will work in re-check), 
the second if statement was significent: a new variable "current_best" would record the best and reasonable slot, and 
did the RESERVATION request to the server and add this slot on the arugument (current held slots both for hotel and band)
After obtaining one satisfying solution, break this for loop since we already found the best one, 
however, another if statement for "len(solution_temp) != 1:" was considered for the new sorted and updated "hotel_slots" and "band_slots" of common slots
to delete the extra solution in the end of the solution, only keeping one.

This function would execute twice to find a satisfying reservation plan with re-check.
"""

# import implemented files
import reservationapi
import configparser
from exceptions import SlotUnavailableError


# The requirement of the "earliest and same" slot was implemented through the "interaction set" in the math.
def interaction(slot_one, slot_two):
    return sorted(set(slot_one) & set(slot_two))  # interaction


# the MAIN optimization function
def better(hotel, band, hotel_slots, band_slots):
    # check available slots both for the hotel and the band then print the first 20 slots
    print("[INFO] get available slots for both hotel and band...")
    available_hotel_slots = hotel.get_slots_available()
    available_band_slots = band.get_slots_available()
    # get common slots 
    common_slots = interaction(available_hotel_slots, available_band_slots)[:20]  # the first 20 available slots
    print(f"[INFO] the first 20 common and available slots: {common_slots}")
    
    # for each slot in these first 20 slots:
    for each_ready_slot in common_slots:
        # OK, now check whether "hotel_slots" and "band_slots" (arguments) could derive a reasonable common slot 
        current_common_slots = interaction(hotel_slots, band_slots)
        print(f"[INFO] current common slots held: {current_common_slots}")  # MAYBE just null list []

        hotel_remove = []  # temporarily store deleted hotel slots in a list 
        for slot in hotel_slots:
            # delete the useless hotel slot, which was not the common one
            if slot not in current_common_slots:
                print(f"[INFO] release hotel slot {slot} since it was not in common slots")
                hotel.release_slot(slot)  # DELETE request
                hotel_remove.append(slot)  # add this slot to the preparatory list
        for slot in hotel_remove:  # the delete operation on the argument would be separated from the server operation MUST in TWO for loops
            hotel_slots.remove(slot)  # remove this slot in the argument

        band_remove = []  # temporarily store deleted band slots in a list 
        for slot in band_slots:
            # delete the useless band slot, which was not the common one
            if slot not in current_common_slots:
                print(f"[INFO] release band slot {slot} since it was not in common slots")
                band.release_slot(slot)  # DELETE request
                band_remove.append(slot)  # add this slot to the preparatory list
        for slot in band_remove:  # the delete operation on the argument would be separated from the server operation MUST in TWO for loops
            band_slots.remove(slot)  # remove this slot in the argument

        # this was a very very large float
        current_best = float("inf")
        if len(current_common_slots) != 0:  # if current COMMON held slots was not empty, this current_best could be improved directly!
            current_best = current_common_slots[0]  # update
        if each_ready_slot < current_best:  # SECOND if the first 20 slots was even better than the "current_best", which may be inf float, may be current_common_slots[0], or anyone in the fitst 20 common slots
            print(f"[INFO] better slot was found: {each_ready_slot}")
            
            # reserving this slot......
            try:
                print(f"[INFO] trying to book hotel slot: {each_ready_slot}")
                hotel.reserve_slot(each_ready_slot)  # POST the hotel slot to the server
            except SlotUnavailableError:
                print(f"[WARN] cannot reserve this hotel slot: {each_ready_slot}, try next one")  # error
                continue  # TRY next each_ready_slot in the for loop
            else:
                hotel_slots.append(each_ready_slot)  # add this in the argument

            try:
                print(f"[INFO] trying to book band slot: {each_ready_slot}")
                band.reserve_slot(each_ready_slot)  # POST the band slot to the server
            except SlotUnavailableError:
                print(f"[WARN] cannot reserve this band slot: {each_ready_slot}, try next one")  # error
                continue  # TRY next each_ready_slot in the for loop
            else:
                band_slots.append(each_ready_slot)  # add this in the argument
                
            break  # BREAK this for loop, since the best slot with small value already been caught 
        
        else:
            print(f"[INFO] there was no better slot found, the client would keep using {current_best}")  # special case
            break  # no matter what slot would be found, the current COMMON slot was the best one and remaining slots in first 20 were not considered

    solution_temp = interaction(hotel_slots, band_slots)  # the argument was updated through remove() or append() slots
    print(f"[INFO] THE current common slot: {solution_temp}")  # check what was the solution (maybe held more than one common solution) 

    if len(solution_temp) != 1:  # the final answer length should only be one:
        extra_slot = solution_temp[-1]  # delete from the end (this solution had been ordered)

        print(f"[INFO] release hotel slot {extra_slot}, since already found better slot {solution_temp[0]}")  # delete the extra one 
        hotel.release_slot(extra_slot)  # delete hotel slot in the server
        hotel_slots.remove(extra_slot)  # for the argument

        print(f"[INFO] release band slot {extra_slot}, since already found better slot {solution_temp[0]}")  # delete the extra one 
        band.release_slot(extra_slot)  # delete band slot in the server
        band_slots.remove(extra_slot)  # for the argument

    return hotel_slots, band_slots  # updated arguments as the result after the optimization


# the MAIN program start # 
# configuration:
config = configparser.ConfigParser()
config.read("api.ini")
hotel = reservationapi.ReservationApi(config['hotel']['url'],
                                      config['hotel']['key'],
                                      int(config['global']['retries']),
                                      float(config['global']['delay']))
band = reservationapi.ReservationApi(config['band']['url'],
                                     config['band']['key'],
                                     int(config['global']['retries']),
                                     float(config['global']['delay']))

print("[INFO] check the reservation situation of this client...")
hotel_slots = hotel.get_slots_held()
print(f"[INFO] current held slots for hotel: {hotel_slots}")  # print the hotel held slots
band_slots = band.get_slots_held()
print(f"[INFO] current held slots for band: {band_slots}")  # print the band held slots

# execute the optimization program to find an earliest and common slot
# while loop was considered once there was no available slot in the server
while True:
    hotel_slots, band_slots = better(hotel, band, hotel_slots, band_slots)
    print("### SECOND CHECK ###")
    hotel_slots, band_slots = better(hotel, band, hotel_slots, band_slots)  # recheck at least once for better bookings
    final_solution = interaction(hotel_slots, band_slots)  # final interaction of two lists
    if len(final_solution) == 1:  # find and catch that best solution 
        print(f"[INFO] reserved successfully for: {final_solution[0]}")
        break  # BREAK the while loop, finding the best slot as a solution
