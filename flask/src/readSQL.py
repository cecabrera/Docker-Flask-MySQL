def readSQL(filename: str):
    """ Read SQL file as text

    Args:
        filename (text): file to read
    Return:
        sqlFile (text): info read
    """

    fd = open(file= filename,mode= 'r')

    sqlFile = fd.read()

    fd.close()

    return sqlFile
