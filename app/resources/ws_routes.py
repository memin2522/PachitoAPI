import json
import threading
from . import sock

_subscribers = set()
_lock = threading.Lock()
_last_answer = None

def register_ws_routes(app):
    @sock.route("/ws/answer")
    def ws_answer(ws):
        # registrar
        with _lock:
            _subscribers.add(ws)
            last = _last_answer

        # si quieres “replay” de la última respuesta al conectar
        if last is not None:
            try:
                ws.send(json.dumps({"type":"answer","answer": last}))
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