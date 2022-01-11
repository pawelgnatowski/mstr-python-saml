from requests import Session
from requests import Response


mstrRESTendpoints = dict()
mstrRESTendpoints['identityToken'] = 'api/auth/identityToken'
mstrRESTendpoints['getRSDinstance'] = 'api/documents/{}/instances'


def SetProject(mstrSession, projectID) -> None:
    """Sets the project ID to be used in subsequent requests

    Args:
        mstrSession (Session): the requests.Session object to be used with subsequent requests to the MSTR REST API
        projectID (str): the project ID to be used in subsequent requests 
    """    
    mstrSession.headers.update({'X-MSTR-ProjectID': projectID})


def SetIdentityToken(mstrSession, mstrIdentityToken) -> None:
    """sets the identity token to be used in subsequent requests

    Args:
        mstrSession (Session): the requests.Session object to be used with subsequent requests to the MSTR REST API
        mstrIdentityToken (str): the identity token to be used in subsequent requests, note that mstrio-py requests require identity token, not the auth token
    """    
    mstrSession.headers.update({'X-MSTR-IdentityToken': mstrIdentityToken})


def runDocument(mstrSession: Session, rsdId) -> Response:
    """Runs a document / Dossier and returns a Response object with instance ID to be used with subsequent requests

    Args:
        mstrSession (Session): requests.Session object to be used with subsequent requests to the MSTR REST API
        rsdId ([type]): document ID to be run (could be dossier ID, it is the same)

    Raises:
        ValueError: oh noes!

    Returns:
        Response: respone with instance ID
    """
    docIDinstanceEndpoint = mstrRESTendpoints['getRSDinstance'].format(rsdId)
    docInstanceRequest = mstrSession.post(
        mstrSession.baseURL + docIDinstanceEndpoint)
    print(docInstanceRequest.url)
    if docInstanceRequest.ok:
        return docInstanceRequest
    else:
        raise ValueError(docInstanceRequest.text)


def exportToPDF(mstrSession: Session, mstrDocument: Response) -> str:
    """Exports the document to PDF format via API

    Args:
        mstrSession (Session): requests.Session object to be used with subsequent requests to the MSTR REST API
        mstrDocument (Response): Response object from runDocument() - contains the document instances string

    Raises:
        NameError: stuff went horribly wrong 

    Returns:
        str: base64 encoded PDF string
    """

    if mstrDocument.ok:
        d = dict()
        d.update(**mstrDocument.json())
        pdfinstance = '/' + d['mid'] + '/pdf'
        return mstrSession.post(mstrDocument.url + pdfinstance)
    else:
        raise NameError('document retrieval failed')


def getIdentityToken(mstrSession: Session) -> str:
    """Returns the identity token

    Args:
        mstrSession (Session): requests.Session object to be used with subsequent requests to the MSTR REST API

    Raises:
        ValueError: stuff did not work

    Returns:
        str: identity token
    """
    identityEndpoint = mstrRESTendpoints['identityToken']
    identityRequest = mstrSession.post(mstrSession.baseURL + identityEndpoint)
    if identityRequest.ok:
        indentityToken = identityRequest.headers.get('X-MSTR-IdentityToken')
        print(indentityToken)

        return indentityToken
    else:
        raise ValueError(identityRequest.text)
