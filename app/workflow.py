import os
import json
import re
import time
import logging
from app.database import SessionLocal
from app.models import AnalyzedAlert, RawAlert
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import re

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
    #cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    cleaned = response.content
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
    #cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    cleaned = response.content
    return cleaned

def analyze_steps(llm, prompt):
    response = llm.invoke(prompt)
    #cleaned = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()
    cleaned = response.content
    return cleaned

def add_final_output(alert_id, ai_output):
    
    try:
        ai_output = json.loads(ai_output)
    except json.JSONDecodeError as e:
        print("Error parsing LLM response as JSON:", e)
        print("LLM response was:", ai_output)
        return
    db = SessionLocal()
    existing = db.query(AnalyzedAlert).filter_by(alert_id=alert_id).first()
    if existing:
        print(f"AnalyzedAlert for alert_id {alert_id} already exists. Skipping insert.")
        db.close()
        return
    
    db_alert = AnalyzedAlert(
    alert_id=alert_id,
    isolation=ai_output["isolation"],
    true_positive=ai_output["true_positive"],
    attack_type=ai_output["attack_type"],
    severity=ai_output["severity"],
    recommendations=ai_output["recommendations"],
    reasoning=ai_output["reasoning"],
    artifacts_and_iocs=ai_output["artifacts_and_iocs"],
    summary=ai_output["summary"]
    )
    
    
    db.add(db_alert)
    db.commit()
    db.close()
    print(f"Inserted analyzed alert for alert_id {alert_id}")
#------------------------------------------------------------------------------------------------------  

def main(alert_id):
    start = time.time()
    # ollama_base_url = "http://host.docker.internal:11434"

    # llm = Ollama(
    #     model="deepseek-r1:8b",      
    #     base_url=ollama_base_url,      
    # )
    
    llm = ChatOpenAI(  
        model="gpt-4.1",  
        api_key=os.environ["OPENAI_API_KEY"]  
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

    playbook_choice = choose_playbook(llm, alert_details, playbook_index)
    
    print(playbook_choice)
    print("\n\n")

    if playbook_choice not in playbook:
        logging.error(f"Unexpected playbook response: {playbook_choice}")
        return
    steps = playbook[playbook_choice]['steps']
#------------------------------------------------------------------------------------------------------  
    recommended_tools = choose_tools(llm, alert_details, steps, tool_index)
    print(recommended_tools)
    recommended_tools = [tool.strip().lower() for tool in recommended_tools.split(" ")]
    
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
        elif tool == "virustotal_ip" and alert_obj.source_ip:
            enrichment = get_enrichment(
                alert_obj.id, "virustotal_ip", "ip", alert_obj.source_ip
            )
            if enrichment:
                print("Using existing VirusTotal_IP enrichment.")
                enrichments_for_prompt.append(enrichment)
            else:
                print(f"Enriching IP {alert_obj.source_ip} with VirusTotal_IP...")
                enrich_alert_ip_virustotal(alert_obj.id, alert_obj.source_ip)
                enrichment = get_enrichment(
                    alert_obj.id, "virustotal_ip", "ip", alert_obj.source_ip
                )
                if enrichment:
                    enrichments_for_prompt.append(enrichment)

        elif tool == "virustotal_url":
            urls = re.findall(r'(https?://\S+)', alert_obj.trigger_reason or "")
            if urls:
                url_value = urls[0]
                enrichment = get_enrichment(
                    alert_obj.id, "virustotal_url", "url", url_value
                )
                if enrichment:
                    print("Using existing VirusTotal_URL enrichment.")
                    enrichments_for_prompt.append(enrichment)
                else:
                    print(f"Enriching URL {url_value} with VirusTotal_URL...")
                    enrich_alert_url_virustotal(alert_obj.id, url_value)
                    enrichment = get_enrichment(
                        alert_obj.id, "virustotal_url", "url", url_value
                    )
                    if enrichment:
                        enrichments_for_prompt.append(enrichment)
            else:
                print("No URL found in alert for VirusTotal_URL enrichment.")
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
    
    #make it extract from logs
    
    system_format_prompt = """
    You are an expert AI SOC analyst. Respond ONLY using this JSON format, with brief, relevant information for each key:

    {
    "isolation": "yes" or "no",       // Should the device be isolated? 
    "true_positive": true or false,   // Is this a true positive or false positive alert?
    "attack_type": "<MITRE technique or name>", // E.g., "T1110 (Brute Force)", or "T1059 (Command and Scripting Interpreter)"
    "severity": "Low" | "Medium" | "High", // Assess severity based on all evidence, not just the alert's original value. If your investigation suggests it is higher or lower than the alert's severity, change it and explain why in reasoning.
    "recommendations": "...",         // Short, clear mitigation/remediation steps
    "reasoning": "...",               // Why did you classify this as you did? Be concise but clear.
    "artifacts_and_iocs": [           // List any found artifacts or indicators of compromise
        "<ioc1>", "<ioc2>", ...
    ]
    "summary": "Summarize the entire investigation here. Step by step, briefly explain what was found in each stage (alert, enrichment, investigation, analysis, decision), so a human SOC analyst understands what happened and how you reached your result. This should help with auditing or deeper review."
    }

    IMPORTANT: The 'severity' field is for your own, independent assessment. Do NOT simply copy the alert's severity value—adjust it as needed based on your findings.
    Only respond with valid JSON in this structure. Do not write any explanations outside the JSON.
    """
    
    human_prompt = f"""
    Here is the alert to analyze:

    {alert_details}

    Enrichment data:
    {enrichment_text}

    Relevant playbook steps:
    {steps_text}

    Please fill in the JSON above based on the alert, enrichment data, and steps. Use "no" or empty array if nothing applies to a field.
    """
    
    final_prompt = [
        SystemMessage(content=system_format_prompt),
        HumanMessage(content=human_prompt)
    ]

    final_response = analyze_steps(llm, final_prompt)
    print(final_response)
    add_final_output(alert_id, final_response)
    
    end = time.time()
    print("Response Took: ", end-start, " sec")

if __name__ == "__main__":
     main(alert_id=1)
