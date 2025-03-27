import os
import shutil

import setuptools

# Load the long_description from README.md
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()


def clean_folder_if_exists(folder_path):
    """
    检查文件夹是否存在，如果存在且不为空则清除其内容
    :param folder_path: 要检查和清理的文件夹路径
    """
    if os.path.exists(folder_path):
        if os.listdir(folder_path):
            try:
                # 递归删除文件夹及其内容
                shutil.rmtree(folder_path)
                # 重新创建空文件夹
                os.makedirs(folder_path)
                print(f"成功清除文件夹 {folder_path} 内的所有内容。")
            except Exception as e:
                print(f"清除文件夹 {folder_path} 内容时出现错误: {e}")


def increment_version(md_file_path):
    try:
        with open(md_file_path, "r", encoding="utf-8") as file:
            version_str = file.read().strip()
        version_parts = [int(part) for part in version_str.split('.')]
        if len(version_parts) != 3:
            raise ValueError("版本号需为 x.y.z 格式")

        # 直接递增最后一位，自动处理进位
        version_parts[2] += 1
        for i in range(2, 0, -1):
            if version_parts[i] >= 100:  # 常规版本号 z 位建议 0-99
                version_parts[i] = 0
                version_parts[i - 1] += 1

        new_version_str = '.'.join(map(str, version_parts))
        with open(md_file_path, "w", encoding="utf-8") as file:
            file.write(new_version_str)
        return new_version_str
    except FileNotFoundError:
        print(f"未找到 {md_file_path} 文件")
        raise
    except ValueError as e:
        print(e)
        raise


version = increment_version('version.txt')
clean_folder_if_exists('dist')

setuptools.setup(
    name="ymskan",
    version=version,
    author="yms",
    author_email="226000@qq.com",
    description="works",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        'pykan': [
            'figures/lock.png',
            'assets/img/sum_symbol.png',
            'assets/img/mult_symbol.png',
        ],
    },
    python_requires='>=3.6',
)
