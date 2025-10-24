import json
import threading
from . import sock

from app.schemas import WSAnswerSchema

_subscribers = set()
_lock = threading.Lock()
_last_answer = None

def register_ws_routes(app):
    @sock.route("/ws/answer")
    def ws_answer(ws):
        with _lock:
            _subscribers.add(ws)
            last = _last_answer

        if last is not None:
            try:
                payload_text = WSAnswerSchema.dumps({"answer": last})
                ws.send(payload_text)
            except Exception:
                pass

        try:
            # escuchar mensajes del cliente (opcional)
            while True:
                msg = ws.receive()   # bloquea; None si se cerró
                if msg is None:
                    break
                # aquí podrías manejar acks, cancelaciones, etc.
        finally:
            with _lock:
                _subscribers.discard(ws)

def broadcast_answer(answer: str):
    global _last_answer
    payload = json.dumps({"type":"answer","answer": answer})
    dead = []
    with _lock:
        _last_answer = answer
        for ws in list(_subscribers):
            try:
                ws.send(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            _subscribers.discard(ws)