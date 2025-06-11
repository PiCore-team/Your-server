import socket
import numpy as np

class Api:
    def __init__(self, host, port=5000):
        self.host = host
        self.port = port

    def send_application(self, expression, variables=None):
        # Отправка арифметического выражения (команда eval)
        if variables:
            for k, v in variables.items():
                expression = expression.replace(f"{{{k}}}", str(v))
        return self._parse_eval_response(self._send(f"eval {expression}"))

    def echo(self, message):
        return self._send(f"echo {message}")

    def sysinfo(self):
        return self._send("sysinfo")

    def dot(self, inp, w):
        # inp и w — numpy-массивы или списки
        inp_str = str(inp.tolist()) if hasattr(inp, 'tolist') else str(inp)
        w_str = str(w.tolist()) if hasattr(w, 'tolist') else str(w)
        response = self._send(f"dot {inp_str}|{w_str}")
        if response.startswith("RESULT:"):
            res = eval(response[7:])
            return np.array(res)
        return response

    def get_error(self, pred, true):
        # pred и true — numpy-массивы или списки
        pred_str = str(pred.tolist()) if hasattr(pred, 'tolist') else str(pred)
        true_str = str(true.tolist()) if hasattr(true, 'tolist') else str(true)
        response = self._send(f"get_error {pred_str}|{true_str}")
        if response.startswith("RESULT:"):
            return float(response[7:])
        return response

    def custom(self, cmd, args=""):
        # Для любых других команд
        return self._send(f"{cmd} {args}")

    def _send(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(data.encode())
            return s.recv(4096).decode()

    def _parse_eval_response(self, response):
        if response.startswith("RESULT:"):
            try:
                return eval(response[7:])
            except Exception:
                return response[7:]
        return response

