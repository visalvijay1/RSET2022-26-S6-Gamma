import wfdb
import os
import pandas as pd
import numpy as np

# Input and output directories
input_dir = r"C:\Users\USER\Desktop\A_final_data\Healthy"  # Folder containing .bin and .hea files
output_dir = r"C:\Users\USER\Desktop\A_final_data\healthy_csv" # Folder for processed CSVs
os.makedirs(output_dir, exist_ok=True)

# Get list of all .bin files (ignoring .hea files)
bin_files = [f for f in os.listdir(input_dir) if f.endswith(".bin")]

for bin_file in bin_files:
    file_path = os.path.join(input_dir, bin_file[:-4])  # Remove .bin extension
    
    try:
        # Read record using WFDB
        record = wfdb.rdrecord(file_path)
        
        # Extract signals and metadata
        signals = record.p_signal.astype(float)  # Ensure numeric type
        fs = record.fs  # Sampling frequency
        channel_names = record.sig_name  # Signal names
        
        # Convert to DataFrame
        df = pd.DataFrame(signals, columns=channel_names)
        
        # Add time column
        time = np.arange(df.shape[0]) / fs
        df.insert(0, "Time (s)", time)
        
        # Save as CSV
        output_filename = f"{bin_file.replace('.bin', '.csv')}"
        df.to_csv(os.path.join(output_dir, output_filename), index=False)
        
        print(f"Processed {bin_file} -> {output_filename}")
    
    except Exception as e:
        print(f"Error processing {bin_file}: {e}")

print("✅ Processing complete! All .bin files have been converted to CSV.")
