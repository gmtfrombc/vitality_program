from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from database import init_db, add_patient_data, get_patient_data
from prompts import generate_prompt  # Import the generate_prompt function

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/entry', methods=['GET', 'POST'])
def entry():
    if request.method == 'POST':
        patient_data = {
            'name': request.form.get('name'),

            # Surveys
            'date_completed_priorities': request.form.get('date_completed_priorities'),
            'nutrition_priority': request.form.get('nutrition_priority'),
            'exercise_priority': request.form.get('exercise_priority'),
            'sleep_priority': request.form.get('sleep_priority'),
            'stress_priority': request.form.get('stress_priority'),
            'relationships_priority': request.form.get('relationships_priority'),

            'date_completed_readiness': request.form.get('date_completed_readiness'),
            'importance_readiness': request.form.get('importance_readiness'),
            'confidence_readiness': request.form.get('confidence_readiness'),

            'date_completed_mental_health': request.form.get('date_completed_mental_health'),
            'phq9_score': request.form.get('phq9_score'),
            'gad7_score': request.form.get('gad7_score'),

            # Biometric Data
            'date_completed_biometrics': request.form.get('date_completed_biometrics'),
            'fasting_glucose': request.form.get('fasting_glucose'),
            'total_cholesterol': request.form.get('total_cholesterol'),
            'triglycerides': request.form.get('triglycerides'),
            'hdl_cholesterol': request.form.get('hdl_cholesterol'),
            'apolipoprotein_b': request.form.get('apolipoprotein_b'),
            'hba1c': request.form.get('hba1c'),
            'alt': request.form.get('alt'),

            # Vital Signs
            'date_completed_vitals': request.form.get('date_completed_vitals'),
            'blood_pressure': request.form.get('blood_pressure'),
            'weight': request.form.get('weight'),
            'bmi': request.form.get('bmi'),
            'vitality_score': request.form.get('vitality_score'),

            # Encounters
            'encounter_dates': request.form.getlist('date_completed_encounter[]'),
            'encounter_types': request.form.getlist('encounter_type[]'),
            'encounter_documents': request.form.getlist('encounter_document[]'),

            # SMS Messages
            'sms_dates': request.form.getlist('date_completed_sms[]'),
            'sms_contents': request.form.getlist('sms_content[]'),

            # Appointments
            'provider_scheduled': request.form.get('provider_scheduled'),
            'provider_completed': request.form.get('provider_completed'),
            'provider_missed': request.form.get('provider_missed'),
            'coach_scheduled': request.form.get('coach_scheduled'),
            'coach_completed': request.form.get('coach_completed'),
            'coach_missed': request.form.get('coach_missed'),

            # Goals and Progress
            'date_completed_goals': request.form.get('date_completed_goals'),
            'weight_loss_goal': request.form.get('weight_loss_goal'),
            'vitality_score_goal': request.form.get('vitality_score_goal')
        }

        add_patient_data(patient_data)
        flash('Patient data added successfully!')
        return redirect(url_for('index'))
    return render_template('entry_form.html')


@app.route('/summary/<int:patient_id>')
def summary(patient_id):
    patient_data = get_patient_data(patient_id)
    if patient_data:
        prompt_text = generate_prompt(patient_data)
        return render_template('summary.html', prompt_text=prompt_text)
    else:
        flash('Patient data not found!')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
