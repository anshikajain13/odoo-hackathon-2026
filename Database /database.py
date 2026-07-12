import sqlite3
import re

DB_NAME = "transitops.db"

def get_connection():
    """Establishes database connection with strict timeouts to prevent connection flooding."""
    conn = sqlite3.connect(DB_NAME, timeout=10.0)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes core relational tables securely for the transit management system."""
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

def validate_reg_number(reg_number):
    """Input Validation: Validates vehicle registration plate format."""
    if not reg_number or not isinstance(reg_number, str):
        return False
    return bool(re.match(r'^[A-Z0-9-]{4,15}$', reg_number.strip().upper()))

def add_vehicle(reg_number, model, v_type, max_capacity, odometer, acquisition_cost, status='Available'):
    """Adds a new vehicle with strict server-side input validation and parameterized queries."""
    if not validate_reg_number(reg_number):
        print("[VALIDATION ERROR] Invalid vehicle registration format.")
        return False
    if not model or not v_type:
        print("[VALIDATION ERROR] Model and Type cannot be blank.")
        return False
        
    try:
        max_capacity = float(max_capacity)
        odometer = float(odometer)
        acquisition_cost = float(acquisition_cost)
        if max_capacity <= 0 or odometer < 0 or acquisition_cost < 0:
            print("[VALIDATION ERROR] Numeric metrics must be logical non-negative values.")
            return False
    except ValueError:
        print("[VALIDATION ERROR] Data conversion failed for numeric fields.")
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vehicles (reg_number, model, type, max_capacity, odometer, acquisition_cost, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (reg_number.strip().upper(), model.strip(), v_type.strip(), max_capacity, odometer, acquisition_cost, status))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("[DATABASE ERROR] Duplicate registration number entry blocked.")
        return False
    finally:
        conn.close()

def add_driver(name, license_number, license_expiry, safety_score=100.0, status='Available'):
    """Registers a new driver with parameter validation."""
    if not name or not license_number or not license_expiry:
        print("[VALIDATION ERROR] Driver credentials cannot be blank.")
        return False
        
    try:
        safety_score = float(safety_score)
        if not (0 <= safety_score <= 100):
            print("[VALIDATION ERROR] Safety score bounds must be 0-100.")
            return False
    except ValueError:
        print("[VALIDATION ERROR] Invalid datatypes provided for safety score.")
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO drivers (name, license_number, license_expiry, safety_score, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (name.strip(), license_number.strip().upper(), license_expiry.strip(), safety_score, status))
        conn.commit()
        return True
    except Exception as e:
        print(f"[DATABASE ERROR] {e}")
        return False
    finally:
        conn.close()

def add_trip(source, destination, vehicle_id, driver_id, cargo_weight, distance, status='Draft'):
    """Creates a new trip log with validated relations and strict input checks."""
    if not source or not destination:
        print("[VALIDATION ERROR] Source and Destination strings cannot be empty.")
        return False
        
    try:
        vehicle_id = int(vehicle_id)
        driver_id = int(driver_id)
        cargo_weight = float(cargo_weight)
        distance = float(distance)
        if cargo_weight <= 0 or distance <= 0:
            print("[VALIDATION ERROR] Distance and weight logs must be positive values.")
            return False
    except ValueError:
        print("[VALIDATION ERROR] Relational ID parsing exception.")
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM vehicles WHERE id = ?", (vehicle_id,))
        if not cursor.fetchone():
            print("[INTEGRITY ERROR] Relational check failed: Vehicle ID does not exist.")
            return False
            
        cursor.execute("SELECT id FROM drivers WHERE id = ?", (driver_id,))
        if not cursor.fetchone():
            print("[INTEGRITY ERROR] Relational check failed: Driver ID does not exist.")
            return False

        cursor.execute('''
            INSERT INTO trips (source, destination, vehicle_id, driver_id, cargo_weight, distance, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (source.strip(), destination.strip(), vehicle_id, driver_id, cargo_weight, distance, status))
        conn.commit()
        return True
    except Exception as e:
        print(f"[DATABASE ERROR] {e}")
        return False
    finally:
        conn.close()

def log_maintenance(vehicle_id, description, cost, entry_date, status='Open'):
    """Logs vehicle maintenance details securely."""
    if not description or not entry_date:
        print("[VALIDATION ERROR] Maintenance fields cannot be null.")
        return False
        
    try:
        vehicle_id = int(vehicle_id)
        cost = float(cost)
        if cost < 0:
            print("[VALIDATION ERROR] Financial maintenance metrics cannot be negative.")
            return False
    except ValueError:
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO maintenance_logs (vehicle_id, description, cost, entry_date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (vehicle_id, description.strip(), cost, entry_date.strip(), status))
        conn.commit()
        return True
    except Exception as e:
        print(f"[DATABASE ERROR] {e}")
        return False
    finally:
        conn.close()

def get_fleet_summary():
    """Fetches total active vehicles, total drivers, and ongoing trips for the dashboard."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Active vehicles summary
        cursor.execute("SELECT COUNT(*) FROM vehicles WHERE status != 'Retired'")
        total_vehicles = cursor.fetchone()[0]
        
        # 2. Total active drivers
        cursor.execute("SELECT COUNT(*) FROM drivers WHERE status != 'Suspended'")
        total_drivers = cursor.fetchone()[0]
        
        # 3. Live trips running
        cursor.execute("SELECT COUNT(*) FROM trips WHERE status = 'Dispatched'")
        live_trips = cursor.fetchone()[0]
        
        return {
            "total_vehicles": total_vehicles,
            "total_drivers": total_drivers,
            "live_trips": live_trips
        }
    except Exception as e:
        print(f"[ANALYTICS ERROR] Fleet summary failed: {e}")
        return {}
    finally:
        conn.close()

def get_total_expenses():
    """Calculates total dynamic expense breakdown across the system."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT type, SUM(amount) FROM expenses GROUP BY type")
        rows = cursor.fetchall()
        
        # Formatting breakdown as a clean dictionary
        breakdown = {row[0]: row[1] for row in rows}
        return breakdown
    except Exception as e:
        print(f"[ANALYTICS ERROR] Expense query failed: {e}")
        return {}
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    print("Database system initialized successfully.")