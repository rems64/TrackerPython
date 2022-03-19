def check_extension(filename, extension):
    """
    Check if a file has a given extension.
    """
    return filename if filename.endswith(extension) else filename + "." + extension