import suds
import functools

from config import load_default_config

class TRTHApi(object):
    """
    A Pythonic wrapper for the TRTH Api
    WSDL interface.

    """

    def __init__(self):
        self._config = None
        self._factory = None
        self._client = None

    def setup(self, config=None):
        """
        Setups up the TRTH Api object. This must be
        called prior to using the Api object.

        """

        # Load config.
        self._config = config or load_default_config()

        # Setup WSDL objects.
        self._client = suds.client.Client(self._config.get_wsdl_url())
        self._factory = TypeFactory(self._client)

        # Set authentication credentials.
        username, password = self._config.get_credentials()
        self._client.set_options(
                soapheaders=(
                    self._factory.create('CredentialsHeader',
                                         username=username,
                                         password=password)
                )
        )
        self._valid_methods = self._client.sd[0].ports[0][0].methods.keys()
        self._valid_types = [typedef[0].name for typedef in self._client.sd[0].types]

    def __getattr__(self, name):
        """
        Proxies method calls to the WSDL service and
        type constructors to the type factory.

        """
        assert self._client and self._factory

        if name in self._valid_methods:
            return getattr(self._client.service, name)
        elif name in self._valid_types:
            return functools.partial(self._factory.create, name)
        else:
            raise AttributeError
    
class TypeFactory(object):
    NAMESPACE = 'ns0'
    TYPE_DEFAULTS = {
        'Instrument' : {
            'status' : None,
        }
    }

    ARRAY_MAP = {
        'Instrument' : ('ArrayOfInstrument', 'instrument'),
    }

    def __init__(self, client):
        self._client = client

    def create(self, typename, **kwargs):
        instance = self._client.factory.create('%s:%s' % (self.NAMESPACE, typename))
        # Use default args if available and merge with explicit kwargs.
        arguments = dict(self.TYPE_DEFAULTS.get(typename, {}))
        arguments.update(kwargs)

        for (k, v) in arguments.iteritems():
            setattr(instance, k, v)
        return instance

    def create_array(self, name, items):
        assert name in self.ARRAY_MAP, '%s has no valid array type.' % (name,)
        typename, containerattr = self.ARRAY_MAP[name]
        instance = self.create(typename)
        setattr(instance, containerattr, items)
        return instance
