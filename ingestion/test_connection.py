import psycopg2

print("Script lancé")

conn = psycopg2.connect(
    host = "localhost",
    dbname = "financial_db",
    user = "postgres",
    password = "postgre123",
    options = '-c client_encoding=UTF8'
)

print("Connexion réussie")

conn.close()