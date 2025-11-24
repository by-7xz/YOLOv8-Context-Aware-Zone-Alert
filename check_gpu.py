import torch

print(f"Pytorch V:{torch.__version__}")

is_availabe = torch.cuda.is_available()
print(f"CUDA Availabe:{is_availabe}")

if is_availabe:
    print(f"GPU NAME:{torch.cuda.get_device_name(0)}")
else:
    print("CUDA IS NOT AVAILABLE")