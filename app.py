from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from database import init_db, add_patient_data, get_patient_data_by_mrn
from prompts import generate_prompt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
init_db()


@app.route('/')
def index():
    conn = sqlite3.connect('vp.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, mrn FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template('index.html', patients=patients)


@app.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        # Set default values or use the form's provided values
        patient_data = {
            'mrn': request.form.get('mrn', 123456),
            'name': request.form.get('name', 'Default Name') or 'Default Name',
            'date_completed_priorities': request.form.get('date_completed_priorities') or '2024-01-01',
            'nutrition_priority': request.form.get('nutrition_priority') or 3,
            'exercise_priority': request.form.get('exercise_priority') or 3,
            'sleep_priority': request.form.get('sleep_priority') or 3,
            'stress_priority': request.form.get('stress_priority') or 3,
            'relationships_priority': request.form.get('relationships_priority') or 3,
            'date_completed_readiness': request.form.get('date_completed_readiness') or '2024-01-01',
            'importance_readiness': request.form.get('importance_readiness') or 3,
            'confidence_readiness': request.form.get('confidence_readiness') or 3,
            'date_completed_mental_health': request.form.get('date_completed_mental_health') or '2024-01-01',
            'phq9_score': request.form.get('phq9_score') or 5,
            'gad7_score': request.form.get('gad7_score') or 5,
            'date_completed_biometrics': request.form.get('date_completed_biometrics') or '2024-01-01',
            'fasting_glucose': request.form.get('fasting_glucose') or 90,
            'total_cholesterol': request.form.get('total_cholesterol') or 200,
            'triglycerides': request.form.get('triglycerides') or 150,
            'hdl_cholesterol': request.form.get('hdl_cholesterol') or 50,
            'apolipoprotein_b': request.form.get('apolipoprotein_b') or 80,
            'hba1c': request.form.get('hba1c') or 5.5,
            'alt': request.form.get('alt') or 30,
            'date_completed_vitals': request.form.get('date_completed_vitals') or '2024-01-01',
            'blood_pressure': request.form.get('blood_pressure') or '120/80',
            'weight': request.form.get('weight') or 150,
            'bmi': request.form.get('bmi') or 22,
            'vitality_score': request.form.get('vitality_score') or 80,
            'encounter_dates': request.form.getlist('date_completed_encounter[]') or ['2024-01-01'],
            'encounter_types': request.form.getlist('encounter_type[]') or ['Default Encounter'],
            'encounter_documents': request.form.getlist('encounter_document[]') or ['Default Document'],
            'sms_dates': request.form.getlist('date_completed_sms[]') or ['2024-01-01'],
            'sms_contents': request.form.getlist('sms_content[]') or ['Default SMS Content'],
            'provider_scheduled': request.form.get('provider_scheduled') or 2,
            'provider_completed': request.form.get('provider_completed') or 1,
            'provider_missed': request.form.get('provider_missed') or 0,
            'coach_scheduled': request.form.get('coach_scheduled') or 2,
            'coach_completed': request.form.get('coach_completed') or 1,
            'coach_missed': request.form.get('coach_missed') or 0,
            'date_completed_goals': request.form.get('date_completed_goals') or '2024-01-01',
            'weight_loss_goal': request.form.get('weight_loss_goal') or 10,
            'vitality_score_goal': request.form.get('vitality_score_goal') or 90
        }

        try:
            add_patient_data(patient_data)
            flash('Patient data added successfully with default values!')
            return redirect(url_for('index'))
        except sqlite3.Error as e:
            flash(f'Error adding patient data: {str(e)}', 'error')
            return redirect(url_for('entry'))

    return render_template('entry_form.html')


@app.route('/summary/<int:mrn>')  # Update route to use mrn
def summary(mrn):  # Update function to accept mrn
    patient_data = get_patient_data_by_mrn(mrn)
    if patient_data is None:
        flash(f'Patient with MRN {mrn} not found!', 'error')
        return redirect(url_for('index'))

    print(patient_data)

    prompt_text = generate_prompt(patient_data)

    # Pass both prompt_text and patient_data to the template
    return render_template('summary.html', prompt_text=prompt_text, patient_data=patient_data)


if __name__ == '__main__':
    app.run(debug=True)
