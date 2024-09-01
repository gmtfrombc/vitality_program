import sqlite3


def print_patient_data(patient_id):
    conn = sqlite3.connect('vitality_program.db')
    cursor = conn.cursor()

    # Fetch and print patient general information
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()
    if patient:
        print("Patient Info:")
        print(f"ID: {patient[0]}, Name: {patient[1]}")
    else:
        print(f"No patient found with ID {patient_id}")
        return

    # Fetch and print survey data
    cursor.execute("SELECT * FROM surveys WHERE patient_id = ?", (patient_id,))
    surveys = cursor.fetchall()
    if surveys:
        print("\nSurveys:")
        for survey in surveys:
            print(survey)
    else:
        print("No surveys found.")

    # Fetch and print biometric data
    cursor.execute(
        "SELECT * FROM biometric_data WHERE patient_id = ?", (patient_id,))
    biometrics = cursor.fetchall()
    if biometrics:
        print("\nBiometric Data:")
        for bio in biometrics:
            print(bio)
    else:
        print("No biometric data found.")

    # Fetch and print vital signs data
    cursor.execute(
        "SELECT * FROM vital_signs WHERE patient_id = ?", (patient_id,))
    vitals = cursor.fetchall()
    if vitals:
        print("\nVital Signs:")
        for vital in vitals:
            print(vital)
    else:
        print("No vital signs data found.")

    # Fetch and print encounters data
    cursor.execute(
        "SELECT * FROM encounters WHERE patient_id = ?", (patient_id,))
    encounters = cursor.fetchall()
    if encounters:
        print("\nEncounters:")
        for enc in encounters:
            print(enc)
    else:
        print("No encounters data found.")

    # Fetch and print SMS messages data
    cursor.execute(
        "SELECT * FROM sms_messages WHERE patient_id = ?", (patient_id,))
    sms_messages = cursor.fetchall()
    if sms_messages:
        print("\nSMS Messages:")
        for sms in sms_messages:
            print(sms)
    else:
        print("No SMS messages found.")

    # Fetch and print appointments data
    cursor.execute(
        "SELECT * FROM appointments WHERE patient_id = ?", (patient_id,))
    appointments = cursor.fetchall()
    if appointments:
        print("\nAppointments:")
        for appt in appointments:
            print(appt)
    else:
        print("No appointments found.")

    # Fetch and print goals data
    cursor.execute("SELECT * FROM goals WHERE patient_id = ?", (patient_id,))
    goals = cursor.fetchall()
    if goals:
        print("\nGoals and Progress:")
        for goal in goals:
            print(goal)
    else:
        print("No goals data found.")

    conn.close()


# Call the function with the desired patient ID
print_patient_data(1)
