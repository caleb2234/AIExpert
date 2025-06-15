patient_conversation_history = """
user: Hi Abigail, what brings you in today?
patient: I've been having this irregular heartbeat that's making me really anxious. It's been affecting my work, and I'm quite worried about it.

user: Have you noticed when these episodes usually happen?
patient: They seem to happen at random, but I've noticed they sometimes occur after I've had a few cups of tea. Yesterday, it happened at work and lasted for about an hour, which was unusual.

user: Do you feel any pain, shortness of breath, or dizziness during these episodes?
patient: I don't feel any pain or shortness of breath. But I do feel weak and a bit faint during the episodes. It's really unsettling.
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