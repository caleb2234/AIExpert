patient_conversation_history = """
user: Hi Abigail, what brings you in today?
patient: I've been having this irregular heartbeat that's making me really anxious. It's been affecting my work, and I'm quite worried about it.

user: Have you noticed when these episodes usually happen?
patient: They seem to happen at random, but I've noticed they sometimes occur after I've had a few cups of tea. Yesterday, it happened at work and lasted for about an hour, which was unusual.

user: Do you feel any pain, shortness of breath, or dizziness during these episodes?
patient: I don't feel any pain or shortness of breath. But I do feel weak and a bit faint during the episodes. It's really unsettling.
"""
patient_conversation_history2 = """
user: Hi Melissa, what brings you in today?
patient: I've been getting short of breath when I run. It's been getting worse, and now I can't finish my usual runs without stopping halfway to catch my breath.

user: Have you noticed when these episodes usually happen?
patient: Yes, the shortness of breath usually starts about halfway into my run, after around 15 minutes. It happens suddenly while I’m running.

user: Is it acute or chronic?
patient: It's been gradually getting worse over the past six months, so I'd say it's a chronic issue now.
"""
student_input2 = """
I'm thinking it's anxiety.
"""
flowchart = """
{
"S0_Dyspnea_Start": {
"text": "Starting point for Dyspnea diagnosis. Common causes include: congestive heart failure, pneumonia, reactive airway disease, pulmonary embolism, deconditioning, foreign body aspiration, DKA, anemia, undiagnosed asthma, pneumothorax, COPD, ARF/CKD. Is the dyspnea acute or chronic?",
"type": "question",
"choices": [
{ "text": "Acute", "next_node_id": "Q1_Acute" },
{ "text": "Chronic", "next_node_id": "Q2_Chronic" }
]
},
"Q1_Acute": {
"text": "For acute dyspnea, is the onset sudden or gradual?",
"type": "question",
"choices": [
{ "text": "Sudden onset", "next_node_id": "A1_SuddenOnsetTests" },
{ "text": "Gradual onset", "next_node_id": "A1_GradualOnsetTests" }
]
},
"A1_SuddenOnsetTests": {
"text": "Obtain ABG, SaO2, CXR, ECG/cardiac enzymes, D-dimer/spiral CT, CBC, BMP.",
"type": "action",
"next_node_id": "D1_SuddenOnsetDiagnoses"
},
"D1_SuddenOnsetDiagnoses": {
"text": "Potential diagnoses for sudden onset acute dyspnea: Pulmonary embolism, Pneumothorax/cardiac tamponade, Foreign body aspiration.",
"type": "diagnosis",
"next_node_id": null
},
"A1_GradualOnsetTests": {
"text": "Obtain ABG, SaO2, ECG/cardiac enzymes, D-dimer/spiral CT, BNP, pH monitoring, CXR, CBC, BMP.",
"type": "action",
"next_node_id": "D1_GradualOnsetDiagnoses"
},
"D1_GradualOnsetDiagnoses": {
"text": "Potential diagnoses for gradual onset acute dyspnea: ARDS, Respiratory failure, MI, GERD, Pneumonia/lung infections.",
"type": "diagnosis",
"next_node_id": null
},
"Q2_Chronic": {
"text": "For chronic dyspnea, obtain CBC, BMP, and TSH. Are the lab results normal or abnormal?",
"type": "question",
"choices": [
{ "text": "Normal", "next_node_id": "Q2_OnExertion" },
{ "text": "Abnormal", "next_node_id": "A2_AddressAbnormalLabs" }
]
},
"A2_AddressAbnormalLabs": {
"text": "Address abnormal labs.",
"type": "action",
"next_node_id": null
},
"Q2_OnExertion": {
"text": "Is the dyspnea on exertion?",
"type": "question",
"choices": [
{ "text": "Yes", "next_node_id": "Q2_HgbSaO2" },
{ "text": "No", "next_node_id": "Q2_AnxietySymptoms" }
]
},
"Q2_AnxietySymptoms": {
"text": "Does the patient present with anxiety symptoms?",
"type": "question",
"choices": [
{ "text": "Yes", "next_node_id": "D2_PanicAttack" },
{ "text": "No", "next_node_id": "Q2_WeightGainExerciseWeakness" }
]
},
"D2_PanicAttack": {
"text": "Diagnosis: Panic attack.",
"type": "diagnosis",
"next_node_id": null
},
"Q2_WeightGainExerciseWeakness": {
"text": "Are there symptoms like recent weight gain, discontinuation of exercise, or muscular weakness?",
"type": "question",
"choices": [
{ "text": "Yes", "next_node_id": "D2_DeconditioningAsthmaNeuromuscular" },
{ "text": "No", "next_node_id": null }
]
},
"D2_DeconditioningAsthmaNeuromuscular": {
"text": "Diagnosis: Deconditioning, Asthma, Neuromuscular disorder.",
"type": "diagnosis",
"next_node_id": null
},
"Q2_HgbSaO2": {
"text": "For dyspnea on exertion, what are the Hgb/Hct and SaO2 levels?",
"type": "question",
"choices": [
{ "text": "Decreased Hgb/Hct", "next_node_id": "D2_Anemia" },
{ "text": "Decreased SaO2", "next_node_id": "Q2_BNP" }
]
},
"D2_Anemia": {
"text": "Diagnosis: Anemia.",
"type": "diagnosis",
"next_node_id": null
},
"Q2_BNP": {
"text": "Given Cardiopulmonary symptoms (e.g., decreased SaO2), what is the BNP level?",
"type": "question",
"choices": [
{ "text": "> 100 pg/mL", "next_node_id": "A2_EchocardiogramCXR" },
{ "text": "< 100 pg/mL", "next_node_id": "A2_SpirometryECGCXREchocardiogram" }
]
},
"A2_EchocardiogramCXR": {
"text": "Obtain Echocardiogram and CXR.",
"type": "action",
"next_node_id": "D2_CHFPulmonaryEdema"
},
"D2_CHFPulmonaryEdema": {
"text": "Diagnosis: CHF, Pulmonary edema.",
"type": "diagnosis",
"next_node_id": null
},
"A2_SpirometryECGCXREchocardiogram": {
"text": "Obtain Spirometry, ECG, CXR, Echocardiogram.",
"type": "action",
"next_node_id": "D2_COPDChronic"
},
"D2_COPDChronic": {
"text": "Diagnosis: COPD, Asthma, Arrhythmia, Sarcoidosis, Cardiomyopathy.",
"type": "diagnosis",
"next_node_id": null
}
}
"""
expert_conversation_history = ""
student_input = """
Based on the patient’s description of irregular heart rhythm and palpitations, I would like to assess for any potential arrhythmias. I will ask more about the frequency and triggers of her episodes, any history of similar events, family history of cardiac disease, and if she’s on any medications. I also want to know if caffeine or other stimulants are involved.

I plan to check her vital signs, perform an ECG to assess rhythm, and consider labs like TSH to rule out hyperthyroidism. I’ll also assess anxiety levels, as she seems distressed.
"""
patient_info = """
Current Patient Information:
- Name: Abigail Park
- Age: 60
- Chief Complaint: Heart palpitations
- Clinical Setting:
<p><strong>Your Role:</strong> You are rotating through your Primary Care clerkship.</p>
<p><strong>Task:</strong> You have been asked to evaluate this patient.</p>
<p><strong>Procedure:</strong></p>
<ol>
<li>Enter the chatbot room</li>
<li>Use the chat to communicate with the patient</li>
<li>You have up to 30 minutes to obtain the following:
<ul>
<li>Chief Concern</li>
<li>History of the present illness</li>
<li>Past medical history</li>
<li>Past surgical history</li>
<li>Medications/supplements</li>
<li>Allergies</li>
<li>Measure the patient's heart rate, respiratory rate, and blood pressure</li>
</ul></li>
</ol>
<p><strong>Note:</strong> There will be no physical exam for this evaluation.</p>
<p><strong>Important Reminders:</strong></p>
<ul>
<li>Recognize that we all have biases in medical decision-making</li>
<li>Take a moment to consider your own perspectives and positionality</li>
<li>Apply screening questions to <em>all</em> patients, regardless of preconceptions</li>
<li>When details are unclear, clarify with the patient rather than making assumptions</li>
</ul>
<p><em>Remember: Our ability to increase the consciousness of our medical decision-making begins with recognizing our own biases.</em></p>
"""
student_record_performance = """
**Overall Performance Summary:**\nYou have an outstanding natural ability to connect with patients, demonstrate empathy, and make them feel heard. This is a critical skill. To advance, the next step is to channel that skill into a more systematic and efficient clinical framework to ensure safety and completeness under timed conditions.\n\n**Key Strengths:**\n*   **Rapport and Empathy:** Consistently received top marks for empathy from simulated patients. You validated patient concerns effectively.\n*   **Clear Explanations:** Your explanations of conditions and treatments were clear, jargon-free, and you always checked for understanding.\n*   **Active Listening:** You demonstrated excellent active listening skills, allowing the patient to fully express their story without interruption.\n\n**Areas for Development:**\n*   **Systematic History Taking:** Your history-taking approach was sometimes disorganized, causing you to miss key information (e.g., a full drug history, including over-the-counter medications). **To improve:** Use a structured mnemonic like SOCRATES or a consistent template (PC -> HPC -> PMH -> etc.) for every history.\n*   **Time Management:** You spent a significant portion of time building rapport, which sometimes left insufficient time for discussing management and safety netting. **To improve:** Practice with the station timer activated and aim to complete history-taking within the first 4-5 minutes.\n*   **Quantifying Symptoms:** You identified symptoms well but often missed opportunities to quantify them (e.g., You didn't ask about exercise tolerance in terms of stairs or distance when the patient had shortness of breath). **To improve:** Always seek specific numbers, frequencies, or functional impacts to better assess severity."""
reasoning_json_schema = """
caseProgress = {
"correctDiagnosis": str,
"correctRecommendations": list[str],
"studentStrengths": list[str],
"studentWeaknesses": list[str],
"studentProgress": str,
"unqueried_patient_details": str
}"""