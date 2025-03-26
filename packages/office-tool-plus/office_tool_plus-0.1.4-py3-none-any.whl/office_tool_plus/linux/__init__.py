from .app import LinuxTools

linux = LinuxTools()


def single_to_pdf(input_path, convert_to="pdf", output_dir=None, java_home=None, lang=None):
    return linux.libreoffice(input_path, convert_to, output_dir, java_home, lang)


def many_to_pdf(input_dir, suffix, convert_to="pdf", output_dir=None, java_home=None, lang=None, recursive=False):
    return linux.many_to_pdf(input_dir, suffix, convert_to, output_dir, java_home, lang, recursive)
