import sqlite3


def init_db():
    conn = sqlite3.connect('vp.db')
    cursor = conn.cursor()

    # Create the Patients table with MRN
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        mrn INTEGER UNIQUE NOT NULL
    )''')

    # Create the Surveys table
    cursor.execute('''CREATE TABLE IF NOT EXISTS surveys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        date_completed_priorities DATE,
        nutrition_priority INTEGER,
        exercise_priority INTEGER,
        sleep_priority INTEGER,
        stress_priority INTEGER,
        relationships_priority INTEGER,
        date_completed_readiness DATE,
        importance_readiness INTEGER,
        confidence_readiness INTEGER,
        date_completed_mental_health DATE,
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


def add_patient_data(patient_data):
    conn = sqlite3.connect('vp.db')
    cursor = conn.cursor()

    # Insert patient record if it doesn't already exist
    cursor.execute('''INSERT OR IGNORE INTO patients (mrn, name) VALUES (?, ?)''',
                   (patient_data['mrn'], patient_data['name']))

    # Get the patient ID based on the MRN
    cursor.execute("SELECT id FROM patients WHERE mrn = ?",
                   (patient_data['mrn'],))
    patient_id = cursor.fetchone()[0]

    # Insert surveys data if any field is filled
    if any([patient_data.get('date_completed_priorities'), patient_data.get('nutrition_priority'),
            patient_data.get('exercise_priority'), patient_data.get(
                'sleep_priority'),
            patient_data.get('stress_priority'), patient_data.get(
                'relationships_priority'),
            patient_data.get('date_completed_readiness'), patient_data.get(
                'importance_readiness'),
            patient_data.get('confidence_readiness'), patient_data.get(
                'date_completed_mental_health'),
            patient_data.get('phq9_score'), patient_data.get('gad7_score')]):
        cursor.execute('''INSERT INTO surveys (
            patient_id, date_completed_priorities, nutrition_priority, exercise_priority, 
            sleep_priority, stress_priority, relationships_priority, date_completed_readiness, 
            importance_readiness, confidence_readiness, date_completed_mental_health, phq9_score, gad7_score) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            patient_id, patient_data.get('date_completed_priorities'),
            patient_data.get('nutrition_priority'), patient_data.get(
                'exercise_priority'),
            patient_data.get('sleep_priority'), patient_data.get(
                'stress_priority'),
            patient_data.get('relationships_priority'), patient_data.get(
                'date_completed_readiness'),
            patient_data.get('importance_readiness'), patient_data.get(
                'confidence_readiness'),
            patient_data.get('date_completed_mental_health'), patient_data.get(
                'phq9_score'),
            patient_data.get('gad7_score')
        ))

     # Insert biometric data only if all relevant fields have been provided
    if patient_data.get('date_completed_biometrics') and any([
        patient_data.get('fasting_glucose'),
        patient_data.get('total_cholesterol'),
        patient_data.get('triglycerides'),
        patient_data.get('hdl_cholesterol'),
        patient_data.get('apolipoprotein_b'),
        patient_data.get('hba1c'),
        patient_data.get('alt')
    ]):
        cursor.execute('''INSERT INTO biometric_data (
            patient_id, date_completed, fasting_glucose, total_cholesterol, triglycerides, 
            hdl_cholesterol, apolipoprotein_b, hba1c, alt) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            patient_id, patient_data.get('date_completed_biometrics'),
            patient_data.get('fasting_glucose'), patient_data.get(
                'total_cholesterol'),
            patient_data.get('triglycerides'), patient_data.get(
                'hdl_cholesterol'),
            patient_data.get('apolipoprotein_b'), patient_data.get('hba1c'),
            patient_data.get('alt')
        ))

    # Insert vital signs data if any field is filled
    if any([patient_data.get('blood_pressure'), patient_data.get('weight'),
            patient_data.get('bmi'), patient_data.get('vitality_score')]):
        cursor.execute('''INSERT INTO vital_signs (
            patient_id, date_completed, blood_pressure, weight, bmi, vitality_score) 
            VALUES (?, ?, ?, ?, ?, ?)''', (
            patient_id, patient_data.get('date_completed_vitals'),
            patient_data.get('blood_pressure'), patient_data.get('weight'),
            patient_data.get('bmi'), patient_data.get('vitality_score')
        ))

    # Insert encounters data if all fields for at least one encounter are filled
    if 'encounter_dates' in patient_data and 'encounter_types' in patient_data and 'encounter_documents' in patient_data:
        for date, type_, document in zip(patient_data['encounter_dates'], patient_data['encounter_types'], patient_data['encounter_documents']):
            if date and type_ and document:  # Ensure all fields are non-empty
                cursor.execute('''INSERT INTO encounters (
                    patient_id, date_completed, encounter_type, encounter_document) 
                    VALUES (?, ?, ?, ?)''', (
                    patient_id, date, type_, document
                ))

    # Insert SMS messages data if both date and content are filled
    if 'sms_dates' in patient_data and 'sms_contents' in patient_data:
        for date, content in zip(patient_data['sms_dates'], patient_data['sms_contents']):
            if date and content:  # Ensure fields are non-empty
                cursor.execute('''INSERT INTO sms_messages (
                    patient_id, date_completed, sms_content) 
                    VALUES (?, ?, ?)''', (
                    patient_id, date, content
                ))

    # Insert goals and progress data if any field is filled
    if any([patient_data.get('weight_loss_goal'), patient_data.get('vitality_score_goal')]):
        cursor.execute('''INSERT INTO goals (
            patient_id, date_completed, weight_loss_goal, vitality_score_goal) 
            VALUES (?, ?, ?, ?)''', (
            patient_id, patient_data.get('date_completed_goals'),
            patient_data.get('weight_loss_goal'),
            patient_data.get('vitality_score_goal')
        ))

    conn.commit()
    conn.close()


def get_patient_data_by_mrn(mrn):
    conn = sqlite3.connect('vp.db')
    cursor = conn.cursor()

    # Fetch the patient's general information using MRN
    cursor.execute("SELECT * FROM patients WHERE mrn = ?", (mrn,))
    patient = cursor.fetchone()

    if patient is None:
        return None  # Handle the case where the patient doesn't exist

    patient_id = patient[0]  # Get patient_id to fetch data from other tables
    patient_data = {
        'id': patient[0],
        'mrn': patient[2],
        'name': patient[1]  # Assuming you want the name as well
    }

    # Surveys
    cursor.execute("SELECT * FROM surveys WHERE patient_id = ?", (patient_id,))
    surveys = cursor.fetchone()
    if surveys:
        patient_data.update({
            'date_completed_priorities': surveys[2],
            'nutrition_priority': surveys[3],
            'exercise_priority': surveys[4],
            'sleep_priority': surveys[5],
            'stress_priority': surveys[6],
            'relationships_priority': surveys[7],
            'date_completed_readiness': surveys[8],
            'importance_readiness': surveys[9],
            'confidence_readiness': surveys[10],
            'date_completed_mental_health': surveys[11],
            'phq9_score': surveys[12],
            'gad7_score': surveys[13],
        })
    else:
        # In case surveys data isn't found
        patient_data.update({
            'date_completed_mental_health': None,
            'phq9_score': None,
            'gad7_score': None,
        })

    # Biometric Data
    cursor.execute(
        "SELECT * FROM biometric_data WHERE patient_id = ?", (patient_id,))
    biometrics = cursor.fetchall()
    patient_data['biometrics'] = [{'date_completed': row[2], 'fasting_glucose': row[3], 'total_cholesterol': row[4],
                                   'triglycerides': row[5], 'hdl_cholesterol': row[6], 'apolipoprotein_b': row[7],
                                   'hba1c': row[8], 'alt': row[9]} for row in biometrics]

    # Vital Signs
    cursor.execute(
        "SELECT * FROM vital_signs WHERE patient_id = ?", (patient_id,))
    vitals = cursor.fetchall()
    patient_data['vitals'] = [{'date_completed': row[2], 'blood_pressure': row[3],
                               'weight': row[4], 'bmi': row[5], 'vitality_score': row[6]} for row in vitals]

    # Encounters
    cursor.execute(
        "SELECT * FROM encounters WHERE patient_id = ?", (patient_id,))
    encounters = cursor.fetchall()
    patient_data['encounters'] = [(row[2], row[3], row[4])
                                  for row in encounters]

    # SMS Messages
    cursor.execute(
        "SELECT * FROM sms_messages WHERE patient_id = ?", (patient_id,))
    sms_messages = cursor.fetchall()
    patient_data['sms_messages'] = [(row[2], row[3]) for row in sms_messages]

    # Goals
    cursor.execute("SELECT * FROM goals WHERE patient_id = ?", (patient_id,))
    goals = cursor.fetchone()
    if goals:
        patient_data.update({
            'date_completed_goals': goals[2],
            'weight_loss_goal': goals[3],
            'vitality_score_goal': goals[4]
        })

    conn.close()

    return patient_data
