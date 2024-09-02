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
        # Use the form's provided values; only include fields that were actually filled out
        patient_data = {
            'mrn': request.form.get('mrn'),
            'name': request.form.get('name'),
            'date_completed_priorities': request.form.get('date_completed_priorities') or None,
            'nutrition_priority': request.form.get('nutrition_priority') or None,
            'exercise_priority': request.form.get('exercise_priority') or None,
            'sleep_priority': request.form.get('sleep_priority') or None,
            'stress_priority': request.form.get('stress_priority') or None,
            'relationships_priority': request.form.get('relationships_priority') or None,
            'date_completed_readiness': request.form.get('date_completed_readiness') or None,
            'importance_readiness': request.form.get('importance_readiness') or None,
            'confidence_readiness': request.form.get('confidence_readiness') or None,
            'date_completed_mental_health': request.form.get('date_completed_mental_health') or None,
            'phq9_score': request.form.get('phq9_score') or None,
            'gad7_score': request.form.get('gad7_score') or None,
            'date_completed_biometrics': request.form.get('date_completed_biometrics') or None,
            'fasting_glucose': request.form.get('fasting_glucose') or None,
            'total_cholesterol': request.form.get('total_cholesterol') or None,
            'triglycerides': request.form.get('triglycerides') or None,
            'hdl_cholesterol': request.form.get('hdl_cholesterol') or None,
            'apolipoprotein_b': request.form.get('apolipoprotein_b') or None,
            'hba1c': request.form.get('hba1c') or None,
            'alt': request.form.get('alt') or None,
            'date_completed_vitals': request.form.get('date_completed_vitals') or None,
            'blood_pressure': request.form.get('blood_pressure') or None,
            'weight': request.form.get('weight') or None,
            'bmi': request.form.get('bmi') or None,
            'vitality_score': request.form.get('vitality_score') or None,
            'encounter_dates': request.form.getlist('date_completed_encounter[]'),
            'encounter_types': request.form.getlist('encounter_type[]'),
            'encounter_documents': request.form.getlist('encounter_document[]'),
            'sms_dates': request.form.getlist('date_completed_sms[]'),
            'sms_contents': request.form.getlist('sms_content[]'),
            'provider_scheduled': request.form.get('provider_scheduled') or None,
            'provider_completed': request.form.get('provider_completed') or None,
            'provider_missed': request.form.get('provider_missed') or None,
            'coach_scheduled': request.form.get('coach_scheduled') or None,
            'coach_completed': request.form.get('coach_completed') or None,
            'coach_missed': request.form.get('coach_missed') or None,
            'date_completed_goals': request.form.get('date_completed_goals') or None,
            'weight_loss_goal': request.form.get('weight_loss_goal') or None,
            'vitality_score_goal': request.form.get('vitality_score_goal') or None
        }

        # Remove empty keys where no data was entered
        patient_data = {k: v for k, v in patient_data.items() if v is not None}

        try:
            add_patient_data(patient_data)
            flash('Patient data added successfully!')
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
