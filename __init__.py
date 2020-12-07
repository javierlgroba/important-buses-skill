from mycroft import MycroftSkill, intent_file_handler
import requests
import json
import sys
from datetime import datetime

class ImportantBuses(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        #self.workBuses = [("106",15184),("204",32062)]
        #self.marthaBuses = [("M46",48027)]
        #self.time = 30
        self.line106 = sys.maxsize
        self.line204 = sys.maxsize
        self.lineM46 = sys.maxsize
        self.lineM462 = sys.maxsize
        self.unknownString = 'unknown time'
        self.singular = 'minute'
        self.plurar = 'minutes'

    @intent_file_handler('important.buses.intent')
    def handle_buses_important(self, message):
        bus_place =  message.data.get('place')
        if bus_place is not None:
            self.log.info(("The place is {}").format(bus_place))
            if (bus_place == 'work'):
                self.get_buses_work()
                text106 = self.unknownString
                text204= self.unknownString
                if self.line106 != sys.maxsize:
                    word = self.plurar
                    if self.line106 == 1:
                        word = self.singular
                    text106 = ('{} minutes').format(self.line106)
                if self.line204 != sys.maxsize:
                    if self.line204 == 1:
                        word = self.singular
                    word = self.plurar
                    text204 = ('{} minutes').format(self.line204)
                self.speak_dialog('buses.to.work', {'L106': text106, 'L204': text204})
            elif (bus_place == 'martha' or bus_place == 'home'):
                self.get_buses_martha()
                textM46 = self.unknownString
                textM462 = self.unknownString
                if self.lineM46 != sys.maxsize:
                    textM46 = ('{}').format(self.lineM46)
                if self.lineM462 != sys.maxsize:
                    if self.lineM462 == 1:
                        word = self.singular
                    word = self.plurar
                    textM462 = ('{} minutes').format(self.lineM462)
                self.speak_dialog('buses.to.martha', {'LM46': textM46, 'LM462': textM462})
            else:
                self.speak_dialog('unknown.place', {'place': bus_place})
        else:
            self.speak_dialog('missed.place')
            

    @intent_file_handler('best.bus.intent')
    def handle_best_bus(self, message):
            self.speak_dialog('best.bus.berlin')

    def get_buses_work(self):
        url = 'https://v5.bvg.transport.rest/stops/900000054109/arrivals?duration=30&remarks=false'
        response = requests.get(url)
        if (response.status_code == 200):
            self.log.info("Received response from BVG")
            jsonResponse = json.loads(response.text)
            now = datetime.now().astimezone()
            for bus in jsonResponse:
                line = bus['line']['name']
                origin = bus['provenance']
                time = bus['when']
                if (origin == 'Lindenhof' and line == '106'):
                    bustime = datetime.fromisoformat(time)
                    time4bus = (bustime - now).seconds / 60
                    minutes = round(time4bus)
                    if time4bus > 0 and self.line106 > minutes:
                        self.line106 = minutes
                        self.log.info(('The bus {} comes in {} minutes').format(line, minutes))
                if (origin == 'S Südkreuz' and line == '204'):
                    bustime = datetime.fromisoformat(time)
                    time4bus = (bustime - now).seconds / 60
                    minutes = round(time4bus)
                    if time4bus > 0 and self.line204 > minutes:
                        self.line204 = minutes
                        self.log.info(('The bus {} comes in {} minutes').format(line, minutes))
        else:
            self.log.error("The BVG server is down")


    def get_buses_martha(self):
        url = 'https://v5.bvg.transport.rest/stops/900000054107/arrivals?duration=30&remarks=false'
        response = requests.get(url)
        if (response.status_code == 200):
            self.log.info("Received response from BVG")
            jsonResponse = json.loads(response.text)
            now = datetime.now().astimezone()
            for bus in jsonResponse:
                line = bus['line']['name']
                origin = bus['provenance']
                time = bus['when']
                if (origin == 'Hertzallee' and line == 'M46'):
                    bustime = datetime.fromisoformat(time)
                    time4bus = (bustime - now).seconds / 60
                    minutes = round(time4bus)
                    if time4bus > 0 and self.lineM46 > minutes:
                        self.lineM46 = minutes
                        self.log.info(('The bus {} comes in {} minutes').format(line, minutes))
                    elif time4bus > 0 and self.lineM462 > minutes:
                        self.lineM462 = minutes
                        self.log.info(('The bus {}-2 comes in {} minutes').format(line, minutes))
        else:
            self.log.error("The BVG server is down")

def create_skill():
    return ImportantBuses()

def stop(self):
    self.stop_beeping()

