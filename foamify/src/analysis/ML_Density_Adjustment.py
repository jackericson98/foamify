from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from joblib import dump, load
import pandas as pd

# Load the dataset
file_path = '../Data/density_adjustments.txt'
data = pd.read_csv(file_path, sep=' ', header=None)

# Assign the columns
data.columns = ['Adjusted Density', 'Mean', 'CV', 'Number', 'Set Density', 'Distribution', 'Overlap', 'PBC']

# Change the PBC data to integer
data['PBC'] = data['PBC'].astype(int)

# One-hot encode the 'distribution' column
# Define the ColumnTransformer to handle the encoding of categorical variables
preprocessor = ColumnTransformer(
    transformers=[
        ('dist', OneHotEncoder(), ['Distribution'])  # Apply OneHotEncoder to the 'distribution' column
    ],
    remainder='passthrough'  # Keep all other columns unchanged
)

# Create a pipeline that includes preprocessing, polynomial features, and the regressor
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('poly', PolynomialFeatures(degree=2)),  # Add polynomial features
    ('regressor', LinearRegression())
])

# Separate the features and the target variable
X = data.drop('Set Density', axis=1)
y = data['Set Density']

# Fit the pipeline
pipeline.fit(X, y)

# Save the pipeline
dump(pipeline, '../Data/linreg_pipeline.pkl')
