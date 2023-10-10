# class SyncService:
#    def sync(self):
#        # Implementação inicial
#        return True

from gcsa.google_calendar import GoogleCalendar

calendar = GoogleCalendar('thiagoarturschumann@gmail.com')


for event in calendar:
    print(event)
