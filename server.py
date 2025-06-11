import socket
import threading
import sys
import traceback
import numpy as np

# --- Система команд ---

def cmd_eval(args):
    """Вычисляет выражение Python (только арифметика)."""
    try:
        allowed_names = {"builtins": None}
        result = eval(args, allowed_names, {})
        return f"RESULT: {result}"
    except Exception as e:
        return f"ERROR: {e}"

def cmd_echo(args):
    """Возвращает то, что прислал клиент."""
    return f"ECHO: {args}"

def cmd_sysinfo(_):
    """Информация о системе."""
    import platform
    return f"SYSINFO: {platform.platform()}"

def cmd_dot(args):
    """Скалярное произведение numpy-массивов или списков."""
    try:
        # Ожидает строку вида: "[10, 20]|[0.1, 0.2]"
        inp_repr, w_repr = args.split('|', 1)
        inp = np.array(eval(inp_repr))
        w = np.array(eval(w_repr))
        result = np.dot(inp, w)
        # Приводим к списку для сериализации
        if hasattr(result, 'tolist'):
            result = result.tolist()
        return f"RESULT: {result}"
    except Exception as e:
        return f"ERROR: {e}"

def cmd_get_error(args):
    """Среднеквадратичная ошибка между двумя массивами."""
    try:
        # Ожидает строку вида: "[5.0]|[10]"
        pred_repr, true_repr = args.split('|', 1)
        pred = np.array(eval(pred_repr))
        true = np.array(eval(true_repr))
        error = np.mean((pred - true) ** 2)  # MSE
        return f"RESULT: {error}"
    except Exception as e:
        return f"ERROR: {e}"

# --- Регистрируем команды ---
COMMANDS = {
    "eval": cmd_eval,
    "echo": cmd_echo,
    "sysinfo": cmd_sysinfo,
    "dot": cmd_dot,
    "get_error": cmd_get_error,
}

# --- Работа с клиентами ---

def handle_client(conn, addr):
    print(f"[+] Новое подключение: {addr}")
    try:
        while True:
            data = conn.recv(4096).decode()
            if not data:
                break
            if ' ' in data:
                cmd, args = data.split(' ', 1)
            else:
                cmd, args = data, ""
            func = COMMANDS.get(cmd)
            if func:
                response = func(args)
            else:
                response = f"ERROR: Unknown command '{cmd}'"
            conn.sendall(response.encode())
    except Exception:
        traceback.print_exc()
    finally:
        conn.close()
        print(f"[-] Отключение: {addr}")

def start_server(host='0.0.0.0', port=int(input("Введите порт: "))):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"СЕРВЕР ЗАПУЩЕН! IP: {get_ip()}  PORT: {port}")
    print("Доступные команды:", ", ".join(COMMANDS.keys()))
    print("Пример запроса: 'eval 1 + 2 * 4 * x' или 'dot [10, 20]|[0.1, 0.2]'")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

def get_ip():
    # Получить локальный IP для подключения
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    start_server()