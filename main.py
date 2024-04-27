import clean_data
import client_separetor
import visualizer

cleaner = clean_data.DataCleaner(r"C:\Users\jimmy\source\Python Projects\Company Statistics\cdrs.xlsx")
cleaner.drop_columns()
cleaner.time_filter()
cleaner.filter_short_calls(minimum_duration_seconds=4)

max_calls = visualizer.Visualizer(cleaner.df)
max_calls.max_calls_per_client_vis()

calls_plot = visualizer.Visualizer(cleaner.df)
calls_plot.call_times_vis()

first_week_plot = visualizer.Visualizer(cleaner.df)
first_week_plot.first_week_calls_vis()

second_week_plot = visualizer.Visualizer(cleaner.df)
second_week_plot.second_week_calls_vis()

third_week_plot = visualizer.Visualizer(cleaner.df)
third_week_plot.third_week_calls_vis()

last_week_plot = visualizer.Visualizer(cleaner.df)
last_week_plot.last_week_calls_vis()

