from tables import DatabaseCreator

if __name__ == "__main__":
    db_creator = DatabaseCreator()
    db_creator.create_tables()
    db_creator.close()
    print("Database tables created successfully.")
