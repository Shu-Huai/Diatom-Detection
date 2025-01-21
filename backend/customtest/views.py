# customtest/views.py
import datetime
import os
import uuid
from openpyxl import Workbook
from django.http import HttpResponse
import io
import numpy as np
from django.core.cache import cache
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
import torch
from users.models import User
from .forms import CustomTestForm
from .models import ImageData
from .utils import load_image, systematic_testing, load_pytorch_model


@api_view(['GET'])
def data(request):
    user_count = User.objects.count()
    total_sample_num = ImageData.objects.count()
    return Response({
        'userCount': user_count,
        'total_sample_num': total_sample_num,
    }, status=200)


@api_view(['POST'])
def custom_test_view(request):
    """
    接收 k(测试轮数) 和 x(每轮测试样本数)，执行测试并返回 JSON，包括 test_id。
    """
    form = CustomTestForm(request.data)
    if not form.is_valid():
        return Response({'code': 1, 'msg': '输入不合法', 'errors': form.errors}, status=400)

    k = form.cleaned_data['k']
    x = form.cleaned_data['x']

    # 检查是否有足够的测试样本
    total_available = ImageData.objects.filter(dataset='test').count()
    if x > total_available:
        return Response({'code': 3, 'msg': f'可用测试样本不足，单轮需要 {x} 个，但当前只有 {total_available} 个'},
                        status=400)

    try:
        print(os.path.join(os.path.dirname(os.path.abspath(
            __file__)), 'resnet50_diatom_best_1.pth'))
        model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resnet50_diatom_best_1.pth')
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = load_pytorch_model(model_dir, device=device)
    except Exception as e:
        return Response({'code': 4, 'msg': f'模型加载失败: {str(e)}'}, status=500)

    # 记录测试开始时间
    start_time = timezone.now()

    results_list = []
    table_data = []
    serial_number = 1  # 初始化序号

    for round_index in range(1, k + 1):
        # 每轮随机抽取 x 个样本
        round_data = ImageData.objects.filter(dataset='test').order_by('?')[:x]

        test_data = []
        test_labels = []
        test_sample_names = []

        for image_data in round_data:
            data = load_image(image_data.file.path)
            test_data.append(data)
            test_labels.append(image_data.label)
            test_sample_names.append(os.path.basename(image_data.file.name))  # 获取文件名作为样本名称

        test_data = np.array(test_data)
        test_labels = np.array(test_labels)
        print("Before calling systematic_testing, test_data.shape =", test_data.shape, "test_labels.shape=",
              test_labels.shape)
        try:
            # 调用 systematic_testing
            (result,
             avg_acc,
             avg_prec,
             avg_rec,
             variance,
             round_table_data_item) = systematic_testing(model, test_data, test_labels, device)  # 每轮1次测试
        except Exception as e:
            print("Error in systematic_testing:", e)
            return Response({'code': 5, 'msg': f'测试过程中出错: {str(e)}'}, status=500)

        # 汇总结果
        results_list.append({
            'round_index': round_index,
            'predict_accurate_num': int(result['predict_accurate_num']),  # 转换为 Python int
            'accuracy': round(float(avg_acc), 2),  # 转换为 Python float
            'precision': round(float(avg_prec), 2),
            'recall_rate': round(float(avg_rec), 2)
        })

        # 添加到表格数据
        for row in round_table_data_item:
            labels = row['label']  # 列表
            predictions = row['predict_result']  # 列表

            for i in range(len(labels)):
                label = labels[i]
                predict = predictions[i]
                sample_name = test_sample_names[i]

                table_data.append({
                    'test_no': serial_number,  # 序号
                    'test_sample_name': sample_name,  # 样本名称
                    'label': label,  # 实际标签 (1 或 0)
                    'predict': predict ,  # 测试标识 (1 或 0)
                    'predict_result': 1 if predict == label else 0  # 是否预测正确 (1 或 0)
                })

                serial_number += 1  # 序号递增

    # 计算总体指标
    avgAccuracy = round(float(np.mean([r['accuracy'] for r in results_list])), 2)
    avgPrecision = round(float(np.mean([r['precision'] for r in results_list])), 2)
    avgRecallRate = round(float(np.mean([r['recall_rate'] for r in results_list])), 2)
    variance = round(float(np.var([r['accuracy'] for r in results_list])), 2) if k > 1 else 0.0  # 当k=1时，方差为0.0

    # 记录测试结束时间
    end_time = timezone.now()
    duration = end_time - start_time  # timedelta 对象
    duration_seconds = duration.total_seconds()
    # 格式化为 hh:mm:ss
    duration_str = str(datetime.timedelta(seconds=int(duration_seconds)))

    # 获取总样本数、训练样本数、测试样本数
    totalSampleNum = ImageData.objects.count()
    totalTrainSampleNum = ImageData.objects.filter(dataset='train').count()
    totalTestSampleNum = ImageData.objects.filter(dataset='test').count()

    # 生成唯一的 test_id
    test_id = str(uuid.uuid4())

    # 构建结果数据
    result_data = {
        'k': k,
        'x': x,
        'avg_acc': avgAccuracy,
        'avg_prec': avgPrecision,
        'avg_rec': avgRecallRate,
        'variance': variance,
        'results_list': results_list,
        'table_data': table_data,
        'total_sample_num': totalSampleNum,
        'total_train_sample_num': totalTrainSampleNum,
        'total_test_sample_num': totalTestSampleNum,
        'test_time': duration_str,
        'end_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # 将数据保存到 Redis，设置过期时间（例如1小时）
    cache.set(f'test_result_{test_id}', result_data, timeout=3600)

    # 添加调试信息
    print(f"Session Data Saved: test_id={test_id}")

    # 返回 test_id 以便前端使用
    return Response({
        'code': 0,
        'msg': '测试完成',
        'k': k,
        'x': x,
        'test_id': test_id,
        'results_list': results_list,
        'table_data': table_data,
        'avg_acc': avgAccuracy,
        'avg_prec': avgPrecision,
        'avg_rec': avgRecallRate,
        'variance': variance,
        'total_sample_num': totalSampleNum,
        'total_train_sample_num': totalTrainSampleNum,
        'total_test_sample_num': totalTestSampleNum,
        'test_time': duration_str,
        'end_time': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    }, status=200)


@api_view(['GET'])
def export_excel_view(request):
    """
    导出自定义测试结果到 Excel (GET 请求).
    需要通过 URL 参数传递 test_id，例如: /customtest/export-excel/?test_id=xxx
    """
    test_id = request.query_params.get('test_id')
    if not test_id:
        return Response({'code': 2, 'msg': '缺少 test_id 参数'}, status=400)

    # 从 Redis 中获取测试数据
    test_data = cache.get(f'test_result_{test_id}')
    if not test_data:
        return Response({'code': 1, 'msg': '没有可导出的数据, 请先执行测试'}, status=400)

    avg_acc = test_data['avg_acc']
    avg_prec = test_data['avg_prec']
    avg_rec = test_data['avg_rec']
    variance = test_data['variance']
    results_list = test_data['results_list']
    table_data = test_data['table_data']
    total_sample_num = test_data['total_sample_num']
    total_train_sample_num = test_data['total_train_sample_num']
    total_test_sample_num = test_data['total_test_sample_num']
    test_round_num = test_data['k']
    samples_per_round = test_data['x']
    test_time = test_data['test_time']
    end_time = test_data['end_time']

    # 创建 Excel 文件
    wb = Workbook()

    # 汇总结果表
    ws_summary = wb.active
    ws_summary.title = "汇总结果"
    ws_summary.append(["数据摘要"])
    ws_summary.append(["总样本数", total_sample_num])
    ws_summary.append(["训练样本数", total_train_sample_num])
    ws_summary.append(["测试样本数", total_test_sample_num])
    ws_summary.append(["测试轮次数", test_round_num])
    ws_summary.append(["每轮随机选取的样本数", samples_per_round])
    ws_summary.append(["测试耗时", test_time])
    ws_summary.append(["测试时间", end_time])
    ws_summary.append([])  # 空行分隔

    ws_summary.append(["平均准确率(%)", "平均精确率(%)", "平均召回率(%)", "方差"])
    ws_summary.append([avg_acc, avg_prec, avg_rec, variance])

    ws_summary.append([])
    ws_summary.append(["轮次", "正确数", "准确率(%)", "精确率(%)", "召回率(%)"])
    for item in results_list:
        ws_summary.append([
            item['round_index'],
            item['predict_accurate_num'],
            item['accuracy'],
            item['precision'],
            item['recall_rate']
        ])

    # **2. 测试明细表**
    ws_detail = wb.create_sheet("测试明细")
    ws_detail.append(["序号", "样本名称", "实际标签", "测试标识", "是否预测正确"])
    for row in table_data:
        ws_detail.append([
            row['test_no'],  # 序号
            row['test_sample_name'],  # 样本名称
            row['label'],  # 实际标签
            row['predict'],
            "正确" if row['predict_result'] == 1 else "错误"  # 是否预测正确
        ])

    # 写入内存
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    # 返回文件下载
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="test_result_{test_id}.xlsx"'
    return response
