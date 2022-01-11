from base64 import b64decode
import os


def savePDFtoFile(data: str, filePathName='export.pdf') -> str:
    """Saves the PDF base64 string to a file

    Args:
        data (str): base64 encoded string
        filePathName (str, optional): path to where the file should be saved. Defaults to 'export.pdf' in current directory.

    Raises:
        ValueError: Tough luck

    Returns:
        str: file path
    """
    if filePathName == 'export.pdf':
        filePathName = os.getcwd() + '/' + filePathName

    pdfByte = b64decode(data, validate=True)
    # Perform a basic pdf signature validation to make sure that the result is a PDF file
    # FYI - The 'magic' file signature is not 100% reliable in validating PDF files
    if pdfByte[0:4] != b'%PDF':
        raise ValueError('Missing the PDF byte signature')
    else:
        file = open(filePathName, "wb")
        file.write(pdfByte)
        file.close()
    return filePathName


def getPDFdata(rsdPDFdocument) -> str:
    """Unpacks response JSON to data dict

    Args:
        rsdPDFdocument ([type]): response object from exportToPDF()

    Returns:
        str: base64 string
    """
    dataDict = dict()
    dataDict.update(**rsdPDFdocument.json())
    # return base64 string
    return dataDict['data']
