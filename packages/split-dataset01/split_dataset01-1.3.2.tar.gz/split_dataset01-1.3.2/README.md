## 功能

划分数据集

## 使用

参数检查：确保输入的比例和重叠概率在合理范围内。
数据划分：
首先划分训练集。
然后划分验证集
最后划分测试集
随机性：使用 TensorFlow 的随机函数确保数据划分的随机性。
返回值：返回三个 tf.data.Dataset 对象，分别对应训练集、验证集和测试集。

---

"""
    将数据集划分为训练集、验证集和测试集，并允许验证集和测试集与训练集有部分重叠。

    参数：
    data (np.ndarray): 数据集，形状为 (样本数, ...)
    labels (np.ndarray): 标签集，形状为 (样本数, ...)
    train_ratio (float): 训练集比例
    val_ratio (float): 验证集比例
    test_ratio (float): 测试集比例
    overlap_prob (float): 验证集和测试集中与训练集重叠的比例（0-1）

    返回：
    train_data (tf.data.Dataset): 训练集
    val_data (tf.data.Dataset): 验证集
    test_data (tf.data.Dataset): 测试集
"""

## 包的构建

4.构建包

使用以下命令构建源代码分发：

python setup.py sdist
5.注册PyPI账户

在发布到PyPI之前，您需要在pypi.org上创建一个账户。

6.上传包到PyPI

为了上传您的包，您需要一个名为twine的工具。您可以使用pip安装它：

pip install twine
7.上传您的包：

twine upload dist/*
8.安装测试:

现在您可以使用pip安装您的包来进行测试：

pip install mypackage
9.更新包: 如果您需要更新包，请更改setup.py中的版本号，重新打包并使用twine重新上传。

注意：创建并维护一个pip包需要负责和注意的事情比以上所述的要多。确保您了解开源许可、正确的版本控制、如何处理依赖关系等。