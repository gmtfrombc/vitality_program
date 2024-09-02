def generate_prompt(patient_data):
    # Priorities Survey Section
    priorities_survey = "\n".join([
        f"Date: {survey['date_completed']}\n"
        f"Scores: Diet: {survey['nutrition_priority']
                         }/5, Exercise: {survey['exercise_priority']}/5, "
        f"Sleep: {survey['sleep_priority']
                  }/5, Stress: {survey['stress_priority']}/5, "
        f"Relationships: {survey['relationships_priority']}/5"
        for survey in patient_data.get('priorities', [])
    ]) or "No Priorities Survey data available."

    # Readiness Survey Section
    readiness_survey = "\n".join([
        f"Date: {survey['date_completed']}\n"
        f"Scores: Importance of Health Change: {
            survey['importance_readiness']}/5, "
        f"Confidence in Making Change: {survey['confidence_readiness']}/5"
        for survey in patient_data.get('readiness', [])
    ]) or "No Readiness Survey data available."

    # Mental Health Survey Section
    mental_health_survey = "\n".join([
        f"Date: {survey['date_completed']}\n"
        f"PHQ-9 Score: {survey['phq9_score']
                        }/27, GAD-7 Score: {survey['gad7_score']}/21"
        for survey in patient_data.get('mental_health', [])
    ]) or "No Mental Health data available."

    # Biometric Data Section
    biometric_data = "\n".join([
        f"{data.get('date_completed')}: Fasting Glucose: {
            data.get('fasting_glucose')}, "
        f"Total Cholesterol: {data.get('total_cholesterol')}, HgbA1C: {
            data.get('hba1c')}, "
        f"Liver Function (ALT): {data.get('alt')}"
        for data in patient_data.get('biometrics', [])
    ]) or "No biometric data available."

    # Vital Signs Section
    vital_signs = "\n".join([
        f"{data.get('date_completed')}: Blood Pressure: {
            data.get('blood_pressure')}, "
        f"Weight: {data.get('weight')} lbs, BMI: {data.get(
            'bmi')}, Vitality Score: {data.get('vitality_score')}"
        for data in patient_data.get('vitals', [])
    ]) or "No vital signs data available."

    # Engagement Metrics Section
    encounters_summary = "\n".join([
        f"{date} {type_}: {document}"
        for date, type_, document in patient_data.get('encounters', [])
    ]) or "No encounter summaries available."

    sms_messages = "\n".join([
        f"{date}: {content}"
        for date, content in patient_data.get('sms_messages', [])
    ]) or "No SMS messages available."

    # Appointments Section
    appointments = patient_data.get(
        'appointments', {'provider': {}, 'coach': {}})
    provider_appointments = appointments.get(
        'provider', {'scheduled': 0, 'completed': 0, 'missed': 0})
    coach_appointments = appointments.get(
        'coach', {'scheduled': 0, 'completed': 0, 'missed': 0})

    appointment_summary = f"""
    Provider Appointments: {provider_appointments['scheduled']} scheduled, {provider_appointments['completed']} completed,
    {provider_appointments['missed']} missed.
    Coach Appointments: {coach_appointments['scheduled']} scheduled, {coach_appointments['completed']} completed,
    {coach_appointments['missed']} missed.
    """

    # Goals and Progress Section
    goals_progress = f"""
    Weight Loss Goal: Initial Target: {patient_data.get('weight_loss_goal', 'N/A')} lbs,
    Progress: {patient_data.get('weight_loss_progress', 'N/A')} lbs lost.
    Vitality Score Goal: Initial Target: {patient_data.get('vitality_score_goal', 'N/A')},
    Progress: Improved from {patient_data.get('initial_vitality_score', 'N/A')} to {patient_data.get('current_vitality_score', 'N/A')}.
    """

    # Construct the prompt
    prompt = f"""
    **Role of AI Agent:**
    As an AI health provider assistant, your task is to generate a concise and actionable summary of a patient's progress in the Vitality Program.
    Your summary should focus on analyzing key health metrics, assessing patient engagement levels, and identifying risk factors for dropping out
    of the program. Based on this analysis, provide specific recommendations for the healthcare provider.

    **Program Description:**
    The Vitality Program is a lifestyle management program designed to improve metabolic health through personalized coaching, regular monitoring,
    and behavior change support.

    **Patient Data for Analysis:**
    1. **Surveys:**
    Priorities Survey
    {priorities_survey}
    Readiness Survey
    {readiness_survey}
    Mental Health Surveys:
    {mental_health_survey}

    2. **Biometric Data:**
    {biometric_data}

    3. **Vital Signs:**
    {vital_signs}

    4. **Engagement Metrics:**
    Encounter Summaries:
    {encounters_summary}
    SMS Messages:
    {sms_messages}
    Appointment Summary
    {appointment_summary}

    5. **Goals and Progress:**
    {goals_progress}

    **Instructions:**
    - For Subsequent Data: Compare the current data with previous data points to identify any significant trends, improvements, or areas of concern.
    Assess how the patient is progressing in relation to their goals and identify any changes in engagement or risk of dropout. Review the encounter
    notes for any insights. Provide recommendations for the provider based on observed trends and changes.
    - Longitudinal Analysis: Emphasize the analysis of trends, such as improvements in key health metrics, consistency in engagement, and overall
    progress toward goals. Use this analysis to inform your recommendations.
    """
    return prompt
