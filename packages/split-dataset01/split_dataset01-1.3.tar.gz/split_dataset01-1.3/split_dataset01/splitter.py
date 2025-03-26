import tensorflow as tf
import numpy as np

def splitter(data, labels, train_ratio, val_ratio, test_ratio, seed=None, overlap_prob=0.75):
    """
    将数据集划分为训练集、验证集和测试集，并允许验证集和测试集与训练集有部分重叠。
    
    参数：
    data (np.ndarray): 数据集，形状为 (样本数, ...)
    labels (np.ndarray): 标签集，形状为 (样本数, ...)
    train_ratio (float): 训练集比例
    val_ratio (float): 验证集比例
    test_ratio (float): 测试集比例
    overlap_prob (float): 验证集和测试集中与训练集重叠的比例（0-1）
    seed (int): 随机种子，用于确保结果可复现
    
    返回：
    train_dataset (tf.data.Dataset): 训练集
    val_dataset (tf.data.Dataset): 验证集
    test_dataset (tf.data.Dataset): 测试集
    """
    # 设置随机种子
    if seed is not None:
        tf.random.set_seed(seed)
        np.random.seed(seed)
    
    # 确保比例之和不超过 1
    assert train_ratio + val_ratio + test_ratio <= 1, "Total ratio must be <= 1"
    
    # 确保 overlap_prob 在 0-1 之间
    assert 0 <= overlap_prob <= 1, "Overlap probability must be between 0 and 1"
    
    # 计算各数据集大小
    num_samples = data.shape[0]
    train_size = int(num_samples * train_ratio)
    val_size = int(num_samples * val_ratio)
    test_size = int(num_samples * test_ratio)
    
    # 创建随机索引
    indices = tf.random.shuffle(tf.range(num_samples))
    
    # 划分训练集
    train_indices = indices[:train_size]
    train_data = tf.gather(data, train_indices)
    train_labels = tf.gather(labels, train_indices)
    
    # 计算验证集和测试集中与训练集重叠的部分
    overlap_size_val = int(val_size * overlap_prob)
    overlap_size_test = int(test_size * overlap_prob)
    
    # 验证集划分
    val_indices = tf.concat([
        tf.random.shuffle(train_indices)[:overlap_size_val],
        tf.random.shuffle(indices[train_size:train_size + val_size - overlap_size_val])
    ], axis=0)
    val_data = tf.gather(data, val_indices)
    val_labels = tf.gather(labels, val_indices)
    
    # 测试集划分
    test_indices = tf.concat([
        tf.random.shuffle(train_indices)[:overlap_size_test],
        tf.random.shuffle(indices[train_size + val_size:train_size + val_size + test_size - overlap_size_test])
    ], axis=0)
    test_data = tf.gather(data, test_indices)
    test_labels = tf.gather(labels, test_indices)
    
    # 创建 tf.data.Dataset
    train_dataset = tf.data.Dataset.from_tensor_slices((train_data, train_labels))
    val_dataset = tf.data.Dataset.from_tensor_slices((val_data, val_labels))
    test_dataset = tf.data.Dataset.from_tensor_slices((test_data, test_labels))
    
    return train_dataset, val_dataset, test_dataset

# 使用示例
# if __name__ == "__main__":
#     # 创建示例数据
#     data = np.random.rand(1000, 28, 28, 1).astype(np.float32)
#     labels = np.random.randint(0, 10, size=(1000,)).astype(np.int32)
    
#     # 设置随机种子以确保结果可复现
#     seed = 42
    
#     # 划分数据集
#     train_ratio = 0.7
#     val_ratio = 0.15
#     test_ratio = 0.15
#     overlap_prob = 0.3  # 验证集和测试集中与训练集重叠的比例
    
#     train_dataset, val_dataset, test_dataset = split_dataset(
#         data, labels, train_ratio, val_ratio, test_ratio, overlap_prob, seed
#     )
    
#     # 打印各数据集大小
#     print("Train dataset size:", len(train_dataset))
#     print("Validation dataset size:", len(val_dataset))
#     print("Test dataset size:", len(test_dataset))
    
#     # 打印各数据集的前几个样本
#     for images, labels in train_dataset.take(2):
#         print("\nTrain dataset samples:")
#         print("Images shape:", images.shape)
#         print("Labels:", labels.numpy())
    
#     for images, labels in val_dataset.take(2):
#         print("\nValidation dataset samples:")
#         print("Images shape:", images.shape)
#         print("Labels:", labels.numpy())
    
#     for images, labels in test_dataset.take(2):
#         print("\nTest dataset samples:")
#         print("Images shape:", images.shape)
#         print("Labels:", labels.numpy())