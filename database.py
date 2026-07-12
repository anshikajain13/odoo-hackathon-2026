import sqlite3

DB_NAME = "transitops.db"

def get_connection():
    """Establishes database connection with foreign key enforcement."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes core relational tables for the transit management system."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. VEHICLES TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_number TEXT UNIQUE NOT NULL,
            model TEXT NOT NULL,
            type TEXT NOT NULL,
            max_capacity REAL NOT NULL,
            odometer REAL NOT NULL,
            acquisition_cost REAL NOT NULL,
            status TEXT DEFAULT 'Available' CHECK (status IN ('Available', 'On Trip', 'In Shop', 'Retired'))
        );
    ''')
    
    # 2. DRIVERS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            license_number TEXT NOT NULL,
            license_expiry TEXT NOT NULL,
            safety_score REAL DEFAULT 100.0,
            status TEXT DEFAULT 'Available' CHECK (status IN ('Available', 'On Trip', 'Off Duty', 'Suspended'))
        );
    ''')
    
    # 3. TRIPS TABLE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            vehicle_id INTEGER NOT NULL,
            driver_id INTEGER NOT NULL,
            cargo_weight REAL NOT NULL,
            distance REAL NOT NULL,
            status TEXT DEFAULT 'Draft' CHECK (status IN ('Draft', 'Dispatched', 'Completed', 'Cancelled')),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE RESTRICT,
            FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE RESTRICT
        );
    ''')
    
    # 4. MAINTENANCE LOGS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            cost REAL DEFAULT 0.0,
            entry_date TEXT NOT NULL,
            status TEXT DEFAULT 'Open' CHECK (status IN ('Open', 'Closed')),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
        );
    ''')
    
    # 5. EXPENSES LOGS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            trip_id INTEGER,
            type TEXT NOT NULL CHECK (type IN ('Fuel', 'Toll', 'Other')),
            amount REAL NOT NULL,
            liters REAL DEFAULT 0.0,
            date TEXT NOT NULL,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE SET NULL
        );
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database schema initialized successfully.") 