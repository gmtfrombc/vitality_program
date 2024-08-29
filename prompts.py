def generate_prompt(patient_data):
    prompt = f"""
    **Role of AI Agent:**
    As an AI health provider assistant, your task is to generate a concise and actionable summary of a patient's progress in the Vitality Program. Your summary should focus on analyzing key health metrics, assessing patient engagement levels, and identifying risk factors for dropping out of the program. Based on this analysis, provide specific recommendations for the healthcare provider.

    **Program Description:**
    The Vitality Program is a lifestyle management program designed to improve metabolic health through personalized coaching, regular monitoring, and behavior change support.

    **Patient Data for Analysis:**
    1. **Surveys:**
       - **Priorities Survey:** {patient_data['priorities_survey']}
       - **Readiness Survey:** {patient_data['readiness_survey']}
       - **Mental Health:**
         - **PHQ-9:** {patient_data['phq9_scores']}
         - **GAD-7:** {patient_data['gad7_scores']}
    2. **Biometric Data:** {patient_data['biometric_data']}
    3. **Vital Signs:** {patient_data['vital_signs']}
    4. **Engagement Metrics:** {patient_data['engagement_metrics']}
    5. **Goals and Progress:** {patient_data['goals_progress']}
    """
    return prompt
