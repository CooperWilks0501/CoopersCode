# Basic Azure Synthetic Data Generator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os
from faker import Faker
from datetime import datetime, timedelta

# ================================
# CONFIG: Set your data output path here
DATA_DIR = r'C:\Users\CWilk\Desktop\PyhtonProj\data'
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the directory exists
# ================================

# Initialize
fake = Faker()
start_date = datetime.now() - timedelta(days=30)
departments = ['Engineering', 'Sales', 'Marketing', 'Finance', 'IT']
resource_types = ['VM', 'Storage', 'Database', 'Functions', 'AppService']

# Generate users
def generate_users(num_users=50):
    users = []
    for i in range(num_users):
        user = {
            'user_id': i,
            'username': fake.user_name(),
            'email': fake.email(),
            'department': random.choice(departments),
            'is_admin': random.random() < 0.15,
        }
        users.append(user)
    return pd.DataFrame(users)

# Generate resources
def generate_resources(num_resources=100):
    resources = []
    for i in range(num_resources):
        resource_type = random.choice(resource_types)
        resources.append({
            'resource_id': i,
            'name': f"{resource_type.lower()}-{fake.word()}-{random.randint(1,999)}",
            'type': resource_type,
            'location': random.choice(['East US', 'West US', 'Europe', 'Asia']),
            'created_date': fake.date_time_between(start_date='-1y', end_date='now'),
            'owner_department': random.choice(departments),
            'is_public': random.random() < 0.3,
        })
    return pd.DataFrame(resources)

# Generate activity logs
def generate_activity(users_df, resources_df, num_days=30, anomaly_rate=0.05):
    activities = []
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        is_weekday = current_date.weekday() < 5
        num_events = random.randint(100, 200) if is_weekday else random.randint(30, 70)

        for _ in range(num_events):
            user = users_df.iloc[random.randint(0, len(users_df)-1)]
            resource = resources_df.iloc[random.randint(0, len(resources_df)-1)]

            hour = random.randint(9, 17) if is_weekday and random.random() < 0.8 else random.randint(0, 23)
            event_time = current_date.replace(hour=hour, minute=random.randint(0, 59))

            is_successful = True if user['is_admin'] or random.random() < 0.95 else False

            activities.append({
                'timestamp': event_time,
                'user_id': user['user_id'],
                'username': user['username'],
                'department': user['department'],
                'resource_id': resource['resource_id'],
                'resource_name': resource['name'],
                'resource_type': resource['type'],
                'action': random.choice(['Read', 'Create', 'Update', 'Delete']),
                'is_successful': is_successful,
                'is_anomaly': False
            })

    num_anomalies = int(len(activities) * anomaly_rate)
    for _ in range(num_anomalies):
        normal_idx = random.randint(0, len(activities)-1)
        anomaly = activities[normal_idx].copy()
        anomaly_type = random.randint(1, 3)

        if anomaly_type == 1:
            anomaly['timestamp'] = anomaly['timestamp'].replace(hour=random.randint(22, 23))
        elif anomaly_type == 2:
            anomaly['is_admin'] = False
            anomaly['action'] = 'Delete'
            anomaly['is_successful'] = random.random() < 0.3
        else:
            user_dept = anomaly['department']
            while anomaly['department'] == user_dept:
                anomaly['department'] = random.choice(departments)

        anomaly['is_anomaly'] = True
        activities.append(anomaly)

    return pd.DataFrame(activities)

# Generate and save everything
def generate_all_data():
    print("Generating users...")
    users = generate_users(50)

    print("Generating resources...")
    resources = generate_resources(100)

    print("Generating activity logs...")
    activities = generate_activity(users, resources)

    # Save to CSV files
    users.to_csv(os.path.join(DATA_DIR, 'azure_users.csv'), index=False)
    resources.to_csv(os.path.join(DATA_DIR, 'azure_resources.csv'), index=False)
    activities.to_csv(os.path.join(DATA_DIR, 'azure_activities.csv'), index=False)

    print(f"Generated {len(users)} users, {len(resources)} resources, and {len(activities)} activities")
    return users, resources, activities

# Entry point
if __name__ == "__main__":
    users, resources, activities = generate_all_data()

    plt.figure(figsize=(10, 6))
    activities['hour'] = activities['timestamp'].dt.hour
    hourly_counts = activities.groupby('hour').size()
    hourly_counts.plot(kind='bar', title='Activity by Hour of Day')
    plt.tight_layout()
    plt.savefig(os.path.join(DATA_DIR, 'activity_by_hour.png'))

    print("Data generation complete!")
