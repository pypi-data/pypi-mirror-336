from .app import ExcelTools

excel = ExcelTools()


def single_to_pdf(excel_path, sheet_names=None, pdf_dir=None):
    return excel.single_to_pdf(excel_path, sheet_names, pdf_dir)


def many_to_pdf(excel_dir, suffix=None, recursive=True, pdf_dir=None):
    return excel.many_to_pdf(excel_dir, suffix, recursive, pdf_dir)


def from_template(template_file, labor_datas, sheet_name=None, output_dir=None):
    return excel.from_template(template_file, labor_datas, sheet_name, output_dir)
