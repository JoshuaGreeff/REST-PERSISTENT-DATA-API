# Reflection

I began by separating the database connection, SQLAlchemy model, Pydantic validation schema, and Flask routes into small files. The POST route validates a clinical record, commits it to SQLite, and then appends the same saved record to a JSON Lines file. The GET route reads the persistent records from SQLite, which made it easy to see the difference between a live API response and a file-based audit record.

One surprise was that the three added fields had to be carried through every layer of the project. I added blood type, allergy notes, and attending provider to the database model, Pydantic schema, request handling, JSONL output, and GET response. The project helped me understand why schema changes require discipline when several systems depend on the same data shape. I would like to learn more about how production systems keep a database and an audit log synchronized if a write to one location fails.
