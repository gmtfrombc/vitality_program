def generate_prompt(patient_data):
    # Surveys Section
    priorities_survey = f"""
    Date: {patient_data.get('date_completed_priorities', 'N/A')}
    Scores: Diet: {patient_data.get('nutrition_priority', 'N/A')}/5, Exercise: {patient_data.get('exercise_priority', 'N/A')}/5,
    Sleep: {patient_data.get('sleep_priority', 'N/A')}/5, Stress: {patient_data.get('stress_priority', 'N/A')}/5,
    Relationships: {patient_data.get('relationships_priority', 'N/A')}/5
    """

    readiness_survey = f"""
    Date: {patient_data.get('date_completed_readiness', 'N/A')}
    Scores: Importance of Health Change: {patient_data.get('importance_readiness', 'N/A')}/5,
    Confidence in Making Change: {patient_data.get('confidence_readiness', 'N/A')}/5
    """

    # Simplified logic to ensure data is displayed if available
    mental_health_survey = f"""
    Date: {patient_data.get('date_completed_mental_health', 'N/A')}
    PHQ-9 Score: {patient_data.get('phq9_score', 'N/A')}/27,
    GAD-7 Score: {patient_data.get('gad7_score', 'N/A')}/21
    """

    if not patient_data.get('date_completed_mental_health') and not patient_data.get('phq9_score') and not patient_data.get('gad7_score'):
        mental_health_survey = "No Mental Health data available."

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
        f"{date} {type}: {document}" for date, type, document in patient_data.get('encounters', [])
    ]) or "No encounter summaries available."

    sms_messages = "\n".join([
        f"{date}: {content}" for date, content in patient_data.get('sms_messages', [])
    ]) or "No SMS messages available."

    appointment_summary = f"""
    Provider Appointments: {patient_data.get('provider_scheduled', 0)} scheduled, {patient_data.get('provider_completed', 0)} completed,
    {patient_data.get('provider_missed', 0)} missed.
    Coach Appointments: {patient_data.get('coach_scheduled', 0)} scheduled, {patient_data.get('coach_completed', 0)} completed,
    {patient_data.get('coach_missed', 0)} missed.
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
    {priorities_survey}
    {readiness_survey}
    Mental Health:
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
