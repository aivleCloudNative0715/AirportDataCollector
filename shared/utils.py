def get_text(elem, default=""):
    return elem.text.strip() if elem is not None and elem.text else default