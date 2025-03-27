from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader=FileSystemLoader("templates"))

def render_template(name: str, params: dict) -> str:
    template = env.get_template(f"{name}.j2")
    return template.render(**params)
