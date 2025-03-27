import typer
import yaml
from engine.renderer import render_template
from engine.validator import validate_policy
from engine.audit import push_audit
from supabase_client.templates import list_templates, pull_template

app = typer.Typer()

@app.command()
def generate(template: str, params: list[str]):
    param_dict = dict(p.split("=") for p in params)
    rendered = render_template(template, param_dict)
    print(rendered)
    push_audit("generate", {"template": template, "params": param_dict}, {"policy": rendered})

@app.command()
def validate(file: str):
    try:
        policy = validate_policy(file)
        print("✅ Policy is valid:", policy)
        push_audit("validate", {"file": file}, {"valid": True})
    except Exception as e:
        print("❌ Invalid policy:", str(e))
        push_audit("validate", {"file": file}, {"valid": False, "error": str(e)})

@app.command()
def push(file: str):
    with open(file, "r") as f:
        content = yaml.safe_load(f)
    push_audit("push", {"file": file}, {"content": content})
    print("✅ Policy pushed to Supabase")

@app.command()
def templates(cmd: str = typer.Argument(...)):
    if cmd == "list":
        templates = list_templates()
        for t in templates:
            print(f"{t['id']} - {t['name']}")
    elif cmd == "pull":
        template_id = typer.prompt("Template ID")
        tpl = pull_template(template_id)
        print("📄 Template:", tpl["template"])
