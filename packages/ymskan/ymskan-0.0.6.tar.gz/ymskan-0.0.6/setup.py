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
        # 读取文件中的版本号
        with open(md_file_path, "r", encoding="utf-8") as file:
            version_str = file.read().strip()
        # 将版本号按 . 分割成列表
        version_parts = [int(part) for part in version_str.split('.')]

        # 确保版本号至少有三位
        if len(version_parts) != 3:
            raise ValueError("版本号格式不正确，请确保为 x.y.z 格式。")

        # 从最后一位开始加 1
        index = 2
        while index >= 0:
            if index == 2:
                # 右边部分按 100 进制进位
                version_parts[index] += 1
                if version_parts[index] < 100:
                    break
                version_parts[index] = 0
                index -= 1
            elif index == 1:
                # 中间部分按 10 进制进位
                version_parts[index] += 1
                if version_parts[index] < 10:
                    break
                version_parts[index] = 0
                index -= 1
            else:
                # 左边部分进位
                version_parts[index] += 1
                break

        # 将更新后的版本号重新组合成字符串
        new_version_str = '.'.join(map(str, version_parts))

        # 将新的版本号写回文件
        with open(md_file_path, "w", encoding="utf-8") as file:
            file.write(new_version_str)
        return new_version_str
    except FileNotFoundError:
        print(f"未找到 {md_file_path} 文件，请检查文件路径。")
    except ValueError as e:
        print(e)
    return None


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
