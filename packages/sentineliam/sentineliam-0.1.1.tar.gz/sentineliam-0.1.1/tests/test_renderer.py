from engine.renderer import render_template

def test_render_template():
    result = render_template("test_template", {"user_id": "123"})
    assert "123" in result
