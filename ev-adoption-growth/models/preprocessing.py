import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load_and_preprocess(filepath):
    df = pd.read_csv(filepath)

    # Keep required columns (modify if column names differ)
    df = df[['Year', 'Vehicle Category', 'Sales']]

    df = df.dropna()
    df['Year'] = df['Year'].astype(int)

    # Encode category
    le = LabelEncoder()
    df['Category_Encoded'] = le.fit_transform(df['Vehicle Category'])

    return df, le
