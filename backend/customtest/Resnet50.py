# customtest/Resnet50.py 系统内模型定义
import math
import torch.nn as nn


class Resnet50(nn.Module):
    def __init__(self, layers=[3, 4, 6, 3], num_classes=2):
        super(Resnet50, self).__init__()
        self.inplanes = 64
        # 改成3通道
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.stack1 = self.make_stack(64, layers[0])
        self.stack2 = self.make_stack(128, layers[1], stride=2)
        self.stack3 = self.make_stack(256, layers[2], stride=2)
        self.stack4 = self.make_stack(512, layers[3], stride=2)
        self.avgpool = nn.AvgPool2d(7, stride=1)
        self.fc = nn.Linear(2048, 2)

        self.init_param()

    def init_param(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                n = m.weight.shape[0] * m.weight.shape[1]
                m.weight.data.normal_(0, math.sqrt(2. / n))
                m.bias.data.zero_()

    def make_stack(self, planes, blocks, stride=1):
        downsample = None
        layers = []

        if stride != 1 or self.inplanes != planes * Bottleneck.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * Bottleneck.expansion,
                          kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes * Bottleneck.expansion),
            )

        layers.append(Bottleneck(self.inplanes, planes, stride, downsample))
        self.inplanes = planes * Bottleneck.expansion
        for i in range(1, blocks):
            layers.append(Bottleneck(self.inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)  # [B, 3, 224, 224] -> [B, 64, 112, 112]
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)  # [B, 64, 56, 56]

        x = self.stack1(x)  # -> [B, 256, 56, 56]
        x = self.stack2(x)  # -> [B, 512, 28, 28]
        x = self.stack3(x)  # -> [B, 1024,14, 14]
        x = self.stack4(x)  # -> [B, 2048, 7, 7]

        x = self.avgpool(x)  # -> [B, 2048, 1, 1]
        x = x.view(x.size(0), -1)  # -> [B, 2048]
        x = self.fc(x)  # -> [B, 2]
        # 不再做 ReLU，因为这是最终分类输出，可根据需要加上 softmax 或在外部处理
        return x


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride,
                               padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, planes * 4, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * 4)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


def resnet50(num_classes=2):
    """
    工厂函数，方便在其他地方直接调用:
    model = resnet50(num_classes=2)
    """
    return Resnet50(layers=[3, 4, 6, 3], num_classes=num_classes)
