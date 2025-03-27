from .app import WordTools

word = WordTools()


def single_to_pdf(word_path, pdf_dir=None):
    return word.single_to_pdf(word_path, pdf_dir)


def many_to_pdf(word_dir, suffix=None, recursive=True, pdf_dir=None):
    return word.many_to_pdf(word_dir, suffix, recursive, pdf_dir)


def from_template(template_file, labor_datas, output_dir=None, save_in_memory=False):
    return word.from_template(template_file, labor_datas, output_dir, save_in_memory)
