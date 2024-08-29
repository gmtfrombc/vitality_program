import sqlite3


def init_db():
    conn = sqlite3.connect('vitality_program.db')
    cursor = conn.cursor()

    # Create the Patients table
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )''')

    # Create the Surveys table
    cursor.execute('''CREATE TABLE IF NOT EXISTS surveys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        date_completed DATE,
        nutrition_priority INTEGER,
        exercise_priority INTEGER,
        sleep_priority INTEGER,
        stress_priority INTEGER,
        relationships_priority INTEGER,
        importance_readiness INTEGER,
        confidence_readiness INTEGER,
        phq9_score INTEGER,
        gad7_score INTEGER,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )''')

    # Create the Biometric Data table
    cursor.execute('''CREATE TABLE IF NOT EXISTS biometric_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        date_completed DATE,
        fasting_glucose REAL,
        total_cholesterol REAL,
        triglycerides REAL,
        hdl_cholesterol REAL,
        apolipoprotein_b REAL,
        hba1c REAL,
        alt REAL,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )''')

    # Create the Vital Signs table
    cursor.execute('''CREATE TABLE IF NOT EXISTS vital_signs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        date_completed DATE,
        blood_pressure TEXT,
        weight REAL,
        bmi REAL,
        vitality_score INTEGER,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )''')

    # Create the Encounters table
    cursor.execute('''CREATE TABLE IF NOT EXISTS encounters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        date_completed DATE,
        encounter_type TEXT,
        encounter_document TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )''')

    # Create the SMS Messages table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sms_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        date_completed DATE,
        sms_content TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )''')

    # Create the Appointments table
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        date_completed DATE,
        appointment_type TEXT,
        scheduled INTEGER,
        completed INTEGER,
        missed INTEGER,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )''')

    # Create the Goals and Progress table
    cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        date_completed DATE,
        weight_loss_goal REAL,
        vitality_score_goal INTEGER,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )''')

    conn.commit()
    conn.close()

# Method to add patient data to the respective tables


def add_patient_data(patient_data):
    conn = sqlite3.connect('vitality_program.db')
    cursor = conn.cursor()

    # Insert patient record
    cursor.execute('''INSERT INTO patients (name) VALUES (?)''',
                   (patient_data['name'],))
    patient_id = cursor.lastrowid

    # Insert surveys data
    cursor.execute('''INSERT INTO surveys (
        patient_id, date_completed, nutrition_priority, exercise_priority, sleep_priority, 
        stress_priority, relationships_priority, importance_readiness, confidence_readiness, 
        phq9_score, gad7_score) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        patient_id, patient_data['date_completed_survey'], patient_data['nutrition_priority'],
        patient_data['exercise_priority'], patient_data['sleep_priority'], patient_data['stress_priority'],
        patient_data['relationships_priority'], patient_data['importance_readiness'],
        patient_data['confidence_readiness'], patient_data['phq9_score'], patient_data['gad7_score']
    ))

    # Insert biometric data
    cursor.execute('''INSERT INTO biometric_data (
        patient_id, date_completed, fasting_glucose, total_cholesterol, triglycerides, 
        hdl_cholesterol, apolipoprotein_b, hba1c, alt) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        patient_id, patient_data['date_completed_biometrics'], patient_data['fasting_glucose'],
        patient_data['total_cholesterol'], patient_data['triglycerides'], patient_data['hdl_cholesterol'],
        patient_data['apolipoprotein_b'], patient_data['hba1c'], patient_data['alt']
    ))

    # Insert vital signs data
    cursor.execute('''INSERT INTO vital_signs (
        patient_id, date_completed, blood_pressure, weight, bmi, vitality_score) 
        VALUES (?, ?, ?, ?, ?, ?)''', (
        patient_id, patient_data['date_completed_vitals'], patient_data['blood_pressure'],
        patient_data['weight'], patient_data['bmi'], patient_data['vitality_score']
    ))

    # Insert encounters data
    for i in range(len(patient_data['encounter_dates'])):
        cursor.execute('''INSERT INTO encounters (
            patient_id, date_completed, encounter_type, encounter_document) 
            VALUES (?, ?, ?, ?)''', (
            patient_id, patient_data['encounter_dates'][i], patient_data['encounter_types'][i],
            patient_data['encounter_documents'][i]
        ))

    # Insert SMS messages data
    for i in range(len(patient_data['sms_dates'])):
        cursor.execute('''INSERT INTO sms_messages (
            patient_id, date_completed, sms_content) 
            VALUES (?, ?, ?)''', (
            patient_id, patient_data['sms_dates'][i], patient_data['sms_contents'][i]
        ))

    # Insert appointments data (Provider)
    cursor.execute('''INSERT INTO appointments (
        patient_id, date_completed, appointment_type, scheduled, completed, missed) 
        VALUES (?, ?, ?, ?, ?, ?)''', (
        patient_id, patient_data['date_completed_appointment'], 'Provider',
        patient_data['provider_scheduled'], patient_data['provider_completed'],
        patient_data['provider_missed']
    ))

    # Insert appointments data (Health Coach)
    cursor.execute('''INSERT INTO appointments (
        patient_id, date_completed, appointment_type, scheduled, completed, missed) 
        VALUES (?, ?, ?, ?, ?, ?)''', (
        patient_id, patient_data['date_completed_appointment'], 'Health Coach',
        patient_data['coach_scheduled'], patient_data['coach_completed'],
        patient_data['coach_missed']
    ))

    # Insert goals and progress data
    cursor.execute('''INSERT INTO goals (
        patient_id, date_completed, weight_loss_goal, vitality_score_goal) 
        VALUES (?, ?, ?, ?)''', (
        patient_id, patient_data['date_completed_goals'], patient_data['weight_loss_goal'],
        patient_data['vitality_score_goal']
    ))

    conn.commit()
    conn.close()

# Method to retrieve patient data


def get_patient_data(patient_id):
    conn = sqlite3.connect('vitality_program.db')
    cursor = conn.cursor()

    # Fetch data from different tables
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()

    cursor.execute("SELECT * FROM surveys WHERE patient_id = ?", (patient_id,))
    surveys = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM biometric_data WHERE patient_id = ?", (patient_id,))
    biometrics = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM vital_signs WHERE patient_id = ?", (patient_id,))
    vitals = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM encounters WHERE patient_id = ?", (patient_id,))
    encounters = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM sms_messages WHERE patient_id = ?", (patient_id,))
    sms_messages = cursor.fetchall()

    cursor.execute(
        "SELECT * FROM appointments WHERE patient_id = ?", (patient_id,))
    appointments = cursor.fetchall()

    cursor.execute("SELECT * FROM goals WHERE patient_id = ?", (patient_id,))
    goals = cursor.fetchall()

    conn.close()

    # Aggregate the data as needed
    patient_data = {
        'name': patient[1],
        'surveys': surveys,
        'biometrics': biometrics,
        'vitals': vitals,
        'encounters': encounters,
        'sms_messages': sms_messages,
        'appointments': appointments,
        'goals': goals
    }

    return patient_data
