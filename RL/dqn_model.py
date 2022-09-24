import torch
import numpy as np


IMAGE_DIM = 84

class DQN(torch.nn.Module):
    def __init__(self):
        super(DQN, self).__init__()

        in_channels1 = 4
        num_filters1 = 16
        kernel_dim1 = 8
        stride1 = 4
        self.conv1 = torch.nn.Conv2d(in_channels=in_channels1,
                                     out_channels=num_filters1,
                                     kernel_size=kernel_dim1,
                                     stride=stride1)
        
        in_channels2 = num_filters1
        num_filters2 = 32
        kernel_dim2 = 4
        stride2 = 2
        self.conv2 = torch.nn.Conv2d(in_channels=in_channels2,
                                     out_channels=num_filters2,
                                     kernel_size=kernel_dim2,
                                     stride=stride2)
        

        self.fc = torch.nn.Linear(82944, 4)
    
    def forward(self, phi):
        out1 = self.conv1(phi)
        print(f"self.conv1: {out1.shape}")
        out2 = self.conv2(out1)
        print(f"self.conv2: {out2.size()}")
        out2_flat = out2.flatten()
        out3 = self.fc(out2_flat)
        print(f"out3.shape: {out3.shape}")
        return out3


if __name__ == "__main__":
    net = DQN()

    img = np.zeros((32, 4, 84, 84))
    net(torch.tensor(img).float())
