from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
from joblib import dump, load
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '../Data/density_adjustments.txt'
data = pd.read_csv(file_path, sep=' ', header=None)

# Assign the columns
data.columns = ['Adjusted Density', 'Mean', 'CV', 'Number', 'Set Density', 'Distribution', 'Overlap', 'PBC']

# Change the PBC data to integers
data['PBC'] = data['PBC'].astype(int)

# Separate the features and the target variable
X = data.drop('Set Density', axis=1)
y = data['Set Density']

# Define preprocessing for numeric and categorical features
numeric_features = ['Mean', 'CV', 'Number', 'Set Density', 'Overlap', 'PBC']
categorical_features = ['Distribution']

# Preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('poly', PolynomialFeatures(degree=2, include_bias=False)),  # Apply polynomial features to numeric columns
            ('scaler', StandardScaler())  # Normalize numeric columns
        ]), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)  # One-hot encode categorical columns
    ]
)

# Create the full pipeline with the linear regression model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the pipeline
pipeline.fit(X_train, y_train)

# Predict outcomes for the test set
y_pred = pipeline.predict(X_test)

# Calculate evaluation metrics
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r_squared = r2_score(y_test, y_pred)

# Print evaluation metrics
print("Evaluation Metrics:")
print(f"Mean Squared Error (MSE): {mse:.5f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.5f}")
print(f"Mean Absolute Error (MAE): {mae:.5f}")
print(f"R-squared Score: {r_squared:.5f}")

# Plot actual vs predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', label='Predicted vs Actual', alpha=0.7)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Perfect Fit')  # Diagonal line
plt.xlabel('Monte Carlo Density', fontdict=dict(size=25))
plt.ylabel('Predicted Density', fontdict=dict(size=25))
plt.title('Monte Carlo vs Predicted Density', fontdict=dict(size=25))
plt.text(x=0.37, y=0.12, s=f"Mean Squared Error (MSE): {mse:.5f} \nRoot Mean Squared Error (RMSE): {rmse:.5f}\nMean "
                         f"Absolute Error (MAE): {mae:.5f}\nR-squared Score: {r_squared:.5f}", fontdict=dict(size=13))
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=20)
plt.tight_layout()
plt.grid(True)
plt.show()

# Save the pipeline
# dump(pipeline, '../Data/linreg_pipeline.pkl')
