from mstrSAML import MstrSession
from mstrRESTwrapper import *
from helper import *
from mstrio.connection import Connection
# to test if we get proper reply from MSTR
from mstrio import application_objects

# link to library - base endpoint


def main():
    # "https://example.com/MicroStrategyLibrary/"
    base_url = "https://<FQDN:port>/MicroStrategyLibrary/"

    # inititate SAML workflow via browser instance
    # for SSO it is necessary to read profile of the User to read all cockies etc.
    # additionally - it will fail if another browser instance is running with the same profile.
    # get profile folder path from: chrome://version => Profile Path
    # Chrome:
    session = MstrSession(base_url=base_url, timeout=5,
                          user_data_dir=r'C:\Users\spock\AppData\Local\Google\Chrome\User Data')

    # project
    projectID = '7734DE534E611A99DE9F539B633DC862'
    # mstrio connection requires identity token instead of auth token.
    identityToken = getIdentityToken(mstrSession=session)

    # we need to pass this dictionary to Connection class.
    connOptions = dict()
    connOptions['defaultEnvironment'] = base_url
    # we use login mode = 1 even though it is not necessary. It is just a way to get around the fact the SAML is not yet implemented in the MSTR REST API. Since we have auth token, we do not need to really reauthenticate.
    mstrioConnection = Connection(
        base_url=base_url, identity_token=identityToken, login_mode=1, project_id=projectID)

    # lets check all the cubes!
    print(application_objects.list_all_cubes(mstrioConnection))


if __name__ == "__main__":
    main()
