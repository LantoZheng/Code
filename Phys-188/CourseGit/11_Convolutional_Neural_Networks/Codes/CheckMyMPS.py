# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 12:01:51 2024

@author: MMH_user
"""

#if cuda is not recognized, run:
#pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118


import torch

def test_mps():
    print("PyTorch version: ", torch.__version__)
    print("MPS Available: ", torch.backends.mps.is_available())
    if torch.backends.mps.is_available():
        print("MPS is built and available on this system!")
        # Create a test tensor to verify MPS works
        try:
            device = torch.device("mps")
            x = torch.ones(5, device=device)
            print("Successfully created tensor on MPS device:", x)
        except Exception as e:
            print("Error creating tensor on MPS:", e)
    else:
        print("MPS is not available on this system.")

if __name__ == "__main__":
    test_mps()