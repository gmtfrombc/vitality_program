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
    print("add_patient_data function called")
    print(f"Received patient_data: {patient_data}")

    conn = sqlite3.connect('vp.db')
    cursor = conn.cursor()

    # Insert patient record if it doesn't already exist
    cursor.execute('''INSERT OR IGNORE INTO patients (mrn, name) VALUES (?, ?)''',
                   (patient_data['mrn'], patient_data['name']))

    # Get the patient ID based on the MRN
    cursor.execute("SELECT id FROM patients WHERE mrn = ?",
                   (patient_data['mrn'],))
    patient_id = cursor.fetchone()[0]

    # Debug: Check patient_id and data
    print(f"Patient ID: {patient_id}")

    # Handle Priorities Survey
    if patient_data.get('date_completed_priorities'):
        cursor.execute('''REPLACE INTO surveys (
            id, patient_id, date_completed_priorities, nutrition_priority, exercise_priority, 
            sleep_priority, stress_priority, relationships_priority) 
            VALUES ((SELECT id FROM surveys WHERE patient_id = ? AND date_completed_priorities IS NOT NULL), ?, ?, ?, ?, ?, ?, ?)''', (
            patient_id, patient_id, patient_data['date_completed_priorities'],
            patient_data.get('nutrition_priority'),
            patient_data.get('exercise_priority'),
            patient_data.get('sleep_priority'),
            patient_data.get('stress_priority'),
            patient_data.get('relationships_priority')
        ))
        print("Inserted/Updated Priorities Survey")

    # Handle Readiness Survey
    if patient_data.get('date_completed_readiness'):
        cursor.execute('''REPLACE INTO surveys (
            id, patient_id, date_completed_readiness, importance_readiness, confidence_readiness) 
            VALUES ((SELECT id FROM surveys WHERE patient_id = ? AND date_completed_readiness IS NOT NULL), ?, ?, ?, ?)''', (
            patient_id, patient_id, patient_data['date_completed_readiness'],
            patient_data.get('importance_readiness'),
            patient_data.get('confidence_readiness')
        ))
        print("Inserted/Updated Readiness Survey")

    # Insert Mental Health Survey data as a new row
    if patient_data.get('date_completed_mental_health'):
        cursor.execute('''INSERT INTO surveys (
            patient_id, date_completed_mental_health, phq9_score, gad7_score) 
            VALUES (?, ?, ?, ?)''', (
            patient_id, patient_data['date_completed_mental_health'],
            patient_data.get('phq9_score'),
            patient_data.get('gad7_score')
        ))
        print("Inserted Mental Health Survey")

    # Insert Biometric Data
    if patient_data.get('date_completed_biometrics'):
        cursor.execute('''INSERT INTO biometric_data (
            patient_id, date_completed, fasting_glucose, total_cholesterol, triglycerides, 
            hdl_cholesterol, apolipoprotein_b, hba1c, alt) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            patient_id, patient_data.get('date_completed_biometrics'),
            patient_data.get('fasting_glucose'), patient_data.get(
                'total_cholesterol'),
            patient_data.get('triglycerides'), patient_data.get(
                'hdl_cholesterol'),
            patient_data.get('apolipoprotein_b'), patient_data.get(
                'hba1c'), patient_data.get('alt')
        ))
        print("Inserted Biometric Data")

    # Insert Vital Signs
    if any([patient_data.get('blood_pressure'), patient_data.get('weight'),
            patient_data.get('bmi'), patient_data.get('vitality_score')]):
        cursor.execute('''INSERT INTO vital_signs (
            patient_id, date_completed, blood_pressure, weight, bmi, vitality_score) 
            VALUES (?, ?, ?, ?, ?, ?)''', (
            patient_id, patient_data.get('date_completed_vitals'),
            patient_data.get('blood_pressure'), patient_data.get('weight'),
            patient_data.get('bmi'), patient_data.get('vitality_score')
        ))
        print("Inserted Vital Signs")

    # Handle Encounters
    if 'encounter_dates' in patient_data and 'encounter_types' in patient_data and 'encounter_documents' in patient_data:
        for date, type_, document in zip(patient_data['encounter_dates'], patient_data['encounter_types'], patient_data['encounter_documents']):
            if date and type_ and document:  # Ensure all fields are non-empty
                cursor.execute('''INSERT INTO encounters (
                    patient_id, date_completed, encounter_type, encounter_document) 
                    VALUES (?, ?, ?, ?)''', (
                    patient_id, date, type_, document
                ))

    # Handle SMS Messages
    if 'sms_dates' in patient_data and 'sms_contents' in patient_data:
        for date, content in zip(patient_data['sms_dates'], patient_data['sms_contents']):
            if date and content:  # Ensure fields are non-empty
                cursor.execute('''INSERT INTO sms_messages (
                    patient_id, date_completed, sms_content) 
                    VALUES (?, ?, ?)''', (
                    patient_id, date, content
                ))

            # Handle Provider Appointments
    if 'provider_scheduled' in patient_data and 'provider_completed' in patient_data and 'provider_missed' in patient_data:
        cursor.execute(
            '''SELECT id FROM appointments WHERE patient_id = ? AND appointment_type = 'Provider' ''', (patient_id,))
        provider_record = cursor.fetchone()
        print(f"Provider appointment record exists: {provider_record}")
        if provider_record:  # If record exists, update it
            cursor.execute('''UPDATE appointments 
                              SET scheduled = ?, completed = ?, missed = ? 
                              WHERE patient_id = ? AND appointment_type = 'Provider' ''', (
                patient_data['provider_scheduled'],
                patient_data['provider_completed'],
                patient_data['provider_missed'],
                patient_id
            ))
            print(f"Updated Provider appointment for patient_id: {patient_id}")
        else:  # Insert a new record
            cursor.execute('''INSERT INTO appointments (
                patient_id, appointment_type, scheduled, completed, missed) 
                VALUES (?, 'Provider', ?, ?, ?)''', (
                patient_id,
                patient_data['provider_scheduled'],
                patient_data['provider_completed'],
                patient_data['provider_missed']
            ))
            print(f"Inserted new Provider appointment for patient_id: {
                  patient_id}")

    # Handle Coach Appointments
    if 'coach_scheduled' in patient_data and 'coach_completed' in patient_data and 'coach_missed' in patient_data:
        cursor.execute(
            '''SELECT id FROM appointments WHERE patient_id = ? AND appointment_type = 'Coach' ''', (patient_id,))
        coach_record = cursor.fetchone()
        print(f"Coach appointment record exists: {coach_record}")
        if coach_record:  # If record exists, update it
            cursor.execute('''UPDATE appointments 
                              SET scheduled = ?, completed = ?, missed = ? 
                              WHERE patient_id = ? AND appointment_type = 'Coach' ''', (
                patient_data['coach_scheduled'],
                patient_data['coach_completed'],
                patient_data['coach_missed'],
                patient_id
            ))
            print(f"Updated Coach appointment for patient_id: {patient_id}")
        else:  # Insert a new record
            cursor.execute('''INSERT INTO appointments (
                patient_id, appointment_type, scheduled, completed, missed) 
                VALUES (?, 'Coach', ?, ?, ?)''', (
                patient_id,
                patient_data['coach_scheduled'],
                patient_data['coach_completed'],
                patient_data['coach_missed']
            ))
            print(f"Inserted new Coach appointment for patient_id: {
                  patient_id}")

            # Handle Goals (Weight Loss Goal and Vitality Score Goal)
    if 'weight_loss_goal' in patient_data or 'vitality_score_goal' in patient_data:
        cursor.execute('''REPLACE INTO goals (
            id, patient_id, date_completed, weight_loss_goal, vitality_score_goal) 
            VALUES ((SELECT id FROM goals WHERE patient_id = ?), ?, (SELECT date_completed FROM goals WHERE patient_id = ?), ?, ?)''', (
            patient_id, patient_id, patient_id,
            patient_data.get('weight_loss_goal', 'N/A'),
            patient_data.get('vitality_score_goal', 'N/A')
        ))

    # Commit the transaction and close the connection
    print("Committing transaction")


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
        'name': patient[1]
    }

    # Fetch all surveys for the patient
    cursor.execute("SELECT * FROM surveys WHERE patient_id = ?", (patient_id,))
    surveys = cursor.fetchall()

    # Separate surveys data into respective categories
    patient_data['priorities'] = []
    patient_data['readiness'] = []
    patient_data['mental_health'] = []

    for survey in surveys:
        if survey[2]:  # date_completed_priorities exists
            patient_data['priorities'].append({
                'date_completed': survey[2],
                'nutrition_priority': survey[3],
                'exercise_priority': survey[4],
                'sleep_priority': survey[5],
                'stress_priority': survey[6],
                'relationships_priority': survey[7]
            })
        if survey[8]:  # date_completed_readiness exists
            patient_data['readiness'].append({
                'date_completed': survey[8],
                'importance_readiness': survey[9],
                'confidence_readiness': survey[10]
            })
        if survey[11]:  # date_completed_mental_health exists
            patient_data['mental_health'].append({
                'date_completed': survey[11],
                'phq9_score': survey[12],
                'gad7_score': survey[13]
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

    # Appointments
    cursor.execute(
        "SELECT * FROM appointments WHERE patient_id = ?", (patient_id,))
    appointments = cursor.fetchall()
    patient_data['appointments'] = {
        'provider': {'scheduled': 0, 'completed': 0, 'missed': 0},
        'coach': {'scheduled': 0, 'completed': 0, 'missed': 0}
    }

    for appointment in appointments:
        if appointment[3] == 'Provider':  # Assuming 'appointment_type' is in the 4th column
            patient_data['appointments']['provider'] = {
                'scheduled': appointment[4],
                'completed': appointment[5],
                'missed': appointment[6]
            }
        elif appointment[3] == 'Coach':  # Adjusting this to match your data
            patient_data['appointments']['coach'] = {
                'scheduled': appointment[4],
                'completed': appointment[5],
                'missed': appointment[6]
            }

    conn.close()

    return patient_data
