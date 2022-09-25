import torch
import numpy as np


IMAGE_DIM = 84

class DQN(torch.nn.Module):
    def __init__(self):
        super(DQN, self).__init__()

        in_channels1 = 4
        num_filters1 = 16
        kernel_dim1 = 3
        stride1 = 2
        self.conv1 = torch.nn.Conv2d(in_channels=in_channels1,
                                     out_channels=num_filters1,
                                     kernel_size=kernel_dim1,
                                     stride=stride1)
        
        # in_channels2 = num_filters1
        # num_filters2 = 32
        # kernel_dim2 = 4
        # stride2 = 2
        # self.conv2 = torch.nn.Conv2d(in_channels=in_channels2,
        #                              out_channels=num_filters2,
        #                              kernel_size=kernel_dim2,
        #                              stride=stride2)
        

        self.fc = torch.nn.Linear(1600, 4)
    
    def forward(self, phi):
        out1 = self.conv1(phi)
        out2_flat = torch.flatten(out1, 1)  # don't flatten batch dimension
        out3 = self.fc(out2_flat)
        return out3


if __name__ == "__main__":
    net = DQN()

    img = np.zeros((32, 4, 21, 21))
    net(torch.tensor(img).float())
