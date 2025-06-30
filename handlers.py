from livekit.agents import function_tool, get_job_context, RunContext
from constants import DOCTOR_SCHEDULE, REQUIRED_FIELDS
from livekit import api

# Patient info reference should be passed from main module
def set_patient_field(field: str, patient_info: dict):
    @function_tool(name=f"set_{field.replace(' ', '_')}", description="Sets a field in the patient information dictionary. Triggered by the LLM when it recognizes a field that needs to be set from the user's input in response to a question.")
    async def tool(context: RunContext, value: str):
        patient_info[field] = value
        print("[DEBUG]" + f"{field.title()} DETECTED! Value: {value}")
        return f"{field.title()} recorded."
    return tool

def get_available_doctors():
    @function_tool(name="get_available_doctors", description="Returns a list of available doctors.")
    async def tool(context: RunContext):
        return {"available_doctors": list(DOCTOR_SCHEDULE.keys())}
    return tool

def get_available_times():
    @function_tool(name="get_available_times", description="Returns available appointment times for a doctor.")
    async def tool(context: RunContext, doctor: str):
        return {"available_times": DOCTOR_SCHEDULE.get(doctor, [])}
    return tool

def final_review(patient_info: dict):
    @function_tool(name="final_review", description="Final review of the appointment details. Called near the end of the call to confirm all details have been collected. Returns a list of any missing required fields.")
    async def tool(context: RunContext):
        missing = [f for f in REQUIRED_FIELDS if not patient_info.get(f)]
        if not patient_info.get("email"):
            patient_info["email"] = "no email"
        return {"missing_fields": missing}
    return tool

async def hangup_call():
    ctx = get_job_context()
    if ctx is None:
        return
    await ctx.api.room.delete_room(api.DeleteRoomRequest(room=ctx.room.name))
