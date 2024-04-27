import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Visualizer:
    def __init__(self, dataframe):
        self.df = dataframe

    def max_calls_per_client_vis(self):
        # Ensure the datetime format is correct
        self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'] = pd.to_datetime(self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'], dayfirst=True)

        # Group by client number and count the number of calls for each client
        client_calls = self.df.groupby('ΚΛΗΘΕΙΣ ΑΡΙΘΜΟΣ').size()

        # Divide the clients into two groups
        calls_up_to_100 = client_calls[client_calls <= 100]
        calls_above_100 = client_calls[client_calls > 100]

        # Plot for clients with up to 100 calls
        plt.figure(figsize=(15, 8))
        barplot_100 = sns.barplot(x=calls_up_to_100.index, y=calls_up_to_100.values, palette='BuPu')
        plt.title('Σύνολο Κλήσεων ανά πελάτη(0-100 Κλήσεις)')
        plt.xlabel('Αριθμός Πελάτη')
        plt.ylabel('Σύνολο Κλήσεων')
        self.annotate_bars(barplot_100)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

        # Plot for clients with more than 100 calls
        plt.figure(figsize=(15, 8))
        barplot_101 = sns.barplot(x=calls_above_100.index, y=calls_above_100.values, palette='BuPu')
        plt.title('Σύνολο Κλήσεων ανά πελάτη(100+ Κλήσεις)')
        plt.xlabel('Αριθμός Πελάτη')
        plt.ylabel('Σύνολο Κλήσεων')
        self.annotate_bars(barplot_101)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def annotate_bars(self, barplot):
        for p in barplot.patches:
            barplot.annotate(format(p.get_height(), '.1f'), 
                             (p.get_x() + p.get_width() / 2., p.get_height()), 
                             ha = 'center', va = 'center', 
                             xytext = (0, 9), 
                             textcoords = 'offset points')


    def call_times_vis(self):
        # Ensure the datetime column is in the correct datetime format
        self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'] = pd.to_datetime(self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'], dayfirst=True)

        # Calculate the number of weeks in the dataset to average the data correctly
        num_weeks = np.ceil((self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].max() - self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].min()).days / 7)

        # Extract day of the week (Monday=0, Sunday=6) and time
        self.df['Day of Week'] = self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.dayofweek
        self.df['Hour'] = self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.hour

        # Create a pivot table counting the number of calls per hour for each day of the week
        # and then divide by the number of weeks to get the average
        pivot_table = self.df.pivot_table(index='Hour', columns='Day of Week', aggfunc='size', fill_value=0) / num_weeks

        # Ensure the pivot table includes the correct hours range from 9 to 21
        hours = np.arange(9, 21)
        pivot_table = pivot_table.reindex(hours)

        # Plot
        plt.figure(figsize=(25, 12))
        heatmap = sns.heatmap(pivot_table, cmap='BuPu', annot=True, linewidths=.3, fmt='.1f')

        # Set the x-axis to show each weekday
        days = ['Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη', 'Παρασκευή']
        heatmap.set_xticklabels(days)

        # Set the y-axis to show hours
        heatmap.set_yticklabels(['{:02d}:00'.format(hour) for hour in hours], rotation=0)

        # Adding labels and title
        plt.xlabel('Ημέρα')
        plt.ylabel('Ώρα')
        plt.title('Θερμικός Χάρτης Μέσης Συχνότητας Κλήσεων ανά Ώρα και Ημέρα')

        plt.show()



    def first_week_calls_vis(self):
        # Filter data for the first seven days of the month
        self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'] = pd.to_datetime(self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'])
        first_week_filter = (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.day <= 7) & (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.dayofweek < 5)
        df_first_week = self.df[first_week_filter]
        grouped_calls = df_first_week.groupby([df_first_week['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.date, 'ΚΛΗΘΕΙΣ ΑΡΙΘΜΟΣ']).size().unstack(fill_value=0)

        # To select only the first 5 weekdays, you would further filter the grouped data
        weekday_dates = df_first_week['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.date.unique()[:5]
        grouped_calls = grouped_calls.loc[grouped_calls.index.isin(weekday_dates)]

        # Plotting with heatmap
        plt.figure(figsize=(25, 12))  # Adjust the size as needed
        sns.set_theme(font_scale=0.7)  # Adjust font scale to fit the annotations

        # Create the heatmap with a threshold for annotations
        threshold = 5  # Set a threshold for annotations
        annot_array = grouped_calls.applymap(lambda x: str(x) if x >= threshold else "")
        
        # Use a different color palette if necessary
        sns.heatmap(grouped_calls, annot=annot_array, fmt="s", cmap='BuPu', linewidths=.5)

        plt.title('Θερμικός Χάρτης Κλήσεων ανά ημέρα για κάθε Πελάτη(1η Εβδομάδα του Μήνα)')
        plt.xlabel('Αριθμός Πελάτη')
        plt.ylabel('Ημερομηνία')
        
        # Rotate the x and y axis labels if necessary
        plt.yticks(rotation=0)
        plt.xticks(rotation=90)  # Rotate to vertical if needed
        
        plt.tight_layout()  # Adjust the layout
        plt.show()



    def second_week_calls_vis(self):
        # Filter data for the first seven days of the month
        self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'] = pd.to_datetime(self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'])
        second_week_filter = (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.day > 7) & (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.day <= 14) & (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.dayofweek < 5)
        df_second_week = self.df[second_week_filter]
        grouped_calls = df_second_week.groupby([df_second_week['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.date, 'ΚΛΗΘΕΙΣ ΑΡΙΘΜΟΣ']).size().unstack(fill_value=0)

        # To select only the first 5 weekdays, you would further filter the grouped data
        weekday_dates = df_second_week['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.date.unique()[:5]
        grouped_calls = grouped_calls.loc[grouped_calls.index.isin(weekday_dates)]

        # Plotting with heatmap
        plt.figure(figsize=(25, 12))  # Adjust the size as needed
        sns.set_theme(font_scale=0.7)  # Adjust font scale to fit the annotations

        # Create the heatmap with a threshold for annotations
        threshold = 5  # Set a threshold for annotations
        annot_array = grouped_calls.applymap(lambda x: str(x) if x >= threshold else "")
        
        # Use a different color palette if necessary
        sns.heatmap(grouped_calls, annot=annot_array, fmt="s", cmap='BuPu', linewidths=.5)

        plt.title('Θερμικός Χάρτης Κλήσεων ανά ημέρα για κάθε Πελάτη(2η Εβδομάδα του Μήνα)')
        plt.xlabel('Αριθμός Πελάτη')
        plt.ylabel('Ημερομηνία')
        
        # Rotate the x and y axis labels if necessary
        plt.yticks(rotation=0)
        plt.xticks(rotation=90)  # Rotate to vertical if needed
        
        plt.tight_layout()  # Adjust the layout
        plt.show()

    def third_week_calls_vis(self):
        # Filter data for the first seven days of the month
        self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'] = pd.to_datetime(self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'])
        third_week_filter = (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.day > 14) & (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.day <= 21) & (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.dayofweek < 5)
        df_third_week = self.df[third_week_filter]
        grouped_calls = df_third_week.groupby([df_third_week['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.date, 'ΚΛΗΘΕΙΣ ΑΡΙΘΜΟΣ']).size().unstack(fill_value=0)

        # To select only the first 5 weekdays, you would further filter the grouped data
        weekday_dates = df_third_week['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.date.unique()[:5]
        grouped_calls = grouped_calls.loc[grouped_calls.index.isin(weekday_dates)]

        # Plotting with heatmap
        plt.figure(figsize=(25, 12))  # Adjust the size as needed
        sns.set_theme(font_scale=0.7)  # Adjust font scale to fit the annotations

        # Create the heatmap with a threshold for annotations
        threshold = 5  # Set a threshold for annotations
        annot_array = grouped_calls.applymap(lambda x: str(x) if x >= threshold else "")
        
        # Use a different color palette if necessary
        sns.heatmap(grouped_calls, annot=annot_array, fmt="s", cmap='BuPu', linewidths=.5)

        plt.title('Θερμικός Χάρτης Κλήσεων ανά ημέρα για κάθε Πελάτη(3η Εβδομάδα του Μήνα)')
        plt.xlabel('Αριθμός Πελάτη')
        plt.ylabel('Ημερομηνία')
        
        # Rotate the x and y axis labels if necessary
        plt.yticks(rotation=0)
        plt.xticks(rotation=90)  # Rotate to vertical if needed
        
        plt.tight_layout()  # Adjust the layout
        plt.show()

    def last_week_calls_vis(self):
        # Filter data for the first seven days of the month
        self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'] = pd.to_datetime(self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'])
        last_week_filter = (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.day > 21) & (self.df['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.dayofweek < 5)
        df_last_week = self.df[last_week_filter]
        grouped_calls = df_last_week.groupby([df_last_week['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.date, 'ΚΛΗΘΕΙΣ ΑΡΙΘΜΟΣ']).size().unstack(fill_value=0)

        # To select only the first 5 weekdays, you would further filter the grouped data
        weekday_dates = df_last_week['ΗΜΕΡΟΜΗΝΙΑ & ΩΡΑ'].dt.date.unique()[:5]
        grouped_calls = grouped_calls.loc[grouped_calls.index.isin(weekday_dates)]

        # Plotting with heatmap
        plt.figure(figsize=(25, 12))  # Adjust the size as needed
        sns.set_theme(font_scale=0.7)  # Adjust font scale to fit the annotations

        # Create the heatmap with a threshold for annotations
        threshold = 5  # Set a threshold for annotations
        annot_array = grouped_calls.applymap(lambda x: str(x) if x >= threshold else "")
        
        # Use a different color palette if necessary
        sns.heatmap(grouped_calls, annot=annot_array, fmt="s", cmap='BuPu', linewidths=.5)

        plt.title('Θερμικός Χάρτης Κλήσεων ανά ημέρα για κάθε Πελάτη(4η Εβδομάδα του Μήνα)')
        plt.xlabel('Αριθμός Πελάτη')
        plt.ylabel('Ημερομηνία')
        
        # Rotate the x and y axis labels if necessary
        plt.yticks(rotation=0)
        plt.xticks(rotation=90)  # Rotate to vertical if needed
        
        plt.tight_layout()  # Adjust the layout
        plt.show()