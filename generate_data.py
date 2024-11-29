import psycopg2
from faker import Faker
from io import StringIO
import time

# Initialize Faker
fake = Faker()

# Database configuration
DB_CONFIG = {
    "dbname": "energy_cons",
    "user": "postgres",
    "password": "12345678",
    "host": "localhost",
    "port": 5432
}

# Function to generate a batch of unique users
def generate_unique_users(batch_size):
    users = set()
    while len(users) < batch_size:
        username = fake.unique.user_name()
        email = fake.unique.email()
        password = fake.password(length=12)
        users.add((username, email, password))
    return list(users)

# Function to generate a batch of energy consumption reports
def generate_consumptions(batch_size, user_ids):
    consumptions = []
    for _ in range(batch_size):
        consumption = {
            "date": fake.date_this_decade(),
            "time": fake.time(),
            "consumption": round(fake.random_number(digits=2), 2),
            "cost": round(fake.random_number(digits=3), 2),
            "source": fake.word(),
            "location": fake.city(),
            "user_id": fake.random_element(user_ids),
        }
        consumptions.append(consumption)
    return consumptions

# Function to generate a batch of savings reports
def generate_savings(batch_size, user_ids):
    savings = []
    for _ in range(batch_size):
        saving = {
            "date": fake.date_this_decade(),
            "energy_saved": round(fake.random_number(digits=2), 2),
            "savings": round(fake.random_number(digits=3), 2),
            "method": fake.word(),
            "percentage_saved": round(fake.random_number(digits=2), 2),
            "units_saved": round(fake.random_number(digits=2), 2),
            "user_id": fake.random_element(user_ids),
        }
        savings.append(saving)
    return savings

# Function to insert data into the database using COPY for users, consumptions, and savings
def bulk_insert_users(users, connection):
    try:
        with connection.cursor() as cursor:
            # Prepare data for COPY
            buffer = StringIO()
            for user in users:
                buffer.write(f"{user[0]}\t{user[1]}\t{user[2]}\n")
            buffer.seek(0)
            # Copy data to the users table
            cursor.copy_from(buffer, "users", sep="\t", columns=("username", "email", "password"))
            connection.commit()
            print(f"Inserted {len(users)} users successfully.")
    except Exception as e:
        print(f"Error during bulk insert: {e}")
        connection.rollback()

def bulk_insert_consumptions(consumptions, connection):
    try:
        with connection.cursor() as cursor:
            buffer = StringIO()
            for consumption in consumptions:
                buffer.write(f"{consumption['date']}\t{consumption['time']}\t{consumption['consumption']}\t{consumption['cost']}\t{consumption['source']}\t{consumption['location']}\t{consumption['user_id']}\n")
            buffer.seek(0)
            cursor.copy_from(buffer, "energy_consumptions", sep="\t", columns=("date", "time", "consumption", "cost", "source", "location", "user_id"))
            connection.commit()
            print(f"Inserted {len(consumptions)} consumptions successfully.")
    except Exception as e:
        print(f"Error during bulk insert: {e}")
        connection.rollback()

def bulk_insert_savings(savings, connection):
    try:
        with connection.cursor() as cursor:
            buffer = StringIO()
            for saving in savings:
                buffer.write(f"{saving['date']}\t{saving['energy_saved']}\t{saving['savings']}\t{saving['method']}\t{saving['percentage_saved']}\t{saving['units_saved']}\t{saving['user_id']}\n")
            buffer.seek(0)
            cursor.copy_from(buffer, "savings_reports", sep="\t", columns=("date", "energy_saved", "savings", "method", "percentage_saved", "units_saved", "user_id"))
            connection.commit()
            print(f"Inserted {len(savings)} savings reports successfully.")
    except Exception as e:
        print(f"Error during bulk insert: {e}")
        connection.rollback()

# Main function to generate and insert users, savings, and consumptions
def generate_users(batch_size, total_users):
    try:
        # Connect to the database
        connection = psycopg2.connect(**DB_CONFIG)
        print("Connected to the database.")
        total_inserted = 0
        user_ids = []
        while total_inserted < total_users:
            # Generate a batch of unique users
            batch_users = generate_unique_users(batch_size)
            # Insert the batch into the database
            bulk_insert_users(batch_users, connection)
            
            # After users are inserted, fetch their IDs
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM users ORDER BY id DESC LIMIT %s", (batch_size,))
                user_ids.extend([row[0] for row in cursor.fetchall()])
            
            # Generate consumptions and savings
            consumptions = generate_consumptions(batch_size, user_ids)
            savings = generate_savings(batch_size, user_ids)

            # Insert consumptions and savings into the database
            bulk_insert_consumptions(consumptions, connection)
            bulk_insert_savings(savings, connection)
            
            total_inserted += len(batch_users)
            print(f"Progress: {total_inserted}/{total_users} users, consumptions, and savings inserted.")
        print("All data inserted successfully.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if connection:
            connection.close()
            print("Database connection closed.")

# Run the script
if __name__ == "__main__":
    # Generate 500,000 users, consumptions, and savings in batches of 10,000
    start_time = time.time()
    generate_users(batch_size=10000, total_users=500000)
    print(f"Execution time: {time.time() - start_time:.2f} seconds")
