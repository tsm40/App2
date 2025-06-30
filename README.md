# 🗣️ Voice AI Appointment Assistant

A real-time voice assistant built with LiveKit, OpenAI, Deepgram, Cartesia, and Twilio. This AI agent collects patient information, schedules appointments, and emails a summary to admins after the call.

Call the live agent at **+14243702125!**

## Features

- Natural language voice conversation with patients via phone.
- Collects structured information (name, DOB, insurance, etc.).
- Uses function calling to store fields with real-time validation.
- Suggests available doctors and appointment times.
- Sends a formatted email summary to admins upon call completion.

---

## Architecture

---

## Tech Stack

- 🧠 LLM: OpenAI GPT-4o-mini  
- 🗣️ TTS: Cartesia Sonic-2  
- 📝 STT: Deepgram Nova-3  
- 📞 Voice infra: Twilio + LiveKit  
- 🦻 VAD: Silero + Turn Detection  
- 📧 Email: Gmail SMTP  
- 🐍 Python 3.10+

---

## Project Structure

| File           | Description                                                  |
|----------------|--------------------------------------------------------------|
| `agent.py`     | Main entrypoint; defines the assistant and session logic     |
| `constants.py` | Doctor schedule, patient info template, and LLM instructions |
| `handlers.py`  | Function tools to collect data and schedule appointments     |
| `emailing.py`  | Formats and sends structured email summaries                 |

---

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set environment variables

Create a `.env` file with the following content:

```env
DEEPGRAM_API_KEY=deepgram_api_key
OPENAI_API_KEY=openai_api_key
CARTESIA_API_KEY=cartesia_api_key
LIVEKIT_URL=livekit_url
LIVEKIT_API_KEY=livekit_api_key
LIVEKIT_API_SECRET=livekit_api_secret
EMAIL_SENDER=youremail@example.com
EMAIL_RECIPIENT=admin@example.com
EMAIL_PASSWORD=your-email-password
```

> 💡 Use an app password for Gmail if 2FA is enabled.

### 3. Run the assistant

```bash
python agent.py start
```

This launches the assistant, which joins a LiveKit room and begins listening for user calls.

---

## 📧 Example Email Output

```
=== Patient Information ===
Name                : Jane Doe
DOB                 : 1990-01-01
Phone Number        : 123-456-7890
Email               : jane@example.com
Address             : 123 Main St, Atlanta, GA

=== Insurance Information ===
Insurance Provider  : Blue Cross
Payer Name          : Anthem
Payer ID            : 123456

=== Referral Information ===
Referral Source     : Primary Care
Referral Doctor     : Dr. Adams

=== Appointment Details ===
Chief Complaint     : Headache
Appointment Doctor  : Dr. Lee
Appointment Time    : 2025-07-02 09:30
```

---

## Security Notes

* Do **not** commit `.env` files.
* Use Gmail app passwords if using `smtp.gmail.com`.
* For production: use encrypted storage, access control, and HIPAA-compliant infrastructure.

---

## Future Enhancements

* Google Calendar sync for dynamic doctor schedules
* RAG-based memory of prior patients
* Analytics dashboard for admins

---

## 📝 License

MIT License

