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

class Vehicle:
    """Represents a general vehicle."""
    
    transport_type = "Land"

    def __init__(self, brand: str, model: str, year: int, price: float):
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self.odometer = 0

    def drive(self, miles: int) -> str:
        self.odometer += miles
        return f"The {self.model} drove {miles} miles. Total: {self.odometer}."

    def __str__(self) -> str:
        return f"{self.year} {self.brand} {self.model}"

# Demonstration
gas_car = Vehicle("Ford", "Mustang", 2024, 45000.0)
print(f"Created: {gas_car}")
print(gas_car.drive(50))

class Vehicle:
    """Represents a general vehicle with encapsulated data."""
    
    transport_type = "Land"

    def __init__(self, brand: str, model: str, year: int, price: float):
        self.brand = brand
        self.model = model
        self.year = year
        self._price = price      # Protected attribute
        self.__odometer = 0      # Private attribute (Name mangled)

    def drive(self, miles: int) -> str:
        self.__odometer += miles
        return f"The {self.model} drove {miles} miles. Total: {self.__odometer}."

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float):
        if new_price > 0:
            self._price = new_price
        else:
            print("Error: Price must be a positive number.")

    def __str__(self) -> str:
        return f"{self.year} {self.brand} {self.model}"
    

    # (Assuming Vehicle class from Commit 2 is above this)

class ElectricCar(Vehicle):
    """A specialized Vehicle powered by electricity."""

    def __init__(self, brand: str, model: str, year: int, price: float, battery_kwh: int):
        super().__init__(brand, model, year, price)
        self.battery_kwh = battery_kwh

    def drive(self, miles: int) -> str:
        # Calls the parent drive method, then adds EV logic
        base_message = super().drive(miles)
        battery_used = miles * 0.3
        return f"{base_message} Used {battery_used:.1f} kWh of battery power."

def take_for_a_spin(vehicle_obj, distance: int):
    """Polymorphic function: accepts any object with a .drive() method."""
    print(f"Testing drive: {vehicle_obj.drive(distance)}")

# Final Test
gas_car = Vehicle("Ford", "Mustang", 2024, 45000.0)
ev_car = ElectricCar("Tesla", "Model 3", 2026, 38000.0, 75)

take_for_a_spin(gas_car, 50)
take_for_a_spin(ev_car, 50)