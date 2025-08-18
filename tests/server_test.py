from server import sanitize_path, find_mime

def test_safe_path():
    requested_uri = "/index.html"
    safe_path = sanitize_path(requested_uri)
    assert safe_path != None

def test_unsafe_path():
    requested_uri = "/../main.py"
    unsafe_path = sanitize_path(requested_uri)
    assert unsafe_path == None

def test_mime_types():
    exts = [".html", ".js", ".txt"]
    mime_types = list(map(find_mime, exts))
    assert mime_types == ["text/html", "application/javascript", "text/plain"]