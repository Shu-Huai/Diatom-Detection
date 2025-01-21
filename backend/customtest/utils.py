# customtest/utils.py
import numpy as np
import cv2
from PIL import Image
import torch
from sklearn.metrics import accuracy_score, precision_score, recall_score
from .Resnet50 import Resnet50


def load_pytorch_model(model_path, device):
    """
    加载 PyTorch 模型和权重
    """
    model = Resnet50(num_classes=2)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model


def load_image(file_path):
    """
    从 pkl 文件中加载图像数据并做适当预处理，返回一个 (C, H, W) 的 numpy 数组
    """
    image = Image.open(file_path)
    image = np.array(image)

    # 调用 resize
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # 转为 float32，归一化
    image = image / 255.0

    # 转置为 (C, H, W)
    image = np.transpose(image, (2, 0, 1))  # 假设原是 (H, W, C)

    return image


def systematic_testing(model, test_data, test_labels, device):  # k, x,
    """
    使用 PyTorch 模型进行测试。
    - model: PyTorch 模型
    - test_data: (N, C, H, W) numpy array
    - test_labels: (N,) numpy array
    - k, x: 每轮测试的次数和批量
    - device: 'cpu' or 'cuda'
    """
    print("Entering systematic_testing")
    print("test_data shape (numpy):", test_data.shape)
    print("test_labels shape (numpy):", test_labels.shape)
    # 转为 Torch Tensor 并移动到 device
    batch_size = 32
    num_batches = (test_data.shape[0] + batch_size - 1) // batch_size
    correct_predictions = 0
    predicted = np.array([])
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, test_data.shape[0])
        batch_data = test_data[start_idx:end_idx]
        batch_labels = test_labels[start_idx:end_idx]
        batch_test_data_tensor = torch.from_numpy(batch_data).to(device).float()
        print("batch_test_data_tensor shape (tensor):", batch_test_data_tensor.shape)
        print("batch_test_data_tensor after conversion:", batch_test_data_tensor.dtype)
        model.eval()
        with torch.no_grad():
            outputs = model(batch_test_data_tensor)  # shape: (N, 2) 如果是 CrossEntropy
            print("outputs shape:", outputs.shape)
            predicted = np.concatenate((predicted, outputs.argmax(dim=1).cpu().numpy()))  # shape=(N,)
            # predicted = (outputs > 0.5).long().cpu().numpy().flatten()
            print("predicted shape:", predicted.shape)
    try:
        correct_predictions = np.sum(predicted == test_labels)
        accuracy = accuracy_score(test_labels, predicted) * 100
        precision = precision_score(test_labels, predicted) * 100
        recall = recall_score(test_labels, predicted) * 100

        variance = np.var([accuracy])  # 当成演示
    except Exception as e:
        print("error computing accuracy_score:", e)
        print("predicted len =", len(predicted), "test_labels len =", len(test_labels))
        accuracy = 0

    # 构建 round_table_data_item (若需要的话，可不切片)
    round_table_data_item = [{
        'label': test_labels.tolist(),
        'predict_result': predicted.tolist(),
        'correct': int(correct_predictions),
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall
    }]

    result = {
        'predict_accurate_num': int(correct_predictions)
    }

    return result, accuracy, precision, recall, variance, round_table_data_item  # round_table_data
