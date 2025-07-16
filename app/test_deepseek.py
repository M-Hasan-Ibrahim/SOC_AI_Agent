from langchain_community.llms import Ollama
import re
import time
import json
from app.database import SessionLocal
from app.models import RawAlert

def format_alert(alert):
    return (
        f"timestamp: {alert.timestamp}\n"
        f"source_ip: {alert.source_ip}\n"
        f"destination_ip: {alert.destination_ip}\n"
        f"source_port: {alert.source_port}\n"
        f"destination_port: {alert.destination_port}\n"
        f"source_hostname: {alert.source_hostname}\n"
        f"destination_hostname: {alert.destination_hostname}\n"
        f"alert_type: {alert.alert_type}\n"
        f"severity: {alert.severity}\n"
        f"rules_triggered: {alert.rules_triggered}\n"
        f"trigger_reason: {alert.trigger_reason}"
    )

start = time.time()

ollama_base_url = "http://host.docker.internal:11434"

llm = Ollama(
    model="deepseek-r1:8b",      
    base_url=ollama_base_url,      
)

playbook_path = "app/playbook.json"
with open(playbook_path, "r") as file:
    playbook = json.load(file)

playbook_index = """
Available playbooks:

1. Brute Force — For repeated failed login attempts or authentication attacks on user accounts.
2. Phishing — For suspicious or malicious emails that try to trick users into clicking links, opening attachments, or giving up credentials.
3. Malware — For detections of known malicious files, software, or unusual file hashes.
4. Lateral Movement — For cases where an attacker moves from one system to another within the network, often using remote desktop or SMB shares.

Instructions:
Based on the alert details I will give you, choose the one playbook that best matches the alert. If you want Brute Force, respond ONLY with: Brute Force. If you want Phishing, respond ONLY with: Phishing. Do the same for the other options.
"""

alert_id = 1
db = SessionLocal()
alert_obj = db.query(RawAlert).filter(RawAlert.id == alert_id).first()
db.close()

if alert_obj:
    alert_details = format_alert(alert_obj)
else:
    raise ValueError(f"No alert found with id {alert_id}")

full_prompt = playbook_index + "\n\n" + alert_details



response = llm.invoke(full_prompt)


cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

print(cleaned_response)
print("\n\n")
# for step in playbook[cleaned_response]['steps']:
#     print(f"Step Number: {step['step_number']}, Name: {step['name']}")

steps = playbook[cleaned_response]['steps']

steps_text = ""
for step in steps:
    steps_text += f"Step {step['step_number']}: {step['name']}\n"
    steps_text += f"Instruction: {step['instructions']}\n\n"

# Compose the prompt
prompt = (
    f"Alert details:\n{alert_details}\n\n"
    f"Given the following steps for handling this alert:\n\n"
    f"{steps_text}"
    "For each step instruction, give a very brief response based ONLY on the alert details above and don't forget to recommend a remediation.\n"
    "If you don't have a response for an instruction just write the step number and its name then write something about that you can't respond to this.\n"
)

response_to_steps = llm.invoke(prompt)
cleaned_response_to_steps = re.sub(r"<think>.*?</think>", "", response_to_steps, flags=re.DOTALL).strip()
print(cleaned_response_to_steps)
file_path  = "app/deepseekResponse.txt"
with open(file_path, "a", encoding="utf-8") as f:
    f.write(f"Response to alert:\n {alert_details}")
    f.write("\n\n")
    f.write(cleaned_response_to_steps.strip())
    f.write("\n--------------------------------------------------------------------------------\n")

end = time.time()
print("Response Took: ", end-start, " sec")