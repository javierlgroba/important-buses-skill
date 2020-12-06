from mycroft import MycroftSkill, intent_file_handler


class ImportantBuses(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('buses.important.intent')
    def handle_buses_important(self, message):
        self.speak_dialog('buses.important')


def create_skill():
    return ImportantBuses()

