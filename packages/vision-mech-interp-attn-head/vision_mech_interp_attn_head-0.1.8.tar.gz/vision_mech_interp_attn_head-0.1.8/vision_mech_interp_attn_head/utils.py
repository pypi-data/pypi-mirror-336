import os
import pandas as pd
import re

def combine_csv_files(input_directory, output_directory):
    data_dict = {}
    
    for filename in os.listdir(input_directory):
        if filename.startswith("scenario_") and filename.endswith(".csv"):
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
    
    return output_csv_path