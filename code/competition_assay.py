#in this code, the excel and spreadsheet that is added needs to be a single candidate protein and a bunch of bait (or different interactors)
#this code will give a ranekd order of which binds better to one protein than the other 
#the rank is dependent on an initial filter for LIA and LIS, then a second filter for mpDockQ, then a composite probability score based off min max normlazation

#import necessary modules
import pandas as pd
from absl import flags, app, logging
import os

FLAGS = flags.FLAGS
flags.DEFINE_string('name', None, 'Name of the bait to name spreadsheet')
flags.DEFINE_string('csv_path', None, 'CSV spreadsheet from AlphaFold')

def calculate_k(row):
    passed_filters = sum([row['Passed_LIA'], row['Passed_LIS'], row['Passed_mpdockq']])
    if passed_filters == 3:
        return 1.0
    elif passed_filters == 2:
        return 0.75
    elif passed_filters == 1:
        return 0.5
    else:
        return 0.0  # Fails all filters

def main(argv):
    #load data
    csv_path= FLAGS.csv_path
    name = FLAGS.name
    current_directory = os.path.dirname(os.path.abspath(__file__))
    new_directory_name = "ranked_predictions"
    new_directory_path = os.path.join(current_directory, new_directory_name)
    os.makedirs(new_directory_path, exist_ok=True)

    output_file = os.path.join(current_directory, new_directory_name,f"{name}.csv")


    csv_data=pd.read_csv(csv_path)

    #filter metrics
    lia_threshold = 1610
    lis_threshold = 0.073
    mpdock_threshold = 0.175

    csv_data['Passed_LIA'] = csv_data['average lia score'] >= lia_threshold
    csv_data['Passed_LIS'] = csv_data['lis_score'] >= lis_threshold
    csv_data['Passed_mpdockq'] = csv_data['mpDockQ/pDockQ'] >= mpdock_threshold

    #grab weight 
    csv_data['k'] = csv_data.apply(calculate_k, axis=1)
    csv_data.loc[csv_data['k'] == 0, 'Composite_Score'] = 0

    #normalizing score -> min/max
    metrics = ['lis_score', 'average lia score', 'mpDockQ/pDockQ']
    for metric in metrics:
        csv_data[f'Normalized_{metric}'] = (
            (csv_data[metric] - csv_data[metric].min()) / (csv_data[metric].max() - csv_data[metric].min())
        )
    
    #composite score
    csv_data['Composite_Score'] = csv_data['k'] * (
    csv_data['Normalized_lis_score'] + csv_data['Normalized_average lia score'] + csv_data['Normalized_mpDockQ/pDockQ'])

    #adding Rank score as a column
    data = csv_data.sort_values(by='Composite_Score', ascending=False)
    data['Rank'] = range(1, len(data) + 1)

    #creating a new csv file ranking the order of the jobs 
    data.to_csv(output_file, index=False)

if __name__ == "__main__":
    app.run(main)
