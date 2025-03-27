# from configparser import ConfigParser
#
# config = ConfigParser()
# config.optionxform = str  # Preserve case sensitivity
# config.read('properties.ini')


class Props:

    # setup.py ---------------------------------------------------------------------------------------------------------
    pip_name = "jainam-pytrade-sdk-test"
    pip_version = "1.0.6"
    setup_author = "Codifi"
    setup_author_email = "periyasamy@codifi.in"
    setup_description = "Python SDK for integrating with Jainam trading platform."
    setup_license = "MIT"
    setup_url = "https://protrade.jainam.in/"
    setup_downloadable_url = "https://github.com/Periyasamy-Dev/jainam_sdk.git"
    setup_apidocs = "https://protrade.jainam.in/apidocs/"


    # tradify.py -------------------------------------------------------------------------------------------------------
    base_url = "https://protrade.jainam.in/"
    api_name = "Codifi API Connect - Python Lib"
    base_url_c = "https://protrade.jainam.in/contract/csv/"

    getSessionData = "omt/auth/sso/vendor/getUserDetails"

    ordExecute = "api/od-rest/orders/execute"
    ordModify = "api/od-rest/orders/modify"
    ordCancel = "api/od-rest/orders/cancel"
    ordGetMargin = "api/od-rest/orders/getmargin"
    getOrderbook = "api/od-rest/info/orderbook"
    getTradebook = "api/od-rest/info/tradebook"
    getOrdHistory = "api/od-rest/info/history"

    getHoldings = "api/ho-rest/holdings/"
    getPositions = "api/po-rest/positions/"
    posConversion = "api/po-rest/positions/conversion"

    getFunds = "api/funds-rest/funds/limits"

    getProfile = "api/client-rest/profile/getclientdetails"