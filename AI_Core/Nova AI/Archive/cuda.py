import torch
print(torch.cuda.is_available())  # Should return True if CUDA is enabled
print(torch.cuda.current_device())  # Should print the current GPU device ID (usually 0)
print(torch.cuda.get_device_name(0))  # Should print the GPU name (RTX 3060 Ti)
