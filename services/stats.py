import pandas as pd
import io

def get_csv_statistics(file_bytes):
    df = pd.read_csv(io.BytesIO(file_bytes))
    return {
        "columns": df.columns.tolist(),
        "summary": df.describe().to_dict()
    }
