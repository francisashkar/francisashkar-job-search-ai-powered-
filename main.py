import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection URI
uri = "mongodb+srv://ashkarfrancis1:frafra45@cluster0.jbpov.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Database and collection name
database_name = "jobs_db"
collection_name = "QA"

# File path to the CSV
csv_file_path = "D:/Users/Ashka/PycharmProjects/pythonProject5/python.csv"

try:
    # Ping the database to confirm connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    # Load the CSV file
    df = pd.read_csv(csv_file_path)

    # Rename columns as needed
    column_rename_mapping = {
        "tablescraper-selected-row href": "links",
        "css-6ubqba": "role",
        "css-1oq4rdn": "company",
        "css-1hqv54u": "location",
        "css-1hqv54u 2": "time_posted",
        "css-1hqv54u 3": "score"
    }
    df.rename(columns=column_rename_mapping, inplace=True)

    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient="records")

    # Access the database and collection
    db = client[database_name]
    collection = db[collection_name]

    # Insert the data into the collection
    result = collection.insert_many(data)
    print(f"Inserted {len(result.inserted_ids)} documents into the collection.")

except FileNotFoundError:
    print(f"File not found at {csv_file_path}. Please check the path.")
except Exception as e:
    print(e)
finally:
    # Close the connection
    client.close()
