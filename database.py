import psycopg2
from psycopg2 import sql, extras
import hashlib
import pandas as pd
import base64
from datetime import datetime

# Database Configuration
DB_CONFIG = {
    "user": "postgres",
    "password": "Pratik@123",
    "host": "localhost",
    "port": "5432",
    "database": "IMS"
}

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# -------------------- AUTHENTICATION FUNCTIONS --------------------
def authenticate_user(username, password):
    """Authenticate user from employee_master table"""
    conn = get_db_connection()
    if not conn:
        print("Database connection failed")
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        query = """
            SELECT 
                id,
                employee_name, 
                designation,
                email_id,
                phone_number,
                password
            FROM employee_master 
            WHERE employee_name = %s
        """
        
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user:
            if user['password'] == password:
                return {
                    'user_id': user['id'],
                    'username': user['employee_name'],
                    'name': user['employee_name'],
                    'user_type': 'admin',
                    'designation': user['designation'] if user['designation'] else '',
                    'email': user['email_id'] if user['email_id'] else '',
                    'phone': user['phone_number'] if user['phone_number'] else ''
                }
        return None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def test_database():
    """Test database connection and show employees"""
    conn = get_db_connection()
    if not conn:
        print("❌ Database connection failed!")
        return False
    
    try:
        cursor = conn.cursor()
        
        print("=" * 60)
        print("TABLE STRUCTURE:")
        print("=" * 60)
        
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'employee_master'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[0]} -> {col[1]}")
        
        print("\n" + "=" * 60)
        print("EMPLOYEE DATA:")
        print("=" * 60)
        
        cursor.execute("SELECT id, employee_name, designation, email_id, phone_number, password, created_at FROM employee_master")
        employees = cursor.fetchall()
        
        for emp in employees:
            print(f"\n--- Employee ---")
            print(f"  id: {emp[0]}")
            print(f"  employee_name: {emp[1]}")
            print(f"  designation: {emp[2]}")
            print(f"  email_id: {emp[3]}")
            print(f"  phone_number: {emp[4]}")
            print(f"  password: {emp[5]}")
            print(f"  created_at: {emp[6]}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_all_employees():
    """Get all employees from database"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT id, employee_name, designation, email_id, phone_number FROM employee_master ORDER BY employee_name"
        cursor.execute(query)
        employees = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return employees
    except Exception as e:
        print(f"Error fetching employees: {e}")
        return []

def add_employee(employee_name, designation, email_id, phone_number, password):
    """Add new employee to database"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        query = """
            INSERT INTO employee_master (employee_name, designation, email_id, phone_number, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (employee_name, designation, email_id, phone_number, password))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding employee: {e}")
        return False

# -------------------- REPORT DATA FUNCTIONS --------------------
def get_table_names():
    """Get available table names"""
    return ['hes_monthly_report', 'hes_monthly_report_1']

def get_report_data(table_name):
    """Fetch data from selected table"""
    conn = get_db_connection()
    if not conn:
        return None, None
    
    try:
        query = f'SELECT * FROM public."{table_name}" ORDER BY sr_no'
        df = pd.read_sql(query, conn)
        conn.close()
        
        columns = df.columns.tolist()
        months = [col for col in columns if col not in ['sr_no', 'items']]
        
        return df, months
    except Exception as e:
        print(f"Error fetching data from {table_name}: {e}")
        conn.close()
        return None, None

# -------------------- BUSINESS DEVELOPMENT FUNCTIONS --------------------
def get_all_bd_objectives():
    """Get all BD objectives from database"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM bd_objectives ORDER BY objective_id"
        cursor.execute(query)
        objectives = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return objectives
    except Exception as e:
        print(f"Error fetching BD objectives: {e}")
        return []

def get_bd_objective_by_id(obj_id):
    """Get single BD objective by ID"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM bd_objectives WHERE id = %s"
        cursor.execute(query, (obj_id,))
        objective = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(objective) if objective else None
    except Exception as e:
        print(f"Error fetching BD objective: {e}")
        return None

def save_bd_evaluation_with_evidence(objective_id, data_entry_value, reviewed_by, remarks, evidence_filename, evidence_content, evidence_text):
    """Save BD evaluation data with both file and text evidence"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT previous_achievement FROM bd_objectives WHERE id = %s", (objective_id,))
        result = cursor.fetchone()
        
        if not result:
            return False
        
        previous = float(result[0]) if result[0] else 0
        actual = float(data_entry_value) if data_entry_value else 0
        
        if previous > 0:
            growth_rate = ((actual - previous) / previous) * 100
            percentage = (actual / previous) * 100
            if percentage < 70:
                status = "Not Achieved"
            elif 70 <= percentage < 100:
                status = "Partially Achieved"
            else:
                status = "Achieved"
        else:
            growth_rate = 0
            status = "Achieved" if actual > 0 else "Not Achieved"
        
        achievement = actual
        
        encoded_evidence = None
        if evidence_content:
            encoded_evidence = base64.b64encode(evidence_content).decode('utf-8')
        
        query = """
            UPDATE bd_objectives 
            SET data_entry_value = %s,
                growth_rate = %s,
                date_of_review = CURRENT_DATE,
                achievement = %s,
                status = %s,
                evidence = %s,
                evidence_filename = %s,
                evidence_text = %s,
                reviewed_by = %s,
                remarks = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (data_entry_value, growth_rate, achievement, status, 
                              encoded_evidence, evidence_filename, evidence_text,
                              reviewed_by, remarks, objective_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving BD evaluation with evidence: {e}")
        return False

def save_evidence(objective_id, file_content, filename):
    """Save evidence file for objective"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        encoded_content = base64.b64encode(file_content).decode('utf-8')
        query = """
            UPDATE bd_objectives 
            SET evidence = %s,
                evidence_filename = %s,
                evidence_uploaded_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (encoded_content, filename, objective_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving evidence: {e}")
        return False

# -------------------- FINANCE DATA FUNCTIONS (Main) --------------------
def get_finance_years():
    """Get all available years from finance table"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        query = "SELECT DISTINCT year FROM finance_data ORDER BY year DESC"
        cursor.execute(query)
        years = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return years
    except Exception as e:
        print(f"Error fetching finance years: {e}")
        return []

def get_finance_amount_by_year(year):
    """Get amount for a specific year"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        query = "SELECT amount FROM finance_data WHERE year = %s"
        cursor.execute(query, (year,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return float(result[0])
        return None
    except Exception as e:
        print(f"Error fetching amount for year {year}: {e}")
        return None

def get_all_finance_data():
    """Get all finance data"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM finance_data ORDER BY year DESC"
        cursor.execute(query)
        data = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"Error fetching finance data: {e}")
        return []

def add_finance_data(year, amount, description):
    """Add new finance data"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        query = "INSERT INTO finance_data (year, amount, description) VALUES (%s, %s, %s)"
        cursor.execute(query, (year, amount, description))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding finance data: {e}")
        return False

# -------------------- HR FINANCE FUNCTIONS --------------------
def get_hr_finance_years():
    """Get all available years from HR finance table"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT year FROM hr_finance_data ORDER BY year DESC")
        years = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return years
    except Exception as e:
        print(f"Error fetching HR finance years: {e}")
        return []

def get_hr_finance_amount_by_year(year):
    """Get amount for a specific year from HR finance"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM hr_finance_data WHERE year = %s", (year,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return float(result[0]) if result else None
    except Exception as e:
        print(f"Error fetching HR amount for year {year}: {e}")
        return None

def get_all_hr_finance_data():
    """Get all HR finance data"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM hr_finance_data ORDER BY year DESC")
        data = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"Error fetching HR finance data: {e}")
        return []

def add_hr_finance_data(year, amount, description):
    """Add new HR finance data"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO hr_finance_data (year, amount, description) VALUES (%s, %s, %s)", (year, amount, description))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding HR finance data: {e}")
        return False

# -------------------- ADMIN FINANCE FUNCTIONS --------------------
def get_admin_finance_years():
    """Get all available years from Admin finance table"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT year FROM admin_finance_data ORDER BY year DESC")
        years = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return years
    except Exception as e:
        print(f"Error fetching Admin finance years: {e}")
        return []

def get_admin_finance_amount_by_year(year):
    """Get amount for a specific year from Admin finance"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM admin_finance_data WHERE year = %s", (year,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return float(result[0]) if result else None
    except Exception as e:
        print(f"Error fetching Admin amount for year {year}: {e}")
        return None

def get_all_admin_finance_data():
    """Get all Admin finance data"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM admin_finance_data ORDER BY year DESC")
        data = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"Error fetching Admin finance data: {e}")
        return []

def add_admin_finance_data(year, amount, description):
    """Add new Admin finance data"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admin_finance_data (year, amount, description) VALUES (%s, %s, %s)", (year, amount, description))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding Admin finance data: {e}")
        return False

# -------------------- OPERATION FINANCE FUNCTIONS --------------------
def get_operation_finance_years():
    """Get all available years from Operation finance table"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT year FROM operation_finance_data ORDER BY year DESC")
        years = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return years
    except Exception as e:
        print(f"Error fetching Operation finance years: {e}")
        return []

def get_operation_finance_amount_by_year(year):
    """Get amount for a specific year from Operation finance"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM operation_finance_data WHERE year = %s", (year,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return float(result[0]) if result else None
    except Exception as e:
        print(f"Error fetching Operation amount for year {year}: {e}")
        return None

def get_all_operation_finance_data():
    """Get all Operation finance data"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM operation_finance_data ORDER BY year DESC")
        data = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"Error fetching Operation finance data: {e}")
        return []

def add_operation_finance_data(year, amount, description):
    """Add new Operation finance data"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO operation_finance_data (year, amount, description) VALUES (%s, %s, %s)", (year, amount, description))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding Operation finance data: {e}")
        return False

# -------------------- PROCUREMENT FINANCE FUNCTIONS --------------------
def get_procurement_finance_years():
    """Get all available years from Procurement finance table"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT year FROM procurement_finance_data ORDER BY year DESC")
        years = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return years
    except Exception as e:
        print(f"Error fetching Procurement finance years: {e}")
        return []

def get_procurement_finance_amount_by_year(year):
    """Get amount for a specific year from Procurement finance"""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM procurement_finance_data WHERE year = %s", (year,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return float(result[0]) if result else None
    except Exception as e:
        print(f"Error fetching Procurement amount for year {year}: {e}")
        return None

def get_all_procurement_finance_data():
    """Get all Procurement finance data"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM procurement_finance_data ORDER BY year DESC")
        data = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"Error fetching Procurement finance data: {e}")
        return []

def add_procurement_finance_data(year, amount, description):
    """Add new Procurement finance data"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO procurement_finance_data (year, amount, description) VALUES (%s, %s, %s)", (year, amount, description))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding Procurement finance data: {e}")
        return False

# -------------------- SYSTEM ADMIN FUNCTIONS --------------------
def get_all_system_admin_objectives():
    """Get all system admin objectives from database"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT * FROM system_admin ORDER BY id"
        cursor.execute(query)
        objectives = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return objectives
    except Exception as e:
        print(f"Error fetching system admin objectives: {e}")
        return []

def update_system_admin_status(objective_id, current_status, remarks_action_plan):
    """Update system admin objective status"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        query = """
            UPDATE system_admin 
            SET current_achievement = %s,
                remarks = %s,
                review_date = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        review_date = datetime.now().strftime("%d-%m-%Y")
        cursor.execute(query, (current_status, remarks_action_plan, review_date, objective_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating system admin objective: {e}")
        return False

def add_system_admin_objective(category, objective, kpi, target, timeline, responsible, remarks):
    """Add new system admin objective"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        # Get next objective_id
        cursor.execute("SELECT COALESCE(MAX(CAST(SUBSTRING(objective_id, 5) AS INTEGER)), 0) + 1 FROM system_admin")
        next_num = cursor.fetchone()[0]
        objective_id = f"ADM-{str(next_num).zfill(2)}"
        
        query = """
            INSERT INTO system_admin 
            (objective_id, category, objective, kpi, target, timeline, responsible, remarks, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (objective_id, category, objective, kpi, target, timeline, responsible, remarks, 'Not Started'))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding system admin objective: {e}")
        return False

def delete_system_admin_objective(objective_id):
    """Delete system admin objective"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        query = "DELETE FROM system_admin WHERE id = %s"
        cursor.execute(query, (objective_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting system admin objective: {e}")
        return False

# -------------------- HR BUSINESS FUNCTIONS --------------------
def get_all_hr_objectives():
    """Get all HR objectives from database"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM hr_business ORDER BY objective_id")
        objectives = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return objectives
    except Exception as e:
        print(f"Error fetching HR objectives: {e}")
        return []

def save_hr_evaluation_with_evidence(objective_id, data_entry_value, reviewed_by, remarks, evidence_filename, evidence_content, evidence_text):
    """Save HR evaluation with evidence"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT previous_achievement FROM hr_business WHERE id = %s", (objective_id,))
        result = cursor.fetchone()
        if not result:
            return False
        previous = float(result[0]) if result[0] else 0
        actual = float(data_entry_value) if data_entry_value else 0
        
        # Calculate variance
        variance = ""
        try:
            if data_entry_value:
                # Get target
                cursor.execute("SELECT target FROM hr_business WHERE id = %s", (objective_id,))
                target_row = cursor.fetchone()
                if target_row and target_row[0]:
                    target_val = float(str(target_row[0]).replace('%', ''))
                    current_val = float(str(data_entry_value).replace('%', ''))
                    variance_val = current_val - target_val
                    variance = f"{variance_val:.2f}"
                    if '%' in str(target_row[0]):
                        variance = f"{variance_val}%"
        except:
            variance = ""
        
        # Calculate trend
        trend = "→ Stable"
        try:
            if previous and data_entry_value:
                prev_val = float(str(previous).replace('%', ''))
                curr_val = float(str(data_entry_value).replace('%', ''))
                if curr_val > prev_val:
                    trend = "↑ Improving"
                elif curr_val < prev_val:
                    trend = "↓ Declining"
                else:
                    trend = "→ Stable"
        except:
            trend = "→ Stable"
        
        # Calculate status
        if previous > 0:
            growth_rate = ((actual - previous) / previous) * 100
            percentage = (actual / previous) * 100
            if percentage < 70:
                status = "Not Achieved"
            elif 70 <= percentage < 100:
                status = "Partially Achieved"
            else:
                status = "Achieved"
        else:
            growth_rate = 0
            status = "Achieved" if actual > 0 else "Not Achieved"
        
        achievement = actual
        review_date = datetime.now().strftime("%d-%m-%Y")
        
        encoded_evidence = None
        if evidence_content:
            encoded_evidence = base64.b64encode(evidence_content).decode('utf-8')
        
        query = """
            UPDATE hr_business 
            SET current_achievement = %s,
                variance = %s,
                trend = %s,
                review_date = %s,
                reviewed_by = %s,
                remarks = %s,
                evidence = %s,
                evidence_filename = %s,
                evidence_location = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (data_entry_value, variance, trend, review_date, 
                              reviewed_by, remarks, encoded_evidence, evidence_filename, 
                              evidence_text, objective_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving HR evaluation: {e}")
        return False

# -------------------- ADMIN OBJECTIVES FUNCTIONS --------------------
def get_all_admin_objectives():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM admin_objectives ORDER BY objective_id")
        objectives = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return objectives
    except Exception as e:
        print(f"Error fetching Admin objectives: {e}")
        return []

def save_admin_evaluation_with_evidence(objective_id, data_entry_value, reviewed_by, remarks, evidence_filename, evidence_content, evidence_text):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT previous_achievement FROM admin_objectives WHERE id = %s", (objective_id,))
        result = cursor.fetchone()
        if not result:
            return False
        previous = float(result[0]) if result[0] else 0
        actual = float(data_entry_value) if data_entry_value else 0
        if previous > 0:
            growth_rate = ((actual - previous) / previous) * 100
            percentage = (actual / previous) * 100
            if percentage < 70:
                status = "Not Achieved"
            elif 70 <= percentage < 100:
                status = "Partially Achieved"
            else:
                status = "Achieved"
        else:
            growth_rate = 0
            status = "Achieved" if actual > 0 else "Not Achieved"
        achievement = actual
        encoded_evidence = None
        if evidence_content:
            encoded_evidence = base64.b64encode(evidence_content).decode('utf-8')
        query = """
            UPDATE admin_objectives 
            SET data_entry_value = %s, growth_rate = %s, date_of_review = CURRENT_DATE,
                achievement = %s, status = %s, evidence = %s, evidence_filename = %s,
                evidence_text = %s, reviewed_by = %s, remarks = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (data_entry_value, growth_rate, achievement, status, encoded_evidence,
                              evidence_filename, evidence_text, reviewed_by, remarks, objective_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving Admin evaluation: {e}")
        return False

# -------------------- OPERATION OBJECTIVES FUNCTIONS --------------------
def get_all_operation_objectives():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM operation_objectives ORDER BY objective_id")
        objectives = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return objectives
    except Exception as e:
        print(f"Error fetching Operation objectives: {e}")
        return []

def save_operation_evaluation_with_evidence(objective_id, data_entry_value, reviewed_by, remarks, evidence_filename, evidence_content, evidence_text):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT previous_achievement FROM operation_objectives WHERE id = %s", (objective_id,))
        result = cursor.fetchone()
        if not result:
            return False
        previous = float(result[0]) if result[0] else 0
        actual = float(data_entry_value) if data_entry_value else 0
        if previous > 0:
            growth_rate = ((actual - previous) / previous) * 100
            percentage = (actual / previous) * 100
            if percentage < 70:
                status = "Not Achieved"
            elif 70 <= percentage < 100:
                status = "Partially Achieved"
            else:
                status = "Achieved"
        else:
            growth_rate = 0
            status = "Achieved" if actual > 0 else "Not Achieved"
        achievement = actual
        encoded_evidence = None
        if evidence_content:
            encoded_evidence = base64.b64encode(evidence_content).decode('utf-8')
        query = """
            UPDATE operation_objectives 
            SET data_entry_value = %s, growth_rate = %s, date_of_review = CURRENT_DATE,
                achievement = %s, status = %s, evidence = %s, evidence_filename = %s,
                evidence_text = %s, reviewed_by = %s, remarks = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (data_entry_value, growth_rate, achievement, status, encoded_evidence,
                              evidence_filename, evidence_text, reviewed_by, remarks, objective_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving Operation evaluation: {e}")
        return False

# -------------------- PROCUREMENT OBJECTIVES FUNCTIONS --------------------
def get_all_procurement_objectives():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM procurement_objectives ORDER BY objective_id")
        objectives = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return objectives
    except Exception as e:
        print(f"Error fetching Procurement objectives: {e}")
        return []

def save_procurement_evaluation_with_evidence(objective_id, data_entry_value, reviewed_by, remarks, evidence_filename, evidence_content, evidence_text):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT previous_achievement FROM procurement_objectives WHERE id = %s", (objective_id,))
        result = cursor.fetchone()
        if not result:
            return False
        previous = float(result[0]) if result[0] else 0
        actual = float(data_entry_value) if data_entry_value else 0
        if previous > 0:
            growth_rate = ((actual - previous) / previous) * 100
            percentage = (actual / previous) * 100
            if percentage < 70:
                status = "Not Achieved"
            elif 70 <= percentage < 100:
                status = "Partially Achieved"
            else:
                status = "Achieved"
        else:
            growth_rate = 0
            status = "Achieved" if actual > 0 else "Not Achieved"
        achievement = actual
        encoded_evidence = None
        if evidence_content:
            encoded_evidence = base64.b64encode(evidence_content).decode('utf-8')
        query = """
            UPDATE procurement_objectives 
            SET data_entry_value = %s, growth_rate = %s, date_of_review = CURRENT_DATE,
                achievement = %s, status = %s, evidence = %s, evidence_filename = %s,
                evidence_text = %s, reviewed_by = %s, remarks = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (data_entry_value, growth_rate, achievement, status, encoded_evidence,
                              evidence_filename, evidence_text, reviewed_by, remarks, objective_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving Procurement evaluation: {e}")
        return False

# -------------------- NRC / AUDIT CHECKLIST FUNCTIONS --------------------
def get_audit_checklist():
    """Get all audit checklist items from database"""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
            SELECT 
                id,
                clause,
                description,
                qms_9001,
                ems_14001,
                ohsms_45001,
                itsms_20000_1,
                isms_27001,
                status,
                findings_remarks
            FROM audit_checklist 
            ORDER BY id ASC
        """)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                'id': row['id'],
                'clause': row['clause'] if row['clause'] else '',
                'description': row['description'] if row['description'] else '',
                'qms_9001': row['qms_9001'] if row['qms_9001'] else 'Not Started',
                'ems_14001': row['ems_14001'] if row['ems_14001'] else 'Not Started',
                'ohsms_45001': row['ohsms_45001'] if row['ohsms_45001'] else 'Not Started',
                'itsms_20000_1': row['itsms_20000_1'] if row['itsms_20000_1'] else 'Not Started',
                'isms_27001': row['isms_27001'] if row['isms_27001'] else 'Not Started',
                'status': row['status'] if row['status'] else 'Not Started',
                'findings_remarks': row['findings_remarks'] if row['findings_remarks'] else ''
            })
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Error fetching audit checklist: {e}")
        return []

def update_audit_checklist_status(item_id, status, findings_remarks):
    """Update audit checklist item status"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE audit_checklist 
            SET status = %s,
                findings_remarks = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (status, findings_remarks, item_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating audit checklist: {e}")
        return False

def update_audit_checklist_standard(item_id, standard, value):
    """Update specific standard status in audit checklist"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        # Map standard to column name
        standard_columns = {
            'qms_9001': 'qms_9001',
            'ems_14001': 'ems_14001',
            'ohsms_45001': 'ohsms_45001',
            'itsms_20000_1': 'itsms_20000_1',
            'isms_27001': 'isms_27001'
        }
        column = standard_columns.get(standard)
        if not column:
            return False
        
        query = f"""
            UPDATE audit_checklist 
            SET {column} = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        cursor.execute(query, (value, item_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating audit checklist standard: {e}")
        return False

def add_audit_checklist_item(clause, description, qms_9001, ems_14001, ohsms_45001, itsms_20000_1, isms_27001, status, findings_remarks):
    """Add new audit checklist item"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audit_checklist 
            (clause, description, qms_9001, ems_14001, ohsms_45001, itsms_20000_1, isms_27001, status, findings_remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (clause, description, qms_9001 or 'Not Started', ems_14001 or 'Not Started', 
              ohsms_45001 or 'Not Started', itsms_20000_1 or 'Not Started', isms_27001 or 'Not Started',
              status or 'Not Started', findings_remarks))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding audit checklist item: {e}")
        return False

def delete_audit_checklist_item(item_id):
    """Delete audit checklist item"""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM audit_checklist WHERE id = %s", (item_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting audit checklist item: {e}")
        return False

# -------------------- ADD MISSING COLUMNS --------------------
def add_missing_columns():
    """Add missing columns to tables"""
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Tables to check
        tables = ['bd_objectives', 'hr_business', 'admin_objectives', 'operation_objectives', 'procurement_objectives']
        
        for table in tables:
            # Check and add evidence_filename
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table}' AND column_name = 'evidence_filename'
            """)
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN evidence_filename VARCHAR(255)")
                print(f"✅ Added evidence_filename column to {table}")
            
            # Check and add evidence_text
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table}' AND column_name = 'evidence_text'
            """)
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN evidence_text TEXT")
                print(f"✅ Added evidence_text column to {table}")
            
            # Check and add evidence_uploaded_at
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table}' AND column_name = 'evidence_uploaded_at'
            """)
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN evidence_uploaded_at TIMESTAMP")
                print(f"✅ Added evidence_uploaded_at column to {table}")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ All columns added successfully!")
        return True
    except Exception as e:
        print(f"Error adding columns: {e}")
        return False

# Run test if executed directly
if __name__ == "__main__":
    print("=" * 60)
    print("ADDING MISSING COLUMNS...")
    print("=" * 60)
    add_missing_columns()
    
    print("\n" + "=" * 60)
    print("TESTING DATABASE CONNECTION...")
    print("=" * 60)
    test_database()
    
    print("\n" + "=" * 60)
    print("FINANCE DATA:")
    print("=" * 60)
    
    print("\n--- Main Finance ---")
    finance_data = get_all_finance_data()
    for data in finance_data:
        print(f"  {data['year']}: {data['amount']}")
    
    print("\n--- HR Finance ---")
    hr_finance = get_all_hr_finance_data()
    for data in hr_finance:
        print(f"  {data['year']}: {data['amount']}")
    
    print("\n--- Admin Finance ---")
    admin_finance = get_all_admin_finance_data()
    for data in admin_finance:
        print(f"  {data['year']}: {data['amount']}")
    
    print("\n--- Operation Finance ---")
    operation_finance = get_all_operation_finance_data()
    for data in operation_finance:
        print(f"  {data['year']}: {data['amount']}")
    
    print("\n--- Procurement Finance ---")
    procurement_finance = get_all_procurement_finance_data()
    for data in procurement_finance:
        print(f"  {data['year']}: {data['amount']}")
    
    print("\n" + "=" * 60)
    print("AUDIT CHECKLIST DATA:")
    print("=" * 60)
    audit_data = get_audit_checklist()
    for item in audit_data:
        print(f"  {item['id']} | {item['clause']} | {item['description']} | {item['status']}")