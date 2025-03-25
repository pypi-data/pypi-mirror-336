#
#
# class FileUtils:
#
#     @staticmethod
#     def extract_and_count_files(file_path, extract_to='.'):
#         import zipfile
#         import tarfile
#
#         if file_path.endswith('.zip'):
#             with zipfile.ZipFile(file_path, 'r') as zip_ref:
#                 zip_ref.extractall(extract_to)
#                 # 只统计文件，不包括文件夹
#                 file_count = sum(1 for f in zip_ref.namelist() if not f.endswith('/'))
#
#         elif file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
#             with tarfile.open(file_path, 'r:gz') as tar_ref:
#                 tar_ref.extractall(path=extract_to)
#                 # 只统计文件
#                 file_count = sum(1 for m in tar_ref.getmembers() if m.isfile())
#         else:
#             raise ValueError("不支持的压缩文件格式，仅支持 .zip 和 .tar.gz/.tgz")
#         return file_count
#
#     @staticmethod
#     def read_pdf_pypdf(path):
#         import PyPDF2
#         text = ""
#         with open(path, 'rb') as f:
#             reader = PyPDF2.PdfReader(f)
#             for page in reader.pages:
#                 text += page.extract_text()
#         return text
#
#
#
# if __name__ == '__main__':
#     FileUtils.extract_and_count_files('C:/Users/LANGMUQING/Downloads/SHIPPING_ORDER_BOOK.zip','C:/Users/LANGMUQING/Downloads/SHIPPING_ORDER_BOOK')