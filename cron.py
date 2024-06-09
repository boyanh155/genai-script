from dotenv import load_dotenv
import pymongo
from datetime import datetime,date
from psycopg2 import connect
import os
import json

load_dotenv()

# PostgreSQL credentials

pg_user_name = os.getenv("pg_user_name")
pg_password = os.getenv("pg_password")
pg_host = os.getenv("pg_host")
pg_port = os.getenv("pg_port")
pg_db_name = os.getenv("pg_db_name")

# credential
user_name = os.getenv("user_name")

azure_user_name = os.getenv("azure_user_name")
mongodb_connection_string = os.getenv("mongodb_connection_string")
azure_connection_string = os.getenv("azure_connection_string")
db_name = os.getenv("db_name")


BATCH_SIZE = os.getenv("BATCH_SIZE") and int(os.getenv("BATCH_SIZE")) or 1000


# mongodb
# 

print("Connecting to PostgreSQL...")
postgre_client = connect(f"dbname={pg_db_name} user={pg_user_name} host={pg_host} password={pg_password} port={pg_port}")
cur = postgre_client.cursor()
# db = mongodb_client[db_name]
print("Connected")


#azure 
azure_client = pymongo.MongoClient(azure_connection_string)
azure_db = azure_client[db_name]

def get_table_names():
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    return [table[0] for table in cur.fetchall()]

def write_log(note):
    with open('migrate-info.txt', 'a') as f:
        f.write(f'{datetime.now()}: {note}\n')
# migrate collection
def migrate_collection(collection_name):
    try:
        offset = 0
        azure_collection = azure_db[collection_name]
        while True:
            cur.execute(f"SELECT * FROM {collection_name} LIMIT {BATCH_SIZE} OFFSET {offset}")
            rows = cur.fetchall()
            
            print(f"Starting migration for collection: {collection_name} at {datetime.now()}")
            if not rows:
                break  # No more rows to fetch, stop the loop
            
            # Fetch all documents from local MongoDB in batches

            # documents = [dict(zip([column[0] for column in cur.description], row)) for row in rows]
            documents = []
            for row in rows:
                document = {}
                for i, column in enumerate(cur.description):
                    value = row[i]
                    if isinstance(value, date) and not isinstance(value, datetime):
                        value = datetime.combine(value, datetime.min.time())
                    document[column[0]] = value
                documents.append((document))
        
                for document in documents:
                    filter = {'_id': document['id'] or document["_id"]}  # Assuming '_id' is the unique identifier
                    update ={'$set': document}
                    
                    try:
                        azure_collection.update_one(filter, update, upsert=True)
                    except Exception as e:
                        raise e
            
                    
                offset += BATCH_SIZE
            
        print(f"Migration completed for collection: {collection_name} at {datetime.now()}")
    except Exception as e:
        raise e
# migrate database (main function)
def migrate_database():
    
    print(f"Starting database migration at {datetime.now()}")
# List all collections in the local database
    try: 
        with open('migrate-info.txt', 'a') as f:
            f.write('--------------------------------------\n')
        write_log('Migration started')
        collections = get_table_names()
        for collection in collections:
            migrate_collection(collection)
    except Exception as e:
        print(f"Error occurred during migration: {e}")
        write_log(f"Error occurred during migration: {e}")
    finally:
        write_log('Migration ended')
    print(f"Database migration completed at {datetime.now()}")


# Schedule the migration to run daily
# schedule.every().day.at("00:00").do(migrate_database)  # Adjust time as needed

# print("Service started...")

# migrate_database()

# Create the scheduler
# scheduler = BlockingScheduler()

# Schedule the migration to run daily at 2:00 AM
# print("Cron started...")

migrate_database()

# scheduler.add_job(migrate_database, 'cron', hour=0, minute=0)

# try:
#     # Start the scheduler
#     scheduler.start()
# except (KeyboardInterrupt, SystemExit):
#     pass