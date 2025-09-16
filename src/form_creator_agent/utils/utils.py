import re

def extract_form(code):
    match = re.search(r"(<form[\s\S]*?</form>)", code)
    if match:
        return match.group(1)
    else:
        return ""
    


def extract_css(code):
    match = re.search(r"<style[^>]*>([\s\S]*?)</style>", code, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    else:
        return ""
