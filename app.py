import sqlite3

DATABASE_NAME = "tasks.db"

def init_db():

    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    
        cursor.execute("SELECT COUNT(*) FROM tasks")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO tasks (title, description, completed)
                VALUES 
                    ('Fix login bug', 'Resolve the 500 error on the login endpoint', 0),
                    ('Write unit tests', 'Cover the auth blueprint handlers', 0),
                    ('Deploy to staging', 'Push the latest main branch to Heroku', 1),
                    ('Update README', 'Add installation and environment variables setup steps', 0),
                    ('Code review PR #42', 'Review the database migrations PR', 1);
            """)
            conn.commit()
            print("Database initialized with sample data.")


def get_all_tasks():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        return cursor.fetchall()

def get_task_by_id(task_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
    
        cursor.execute(
            'SELECT * FROM tasks WHERE id=?',
            (task_id,)
        )
        return cursor.fetchone()

def get_incomplete_tasks():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tasks WHERE completed=0'
            ' ORDER BY created_at DESC'
        )
        return cursor.fetchall()

if __name__ == "__main__":
    init_db()
    
    print("\n All Tasks ")
    all_tasks = get_all_tasks()
    for task in all_tasks:
        print(task)
        
    print("\n Incomplete Tasks (Sorted Newest First) ")
    incomplete = get_incomplete_tasks()
    for task in incomplete:
        print(task)
        
    print("\n Fetching Task ID #3 ")
    task_three = get_task_by_id(3)
    print(task_three)

def fibonacci(n):
    """
    Returns the N-th Fibonacci number using recursion.
    n must be a non-negative integer.
    """
    # Base cases: F(0) = 0, F(1) = 1
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    # Recursive step: F(n) = F(n-1) + F(n-2)
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# Example usage: Generate the first 10 numbers in the sequence
terms = 10
fib_sequence = [fibonacci(i) for i in range(terms)]
print(f"First {terms} Fibonacci numbers: {fib_sequence}")

from functools import lru_cache

# Using a cache optimizes the time complexity to O(n)
@lru_cache(maxsize=None)
def fibonacci_fast(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci_fast(n - 1) + fibonacci_fast(n - 2)

# This will run instantly, whereas the un-cached version would hang indefinitely!
print(fibonacci_fast(50))