def check_extension(filename, extension):
    """
    Check if a file has a given extension.
    """
    return filename if filename.endswith(extension) else filename + "." + extension


def deriveeUniformeDiscrete(points):
    deriv = []
    for x in range(len(points)-1):
        deriv+=[points[x+1]-points[x]]
    return deriv