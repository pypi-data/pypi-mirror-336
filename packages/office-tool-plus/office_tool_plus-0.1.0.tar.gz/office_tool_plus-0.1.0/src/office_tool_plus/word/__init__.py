from .app import WordTools

word = WordTools()


def single_to_pdf(word_path, pdf_dir=None):
    return word.single_to_pdf(word_path, pdf_dir)


def many_to_pdf(word_dir, suffix=None, recursive=True, pdf_dir=None):
    return word.many_to_pdf(word_dir, suffix, recursive, pdf_dir)
