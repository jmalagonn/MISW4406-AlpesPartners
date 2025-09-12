import httpx
from contextlib import contextmanager

def make_client(timeout_seconds: float):
    return httpx.Client(timeout=timeout_seconds)

def forward_headers(incoming_headers, request_id_header="X-Request-Id"):
    out = {}
    req_id = incoming_headers.get(request_id_header)
    
    if not req_id:
        import uuid
        req_id = str(uuid.uuid4())
        
    out[request_id_header] = req_id
    return out, req_id
