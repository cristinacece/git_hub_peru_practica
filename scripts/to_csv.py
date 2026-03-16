import json
import pandas as pd
import os

def json_to_csv():
    input_file = "data/users_peru_all.json"
    output_file = "data/users_peru_all.csv"
    
    if not os.path.exists(input_file):
        print(f"File {input_file} not found.")
        return
        
    with open(input_file, "r") as f:
        data = json.load(f)
        
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Converted {len(df)} rows to {output_file}")

if __name__ == "__main__":
    json_to_csv()
