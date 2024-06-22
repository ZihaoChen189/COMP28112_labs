import requests
import simplejson
import warnings
import time
from requests.exceptions import HTTPError
from exceptions import (
    BadRequestError, InvalidTokenError, BadSlotError, NotProcessedError,
    SlotUnavailableError,ReservationLimitError)


class ReservationApi:
    def __init__(self, base_url: str, token: str, retries: int, delay: float):
        self.base_url = base_url
        self.token    = token
        self.retries  = retries
        self.delay    = delay


    def _reason(self, req: requests.Response) -> str:
        reason = ''
        try:
            json = req.json()
            reason = json['message']
        except simplejson.errors.JSONDecodeError:
            if isinstance(req.reason, bytes):
                try:
                    reason = req.reason.decode('utf-8')
                except UnicodeDecodeError:
                    reason = req.reason.decode('iso-8859-1')
            else:
                reason = req.reason
        return reason


    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}  # the unique API Key


    # a new argument was expanded to record the time of retries
    def _send_request(self, method: str, endpoint: str, try_number: int = 1) -> dict: 
        time.sleep(self.delay)                                                      # DELAY before processing the response to avoid swamping server
        request_help = requests.request(method, endpoint, headers=self._headers())  # perform the request
        code = str(request_help.status_code)                                        # the HTTP response code
        
        if code == "200":                                                           # 200 response indicates all is well - send back the json data
            return request_help.json()                                              # the JSON response body
        
        elif code.startswith("4"):                                                  # the client but meaningful problems 
            reason = self._reason(request_help)                                     # get detailed information
            # raise exceptions according to coursework requirements
            if reason == "Bad request.":
                raise BadRequestError
            elif reason == "The API token was invalid or missing.":
                raise InvalidTokenError
            elif reason == "SlotId does not exist.":
                raise BadSlotError
            elif reason == "The request has not been processed.":
                raise NotProcessedError
            elif reason == "Slot is not available.":
                raise SlotUnavailableError
            elif reason == "The client already holds the maximum number of reservations.":
                raise ReservationLimitError
            else:
                print(f"[ERROR] unexpected message: {reason}, exit")  # .format()
                exit(1)  # kill this client as requested
        
        elif code.startswith("5"):                                                  # a server-side error
            reason = self._reason(request_help)                                     # get detailed information
            warnings.warn(f"[WARN] {reason}, try number: {try_number}")  # warning message
            if try_number != self.retries:                                          # still not reached
                return self._send_request(method, endpoint, try_number + 1)         # call this function again until reaching the limit of retries
            else:
                print(f"[ERROR] retries reached the limit, exit")                   # reach the limited number of retries defined in the api.ini
                exit(1)  # kill this client as requested
                           
        else:
            print(f"[ERROR] unexpected HTTP response code: {code}, exit")  # .format()
            exit(1)  # kill this client as requested
        
    
    def get_slots_available(self):
        dict = self._send_request("GET", f"{self.base_url}/reservation/available")  # GET request with the condition
        return [int(i['id']) for i in dict]  # a list was created using id values in the dictionary


    def get_slots_held(self):
        dict = self._send_request("GET", f"{self.base_url}/reservation")  # GET request
        return [int(i['id']) for i in dict]  # a list was created using id values in the dictionary


    def release_slot(self, slot_id):
        self._send_request("DELETE", f"{self.base_url}/reservation/{slot_id}")  # DELETE request


    def reserve_slot(self, slot_id):
        self._send_request("POST", f"{self.base_url}/reservation/{slot_id}")  # POST request
