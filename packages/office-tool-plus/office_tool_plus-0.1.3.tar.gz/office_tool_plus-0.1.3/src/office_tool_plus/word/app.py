from docx.shared import Inches

from ..utils import *
from docxtpl import DocxTemplate, InlineImage


class WordTools:
    def __init__(self):
        self.app = None

    def create_app(self):
        from win32com.client import gencache
        self.app = gencache.EnsureDispatch("Word.Application")
        self.app.Visible = False

    def close_app(self):
        self.app.Quit()
        self.app = None

    @check_platform('windows')
    def single_to_pdf(self, word_path, pdf_dir=None):
        """
        将单个Word文档转换为PDF格式。

        :param word_path: Word文档的文件路径。
        :param pdf_dir: PDF文件的保存目录，如果未提供，则默认保存在Word文档的同目录下。
        :return: 转换后的PDF文件路径。
        """
        from win32com.client import constants
        # 检查并准备文件路径
        word_path = check_file_path(word_path)
        pdf_path = save_file_path(word_path, ".pdf", pdf_dir)

        # 如果没有提供特定的工作表名称，则导出所有工作表
        if self.app is None:
            self.create_app()
        # 打开Word文档，设置为只读模式
        doc = self.app.Documents.Open(str(word_path), ReadOnly=1)

        try:
            # 将Word文档导出为PDF格式
            doc.ExportAsFixedFormat(pdf_path, constants.wdExportFormatPDF)
        except Exception as e:
            print(f"导出word到PDF时出错：{e}")

        # 关闭时不保存更改
        doc.Close(SaveChanges=False)

        # 退出应用程序
        self.app.Quit()
        self.app = None

        # 返回导出的PDF文件路径
        return pdf_path

    @check_platform('windows')
    def many_to_pdf(self, word_dir, suffix=None, recursive=True, pdf_dir=None):
        """
        将指定目录下的Excel文件转换为PDF格式。

        参数:
        - word_dir: str,  Word 文件所在目录
        - pdf_dir: str, PDF文件的保存目录。如果未提供，则默认保存在Excel文件的同目录下。
        """
        from win32com.client import constants
        suffix = suffix or ["*.doc", "*.docx"]
        word_path_yield = search_files(word_dir, suffix, recursive)
        if self.app is None:
            self.create_app()
        for word_path in word_path_yield:
            # 检查并准备文件路径
            pdf_path = save_file_path(word_path, ".pdf", pdf_dir)
            # 打开Word文档，设置为只读模式
            doc = self.app.Documents.Open(str(word_path), ReadOnly=1)
            try:
                # 将Word文档导出为PDF格式
                doc.ExportAsFixedFormat(pdf_path, constants.wdExportFormatPDF)
            except Exception as e:
                print(f"导出word到PDF时出错：{e}")

            # 关闭时不保存更改
            doc.Close(SaveChanges=False)

        # 退出Excel应用程序
        self.app.Quit()
        self.app = None

    @staticmethod
    def from_template(template_file, labor_datas, output_dir=None):
        """
        从模板文件生成文档。

        根据提供的模板文件、模板数据以及输出目录，为每个数据生成文档。

        参数:
        - template_file: 模板文件的路径。
        - labor_datas: 包含模板替换信息的列表，每个元素是一个字典。
        - output_dir: 输出文件的目录，如果未提供，则默认为模板文件所在目录。

        返回:
        无返回值，但会在指定输出目录下生成文档。
        """
        # 确保模板文件路径有效
        abs_template_file = check_file_path(template_file)
        # 获取路径、文件名和后缀
        output_dir = output_dir or os.path.dirname(abs_template_file)
        template_name = os.path.basename(abs_template_file)
        tmp_file_name, tmp_file_suffix = os.path.splitext(template_name)
        # 打开模板文件
        tmp_doc = DocxTemplate(abs_template_file)
        # 遍历数据
        for lb in labor_datas:
            # 准备文件名和照片
            new_file_name = lb.get("文件名", lb.get("姓名", tmp_file_name))
            photo_key_value = {k: v for k, v in lb.items() if k.endswith("照片")}
            for photo in photo_key_value:
                img_path = check_file_path(lb.get(photo, None))
                if img_path:
                    lb[photo] = InlineImage(tmp_doc, str(img_path), width=Inches(1))
                else:
                    lb[photo] = None
            # 生成唯一的输出文件路径
            output_file = unique_file_path(str(os.path.join(output_dir, new_file_name + tmp_file_suffix)))
            # 使用数据渲染模板并保存文档
            tmp_doc.render(lb)
            tmp_doc.save(output_file)
