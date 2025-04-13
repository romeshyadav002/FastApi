import pandas as pd
import io

def filter_csv_by_column(file_bytes, column_name, filter_value):
    df = pd.read_csv(io.BytesIO(file_bytes))
    if column_name not in df.columns:
        return {"error": f"Column '{column_name}' not found."}
    filtered_df = df[df[column_name] == filter_value]
    return filtered_df.to_dict(orient="records")
