from mstrSAML import MstrSession
from mstrRESTwrapper import *
from helper import *


def main() -> None:
    # link to library - base endpoint
    # "https://example.com/MicroStrategyLibrary/"
    base_url = "https://<FQDN:port>/MicroStrategyLibrary/"

    # trying 3 times per timeout to get token. If token is not found, wait for timeout and try again
    # TODO: add hooks to check if token is available
    # timeout 10 seconds means we have 3x10 seconds to get token from browser - 30 seconds to authentitcate
    # for SSO it is necessary to read profile of the User to read all cockies etc.
    # additionally - it will fail if another browser instance is running with the same profile.
    # get profile folder path from: chrome://version => Profile Path
    # Chrome:
    session = MstrSession(base_url=base_url, timeout=10, useBrowser='Chrome',
                          user_data_dir=r'C:\Users\spock\AppData\Local\Google\Chrome\User Data')
    # SSO profile path so that it is possible to omit logging into every time - only once, until SSO token is expired
    
    # Edge
    # session = MstrSession(base_url=base_url, timeout=10, useBrowser='Edge',
                        #   user_data_dir=r'C:\Users\saint\AppData\Local\Google\Chrome\User Data')
    # issue
    # https://stackoverflow.com/questions/70240234/python-webdrivermanager-install-does-not-work-for-edge-in-custom-webdriver-in
    # Solution:
    # https://github.com/Muddyblack/custom-webdrivemanager-python

    projectID = '7734DE534E611A99DE9F539B633DC862'
    # set header to a project, which is necessary for most REST calls
    SetProject(session, projectID)
    # get document instAance
    RSDid = '6C23B0604A9471F149E79D907CD4779A'
    mstrDocument = runDocument(mstrSession=session, rsdId=RSDid)
    # export to PDF
    mstrDocumentPDF = exportToPDF(session, mstrDocument)
    pdfData = getPDFdata(mstrDocumentPDF)
    OpenInExplorerStr = savePDFtoFile(pdfData)
    print(
        '************************************************** \n ***' + OpenInExplorerStr + '\n ' + '************************************************** \n')


if __name__ == "__main__":
    main()
# pip freeze > requirements.txt
