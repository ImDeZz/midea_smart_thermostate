from supabase import create_client, Client
import os

# Define your Supabase URL and Key
SUPABASE_URL = "https://vmwgjhzxalqtguiqavos.supabase.co"  # Replace with your Supabase project URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZtd2dqaHp4YWxxdGd1aXFhdm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI5ODcyODMsImV4cCI6MjA0ODU2MzI4M30.755ljphmQkmLF0HPnDUfSXTldmOWjM0jo5JQ5zuZz94"  # Replace with your Supabase public anon key

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Example: Insert a new row into a "users" table
def insert_user():
    data = {
        "is_active": True,
    }
    
    # Insert a new user into the "users" table
    response = supabase.table("status").insert(data).execute()

# Example: Query rows from a "users" table
def get_users():
    # Select all users
    response = supabase.table("status").select("*").execute()

    if response.status_code == 200:
        print("Users retrieved successfully:")
        for user in response.data:
            print(user)
    else:
        print(f"Error retrieving users: {response.status_code} - {response.message}")

# Call the functions to test them
insert_user()  # Insert a user
get_users()    # Get users from the "users" table
