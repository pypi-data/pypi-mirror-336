import pandas as pd
import matplotlib.pyplot as plt
import os
import re

def extract_distributions(input_directory, output_directory):
    data_dict = {}
    
    for filename in os.listdir(input_directory):
        if filename.startswith("scenario_layer") and filename.endswith(".csv"):
            file_path = os.path.join(input_directory, filename)
            df = pd.read_csv(file_path)
            
            match = re.match(r'scenario_layer_(\d+)_head_(\d+)\.csv', filename)
            if match:
                layer_num = int(match.group(1)) + 1
                head_num = int(match.group(2)) + 1
                new_column_name = f"layer {layer_num} - head {head_num}"
                data_dict[new_column_name] = df['Chirp_Start_Time_Pred']
    
    combined_df = pd.DataFrame(data_dict)
    output_csv_path = os.path.join(output_directory, 'combined_chirp_start_times.csv')
    combined_df.to_csv(output_csv_path, index=False)
    
    plt.figure(figsize=(10, 6))
    for column in combined_df.columns:
        plt.hist(combined_df[column].dropna(), bins=30, alpha=0.5, label=column)

    plt.title('Distribution of Chirp Start Time Predictions')
    plt.xlabel('Chirp Start Time Predicted')
    plt.ylabel('Frequency')
    plt.legend(title='File Name')

    output_plot_path = os.path.join(output_directory, 'chirp_start_time_distribution.png')
    plt.savefig(output_plot_path)
    plt.close()

    print(f"Combined CSV file saved to: {output_csv_path}")
    print(f"Distribution plot saved to: {output_plot_path}")