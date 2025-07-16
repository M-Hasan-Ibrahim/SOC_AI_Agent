import os
import json
import re
import time
import logging
from app.database import SessionLocal
from app.models import RawAlert
from langchain_community.llms import Ollama

from app.enrichment import enrich_alert_ip_abuseipdb, enrich_alert_ip_virustotal, enrich_alert_ip_ipinfo
from app.enrichment_methods import get_enrichment, format_enrichment, format_multiple_enrichments

logging.basicConfig(level=logging.INFO)

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

def get_alert_from_db(alert_id):
    db = SessionLocal()
    alert = db.query(RawAlert).filter(RawAlert.id == alert_id).first()
    db.close()
    return alert

def choose_playbook(llm, alert_details, playbook_index):
    prompt = playbook_index + "\n\n" + alert_details
    response = llm.invoke(prompt)
    cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    return cleaned

def choose_tools(llm, alert_details, steps, tool_index):
    steps_text = json.dumps(steps, indent=2)

    prompt = (
        f"Alert details:\n{alert_details}\n\n"
        f"Relevant playbook steps (as JSON):\n{steps_text}\n"
        f"{tool_index}\n"
        "Which enrichment tools (APIs) should be used for this alert? Respond ONLY with the tool name(s) from the list above, or 'None'."
    )
    response = llm.invoke(prompt)
    cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    return cleaned

def analyze_steps(llm, prompt):
    response = llm.invoke(prompt)
    cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    return cleaned




def main(alert_id):
    start = time.time()
    ollama_base_url = "http://host.docker.internal:11434"

    llm = Ollama(
        model="deepseek-r1:8b",      
        base_url=ollama_base_url,      
    )

    with open("app/playbook.json", "r") as file:
        playbook = json.load(file)

    playbook_index_path = "app/indexes/playbook_index.txt"
    with open(playbook_index_path, 'r', encoding='utf-8') as f:
        playbook_index = f.read()
    
    
    tool_index_path = "app/indexes/tool_index.txt"
    with open(tool_index_path, 'r', encoding='utf-8') as f:
        tool_index = f.read()

    alert_obj = get_alert_from_db(alert_id)
    if not alert_obj:
        logging.error(f"No alert found with id {alert_id}")
        return
    alert_details = format_alert(alert_obj)

    cleaned_response = choose_playbook(llm, alert_details, playbook_index)
    
    print(cleaned_response)
    print("\n\n")

    if cleaned_response not in playbook:
        logging.error(f"Unexpected playbook response: {cleaned_response}")
        return
    steps = playbook[cleaned_response]['steps']
#------------------------------------------------------------------------------------------------------  
    recommended_tools = choose_tools(llm, alert_details, steps, tool_index)
    print(recommended_tools)
    recommended_tools = [tool.strip().lower() for tool in recommended_tools.split(",")]
    
    # if "abuseipdb" in recommended_tools and alert_obj.source_ip:
    #     print(f"Enriching IP {alert_obj.source_ip} with AbuseIPDB...")
    #     enrich_alert_ip_abuseipdb(alert_obj.id, alert_obj.source_ip)
    # else:
    #     print("No recommended tools from the AI")


    enrichments_for_prompt = []

    for tool in recommended_tools:
        if tool == "none":
            continue
        if tool == "abuseipdb" and alert_obj.source_ip:
            enrichment = get_enrichment(
                alert_obj.id, "abuseipdb", "ip", alert_obj.source_ip
            )
            if enrichment:
                print("Using existing AbuseIPDB enrichment.")
                enrichments_for_prompt.append(enrichment)
            else:
                print(f"Enriching IP {alert_obj.source_ip} with AbuseIPDB...")
                enrich_alert_ip_abuseipdb(alert_obj.id, alert_obj.source_ip)
                enrichment = get_enrichment(
                    alert_obj.id, "abuseipdb", "ip", alert_obj.source_ip
                )
                if enrichment:
                    enrichments_for_prompt.append(enrichment)
        elif tool == "virustotal" and alert_obj.source_ip:
            enrichment = get_enrichment(
                alert_obj.id, "virustotal", "ip", alert_obj.source_ip
            )
            if enrichment:
                print("Using existing VirusTotal enrichment.")
                enrichments_for_prompt.append(enrichment)
            else:
                print(f"Enriching IP {alert_obj.source_ip} with VirusTotal...")
                enrich_alert_ip_virustotal(alert_obj.id, alert_obj.source_ip)
                enrichment = get_enrichment(
                    alert_obj.id, "virustotal", "ip", alert_obj.source_ip
                )
                if enrichment:
                    enrichments_for_prompt.append(enrichment)
        elif tool == "ipinfo.io" and alert_obj.source_ip:
            enrichment = get_enrichment(
                alert_obj.id, "ipinfo.io", "ip", alert_obj.source_ip
            )
            if enrichment:
                print("Using existing ipinfo.io enrichment.")
                enrichments_for_prompt.append(enrichment)
            else:
                print(f"Enriching IP {alert_obj.source_ip} with ipinfo.io...")
                enrich_alert_ip_ipinfo(alert_obj.id, alert_obj.source_ip)
                enrichment = get_enrichment(
                    alert_obj.id, "ipinfo.io", "ip", alert_obj.source_ip
                )
                if enrichment:
                    enrichments_for_prompt.append(enrichment)
        else:
            print(f"No enrichment handler for tool: {tool}")

#------------------------------------------------------------------------------------------------------
    #build final prompt
    steps_text = ""
    for step in steps:
        steps_text += f"Step {step['step_number']}: {step['name']}\n"
        steps_text += f"Instruction: {step['instructions']}\n\n"
    
    enrichment_text = format_multiple_enrichments(enrichments_for_prompt)
   
    final_prompt = (
    f"Alert details:\n{alert_details}\n\n"
    f"Enrichment data:\n{enrichment_text}\n\n"
    f"Given the following steps for handling this alert:\n\n"
    f"{steps_text}"
    "For each step instruction, give a very brief response based ONLY on the alert details and enrichment above. Recommend remediation at the end. "
    "If you cannot respond to an instruction, say so."
    )
   
    final_cleaned_response = analyze_steps(llm, final_prompt)
    print(final_cleaned_response)
   
   
    
    # file_path = f"app/deepseekResponse.txt"
    # with open(file_path, "a", encoding="utf-8") as f:
    #     f.write(f"Response to alert:\n {alert_details}")
    #     f.write("\n\n")
    #     f.write(cleaned_response_to_steps.strip())
    #     f.write("\n--------------------------------------------------------------------------------\n")
    
    end = time.time()
    print("Response Took: ", end-start, " sec")

if __name__ == "__main__":
     main(alert_id=6)
