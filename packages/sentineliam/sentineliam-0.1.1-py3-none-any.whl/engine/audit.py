import json
import os
from supabase_client.client import supabase

QUEUE_FILE = ".sentinel/logs/queue.json"

def push_audit(action, input_data, result, user_id=None):
    try:
        supabase.table("audit_logs").insert({
            "action": action,
            "input": input_data,
            "result": result,
            "user_id": user_id
        }).execute()
    except Exception:
        os.makedirs(".sentinel/logs", exist_ok=True)
        with open(QUEUE_FILE, "a") as f:
            f.write(json.dumps({
                "action": action,
                "input": input_data,
                "result": result,
                "user_id": user_id
            }) + "\n")

def flush_log_queue():
    if not os.path.exists(QUEUE_FILE):
        return
    with open(QUEUE_FILE) as f:
        for line in f:
            entry = json.loads(line)
            supabase.table("audit_logs").insert(entry).execute()
    os.remove(QUEUE_FILE)
