import pandas as pd
import datetime


class DataCleaner:
    def __init__(self, filepath):
        self.df = pd.read_excel(filepath)

    def drop_columns(self):
        # Drop the specified columns from the dataframe
        self.df = self.df.drop(['ΤΥΠΟΣ ΚΛΗΣΗΣ', 'ΤΕΡΜΑΤΙΚΟ', 'ΔΙΚΤΥΟ ΠΡΟΟΡΙΣΜΟΥ', 'ΧΡΕΩΣΗ (€)'], axis=1)
        self.df = self.df.rename(columns={'ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ  (Europe/Athens)': 'ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'})
        
    def time_filter(self):
        # Ensure the datetime column is in the correct datetime format
        self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'] = pd.to_datetime(self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'], dayfirst=True)
        # Apply the weekend filter
        weekend_mask = self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.dayofweek >= 5
        self.df = self.df[weekend_mask == False]  # Keep only non-weekend rows
        # Define the time range outside of which you want to keep calls
        start_time = datetime.datetime.strptime('21:01:00', '%H:%M:%S').time()
        end_time = datetime.datetime.strptime('08:59:00', '%H:%M:%S').time()
        # Apply the time filter
        time_mask = (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.time >= end_time) & (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.time <= start_time)
        self.df = self.df[time_mask]  # Keep rows within the specified time range
        
    def filter_short_calls(self, minimum_duration_seconds=4):
        # Convert duration string to timedelta
        def parse_duration(duration):
            parts = duration.split(':')
            if len(parts) == 3:
                hours, minutes, seconds = parts
                return datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
            return datetime.timedelta(seconds=0)

        self.df['ΔΙΑΡΚΕΙΑ'] = self.df['ΔΙΑΡΚΕΙΑ'].apply(parse_duration)

        # Filter out calls shorter than the minimum duration
        minimum_duration = datetime.timedelta(seconds=minimum_duration_seconds)
        self.df = self.df[self.df['ΔΙΑΡΚΕΙΑ'] >= minimum_duration]