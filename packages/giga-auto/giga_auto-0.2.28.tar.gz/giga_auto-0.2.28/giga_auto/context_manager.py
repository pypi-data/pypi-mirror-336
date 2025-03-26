import copy
import os
import shutil
import tempfile
from contextlib import contextmanager


@contextmanager
def folder_context(folder_path=''):
    """
    上下文管理器：进入时操作 文件，退出时自动删除整个文件夹。
    """
    try:
        if not folder_path:
            folder_path = tempfile.gettempdir() + os.sep + "api_test_folder"

        os.makedirs(folder_path, exist_ok=True)  # 如果文件夹不存在则创建
        yield folder_path  # 暴露文件夹路径给 with 块
    finally:
        # 退出时删除文件夹及其内容
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

@contextmanager
def header_manager(headers, update_headers=None, remove_headers=None):
    """
    Context manager for managing headers.

    :param headers: The original headers dictionary.
    :param update_headers: A dictionary of headers to update or add.
    :param remove_headers: A list of header keys to remove.
    """

    # Make a copy of the original headers
    original_headers = copy.copy(headers)

    # Update headers with new values
    if update_headers:
        for key, value in update_headers.items():
            headers[key] = value

    # Remove specified headers
    if remove_headers:
        for key in remove_headers:
            if key in headers:
                del headers[key]
    try:
        yield
    finally:
        # Restore the original headers
        headers.clear()
        headers.update(original_headers)


@contextmanager
def download_file(response, filename):
    """
    上下文管理器：保存 Excel 响应内容到本地，并在退出时自动清理

    :param response: `requests` 的响应对象，需确保 response.content 是 Excel 文件
    :param filename: 自定义保存的文件名
    :return: 返回本地 Excel 文件路径
    """
    if response.status_code != 200:
        raise RuntimeError(f"下载失败，状态码：{response.status_code}")

    # 获取当前项目的临时目录
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)

    # 保存文件
    with open(file_path, "wb") as f:
        f.write(response.content)

    try:
        yield file_path  # 返回 Excel 文件路径
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)  # 退出时自动删除文件