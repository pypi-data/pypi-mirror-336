import torch

DEVICE_CPU = torch.device("cpu")
DEVICE_MPS = torch.device("mps")


def get_device():
    if torch.backends.mps.is_available():
        print(f"[get_device] mps device count: {torch.mps.device_count()}")
        result = DEVICE_MPS
    else:
        print("[get_device] MPS device not found!")
        result = DEVICE_CPU
    return result
