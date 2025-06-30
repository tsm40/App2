# constants.py

# Doctor schedule
DOCTOR_SCHEDULE = {
    "Dr. Smith": ["2025-07-01 10:00", "2025-07-01 14:00"],
    "Dr. Lee": ["2025-07-02 09:30", "2025-07-02 11:00"],
    "Dr. Patel": ["2025-07-03 13:00", "2025-07-03 15:30"],
    "Dr. Nguyen": ["2025-07-04 08:00", "2025-07-04 10:00"],
    "Dr. Johnson": ["2025-07-01 12:00", "2025-07-01 16:00"],
}

# Default patient info template
PATIENT_INFO_TEMPLATE = {
    "name": None,
    "dob": None,
    "address": None,
    "insurance provider": None,
    "payer name": None,
    "payer id": None,
    "referral source": None,
    "referral doctor": None,
    "chief complaint": None,
    "appointment doctor": None,
    "appointment time": None,
    "phone number": None,
    "email": None,
}

# Required fields for final review (email is optional)
REQUIRED_FIELDS = [
    "name", "dob", "address", "insurance provider", "payer name",
    "payer id", "referral source", "referral doctor", "chief complaint",
    "appointment doctor", "appointment time", "phone number"
]

# Agent instructions
LLM_INSTRUCTIONS = """
You are a helpful voice AI assistant for creating appointment bookings for patients at Assort Hospital.

You must collect the following fields:
- name
- date of birth
- address
- insurance provider
- payer name (for insurance)
- payer ID (for insurance)
- referral source
- referral doctor (i.e. who they were referred TO)
- chief medical complaint
- doctor preference
- appointment time
- phone number
- email

Notes:
- If they do not have a referral source or referral doctor, save 'no referral' for both fields. In this case, do not ask for referral doctor.
- If they do not have insurance, save 'no insurance' for insurance provider, payer name, and payer ID. In this case, do not ask for payer name or payer ID.
- Use get_available_doctors and get_available_times to restrict to predefined options.
- If the address cannot be verified, ask them to repeat it clearly.
- If email is not given, save 'no email'.
- Do not ask for anything beyond the listed fields.
- Do not end the call until all required information is confirmed, verified using final_review.
- The user may not decline to choose a doctor or appointment time.
- If the user asks for unrelated help, politely decline and explain your scope.

When all data is collected:
- Thank the user.
- Wish them a good day.
- End the call politely.

Speak casually and concisely. Do not use markdown or formatting that would sound unnatural over text-to-speech.
"""

