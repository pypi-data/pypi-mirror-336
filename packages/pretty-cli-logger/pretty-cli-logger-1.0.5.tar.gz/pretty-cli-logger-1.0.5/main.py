import datetime
import sys

def _colors_enabled():
    return sys.stdout.isatty()

def _colored(message: str, color: str): 
    if _colors_enabled():
        return f"\033[{color}m{message}\033[0m"
    else:
        return message

def _get_timestamp():
    now = datetime.datetime.utcnow()
    ms = now.microsecond // 1000
    return now.strftime("%Y/%m/%d %H:%M:%S") + f".{ms:03d}"

def _print_log(color: str, label: str, message: str):
    label = f"({label})"
    timestamp = f"[{_get_timestamp()}]"
    timestamp_c = "90"
    print(f"{_colored(label, color)} {_colored(timestamp, timestamp_c)} {_colored(message, color)}")

    if len(message) > 1:
        import colors
        colors.update_colors(1)

def log_debg(message):
    _print_log("90", "DEBG", message)

def log_info(message):
    _print_log("32", "INFO", message)

def log_warn(message):
    _print_log("33", "WARN", message)

def log_err(message):
    _print_log("31", "ERR ", message)

if __name__ == "__main__":
    log_debg("This is debug")
    log_info("This is info")
    log_warn("This is warn")
    log_err("This is err")