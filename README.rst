**Note: This Python package is out of date. The crew at ContinuumIO have put a lot of effort into maintaining their own fork, I'd recommend using their version at https://github.com/ContinuumIO/pytrth.**

pytrth provides a lite wrapper around the Thomson Reuters Tick History (TRTH)
API. A command line tool is provided to assist extraction of options chains.

Thomson Reuters exposes a WSDL service at https://trth-api.thomsonreuters.com/TRTHApi-$VERSION/wsdl/TRTHApi.wsdl where
$VERSION is the current API version. pytrth uses the suds package to access this
service, wrapping API object in Pythonic object where appropriate. The TRTHApi
class in src/api.py wraps this suds interface with an even higher level
interface, greatly easing the creation of TRTH API calls.

Usage
=====

TRTH credentials are read from ~/.trth which should be a YAML file containing the following::

  credentials:
    username: *username*
    password: *password*

You can test your connection to TRTH by requesting the landing speed guide page::
  
  pytrth getpage THOMSONREUTERS


