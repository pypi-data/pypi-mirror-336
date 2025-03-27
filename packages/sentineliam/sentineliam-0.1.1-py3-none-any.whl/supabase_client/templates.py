from .client import supabase

def list_templates():
    return supabase.table("policy_templates").select("*").execute().data

def pull_template(template_id: str):
    return supabase.table("policy_templates").select("*").eq("id", template_id).single().execute().data
