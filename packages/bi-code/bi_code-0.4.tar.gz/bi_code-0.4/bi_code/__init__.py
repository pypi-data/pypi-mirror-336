
def prac3():
    return """
    #Practical 3:- Perform the data classification using classificaiton algorithm using Python
#Random Forest Classifier

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.datasets import load_iris

data = load_iris()

df = pd.DataFrame(data.data, columns = data.feature_names)

df['target'] = data.target

print(df.head())

X = df.drop('target', axis = 1)
y = df['target']

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

scalar = StandardScaler()
X_train = scalar.fit_transform(X_train)
X_test = scalar.transform(X_test)

model = RandomForestClassifier(n_estimators = 100, random_state = 1)

model.fit(X_train, Y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(Y_test, y_pred)
print(f'Accuracy: {accuracy :.2f}')

print('Classification Report : \n', classification_report(Y_test, y_pred))

conf_matrix = confusion_matrix(Y_test, y_pred)

sns.heatmap(conf_matrix, annot = True, cmap = 'viridis', fmt = 'd')
plt.xlabel('predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

"""

def prac4():
    return """
    import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

# Generate Sample data with 3 clusters
X, y = make_blobs(n_samples=300, centers=3, random_state=1, cluster_std=1.0)

df = pd.DataFrame(X, columns=['Feature1', 'Feature2'])

print(df.head())

scaler = StandardScaler()
X_Scaled = scaler.fit_transform(X)

# Define The number of Clusters
k = 3

kmeans = KMeans(n_clusters=k, random_state=1)
df['Cluster'] = kmeans.fit_predict(X_Scaled)

centers = kmeans.cluster_centers_
plt.figure(figsize=(8, 6))

# Scatter plot of clusters
sns.scatterplot(x=df['Feature1'], y=df['Feature2'], hue=df['Cluster'], palette='coolwarm', s=50)

# Plot Cluster Centers
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='X', s=200, label='Centroids')

plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('K-Means Clustering Visualization')
plt.legend()
plt.show()

# Elbow Method for Optimal k
inertia = []
K_range = range(1, 11)  # This should generate numbers from 1 to 10
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_Scaled)
    inertia.append(kmeans.inertia_)

# Now plot inertia vs number of clusters
plt.figure(figsize=(8, 6))
plt.plot(K_range, inertia, marker='o', linestyle='--')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.show()

"""

def prac5():
    return """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Sample Data (replace this with your warehouse data)
# Assuming 'Quantity' is the independent variable (X) and 'Sales' is the dependent variable (y)
data = {
    'Quantity': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
    'Sales': [200, 250, 300, 350, 400, 450, 500, 550, 600, 650]
}

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Display the first few rows
print(df.head())

# Define the independent variable (X) and dependent variable (y)
X = df[['Quantity']]  # Independent variable (X) - needs to be a 2D array
y = df['Sales']  # Dependent variable (y)

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Linear Regression model
model = LinearRegression()

# Train the model using the training data
model.fit(X_train, y_train)

# Predict on the testing data
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)  # Mean Squared Error
r2 = r2_score(y_test, y_pred)  # R-squared score

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Visualize the data and the regression line
plt.figure(figsize=(8,6))
plt.scatter(X, y, color='blue', label='Actual data')
plt.plot(X, model.predict(X), color='red', label='Regression Line')
plt.xlabel('Quantity')
plt.ylabel('Sales')
plt.title('Linear Regression - Warehouse Data')
plt.legend()
plt.show()

# If you want to predict new values:
new_data = np.array([[60]])  # Example: Predict sales for quantity 60
prediction = model.predict(new_data)
print(f'Predicted sales for quantity 60: {prediction[0]}')


"""

def prac6():
    return """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

# Load the Iris dataset
data = load_iris()

# Create a DataFrame using the Iris data
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# Display the first few rows
print(df.head())

# Define the independent variables (X) and the dependent variable (y)
X = df[data.feature_names]  # Features
y = df['target']  # Target variable (the iris species)

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature Scaling (Standardizing the features to improve performance)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create the Logistic Regression model
model = LogisticRegression(max_iter=200)

# Train the model using the training data
model.fit(X_train_scaled, y_train)

# Predict on the testing data
y_pred = model.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Confusion Matrix (with 'labels' argument to avoid warning)
conf_matrix = confusion_matrix(y_test, y_pred)
print(f'Confusion Matrix:\n{conf_matrix}')

# Classification Report (with 'labels' argument)
class_report = classification_report(y_test, y_pred)
print(f'Classification Report:\n{class_report}')

# Visualize the decision boundary (optional)
plt.figure(figsize=(8, 7))
sns.heatmap(conf_matrix, annot = True, cmap = 'coolwarm')
plt.show()

"""

def prac7():
    return """

import pandas as pd

# Step 1: Read the CSV file into a DataFrame
# Replace 'sales_data.csv' with the path to your actual CSV file
df = pd.read_csv(r'C:\Users\amany\OneDrive\Documents\BI_Practical\Data\sales_data_sample.csv')
#Step 2: Display the first few rows of the dataset to understand its structure
print("First few rows of the dataset:")
print(df.head())

# Step 3: Basic data exploration

# 3.1: Check the basic information about the dataset
print("\nBasic Information about the dataset:")
print(df.info())

# 3.2: Check for any missing values
print("\nMissing values in the dataset:")
print(df.isnull().sum())

# 3.3: Describe the numerical columns to get basic statistics (e.g., mean, median, std, etc.)
print("\nBasic Statistics (Numerical Columns):")
print(df.describe())

# Step 4: Perform some simple data analysis

# 4.1: Total Sales and Profit
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()

print(f"\nTotal Sales: {total_sales}")
print(f"Total Profit: {total_profit}")

# 4.2: Average Sales and Profit per Product
avg_sales_per_product = df.groupby('Product')['Sales'].mean()
avg_profit_per_product = df.groupby('Product')['Profit'].mean()

print("\nAverage Sales per Product:")
print(avg_sales_per_product)

print("\nAverage Profit per Product:")
print(avg_profit_per_product)

# 4.3: Sales and Profit by Category
sales_by_category = df.groupby('Category')['Sales'].sum()
profit_by_category = df.groupby('Category')['Profit'].sum()

print("\nTotal Sales by Category:")
print(sales_by_category)

print("\nTotal Profit by Category:")
print(profit_by_category)

# 4.4: Find the most profitable product
most_profitable_product = df.loc[df['Profit'].idxmax()]
print(f"\nMost Profitable Product:\n{most_profitable_product}")

# Step 5: Generate some simple visualizations

# Plot total sales by category
import matplotlib.pyplot as plt

sales_by_category.plot(kind='bar', title='Total Sales by Category', xlabel='Category', ylabel='Total Sales', color='skyblue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot total profit by category
profit_by_category.plot(kind='bar', title='Total Profit by Category', xlabel='Category', ylabel='Total Profit', color='salmon')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


"""

def prac8a():
    return """

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample Sales Data (replace this with your actual sales data)
data = {
    'Date': pd.date_range(start='2020-01-01', periods=12, freq='M'),
    'Sales': [1500, 2300, 1800, 2500, 2100, 3000, 2700, 3200, 3500, 3700, 3900, 4200],
    'Region': ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West', 'North', 'South', 'East', 'West'],
    'Product Category': ['A', 'B', 'A', 'C', 'B', 'C', 'A', 'C', 'A', 'B', 'C', 'A']
}

# Creating a DataFrame
df = pd.DataFrame(data)

# Display the first few rows of the DataFrame
print(df.head())

# Visualization 1: Sales Trend over Time (Line Plot)
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Sales'], marker='o', linestyle='-', color='b')
plt.title('Sales Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Visualization 2: Sales by Region (Bar Plot)
plt.figure(figsize=(10, 6))
sns.barplot(x='Region', y='Sales', data=df, palette='Set2')
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Sales')
plt.tight_layout()
plt.show()

# Visualization 3: Sales Distribution by Product Category (Box Plot)
plt.figure(figsize=(10, 6))
sns.boxplot(x='Product Category', y='Sales', data=df, palette='Set1')
plt.title('Sales Distribution by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Sales')
plt.tight_layout()
plt.show()

# Visualization 4: Heatmap for Sales Correlation (if you have multiple numeric variables)
# In case of having multiple numeric columns (for now, we only have "Sales")
# We will simulate a correlation matrix with the Sales data alone

correlation_matrix = df[['Sales']].corr()  # Using only Sales for demonstration
plt.figure(figsize=(6, 4))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Sales Correlation Heatmap')
plt.tight_layout()
plt.show()

"""
