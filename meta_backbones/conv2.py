import torch.nn as nn
from torchmeta.modules import (MetaModule, MetaSequential, MetaConv2d,
                               MetaBatchNorm2d, MetaLinear)

def conv3x3(in_channels, out_channels, **kwargs):
    return MetaSequential(
        MetaConv2d(in_channels, out_channels, kernel_size=3, padding=1, **kwargs),
        MetaBatchNorm2d(out_channels, momentum=1., track_running_stats=False),
        nn.ReLU(),
        nn.MaxPool2d(2)
    )

class Conv2(MetaModule):
    def __init__(self, in_channels=3, hid_channels=64):
        super(Conv2, self).__init__()
        self.in_channels = in_channels
        self.hid_channels = hid_channels

        self.encoder = MetaSequential(
            conv3x3(in_channels, hid_channels),
            conv3x3(hid_channels, hid_channels)
        )


    def forward(self, inputs, params=None):
        features = self.encoder(inputs, params=self.get_subdict(params, 'features'))
        return features
        
def conv2(**kwargs):
    return Conv2(**kwargs)

