import time


def on_cooldown(seconds: int):
    def decorator(func):
        last_executed: int = 0

        def wrapper(*args, **kwargs):
            nonlocal last_executed
            now = int(time.time())

            if (now - last_executed) >= seconds:
                last_executed = now

                return func(*args, **kwargs)
            else:
                raise Exception(
                    f"On cooldown for {seconds - last_executed} more seconds"
                )

        return wrapper

    return decorator
