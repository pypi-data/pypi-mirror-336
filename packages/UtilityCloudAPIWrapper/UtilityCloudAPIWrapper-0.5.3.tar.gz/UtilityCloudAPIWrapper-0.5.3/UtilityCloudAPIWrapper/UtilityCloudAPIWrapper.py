"""
UtilityCloudAPIWrapper.py

Python wrapper for the utility cloud API

"""
from os import makedirs, remove
from os.path import join, isfile, abspath, isdir
# noinspection SpellCheckingInspection
from json import load as jload, dump as jdump, dumps as jdumps, JSONDecodeError
from logging import Logger
from configparser import ConfigParser
import getpass

import requests

# this is how these modules should be imported to function properly as a PyPI module
import BetterConfigAJM as BetterConfig
import PurgeSecrets
from EasyLoggerAJM import EasyLogger


IMPORT_WARNING_MSG = 'module could not be imported with full path, trying different import method'

try:
    from UCWrapBetterConfig.UCWrapBetterConfig import UCWrapBetterConfig
except (ImportError, ModuleNotFoundError) as e:
    print(IMPORT_WARNING_MSG)
    try:
        from UCWrapBetterConfig import UCWrapBetterConfig
    except (ImportError, ModuleNotFoundError) as e:
        raise e


try:
    from UtilityCloudAPIWrapper.UCAPIErr import *
except (ImportError, ModuleNotFoundError) as e:
    print(IMPORT_WARNING_MSG)
    try:
        from UCAPIErr import *
    except (ImportError, ModuleNotFoundError) as e:
        raise e

module_name = __file__.rsplit('\\', maxsplit=1)[-1].split(".")[0]

base_url_default = "https://api.ucld.us/env/prd/"


class EasyReq:
    TOO_MANY_REQUESTS_REASON = "Too many requests sent too quickly"
    VALID_REQUEST_METHODS = ["GET", "POST"]

    def __init__(self, logger: Logger = None, fail_http_400s: bool = True):
        self._fail_http_400s = fail_http_400s
        self._logger = logger if logger else Logger("Dummy_logger")

    def make_request(self, method: str, url: str, headers: dict, payload) -> requests.Response:
        self._validate_request_method(method)
        try:
            response = requests.request(method, url, headers=headers, data=payload)
            return self._handle_response(response)
        except requests.RequestException as e:
            self._logger.error(e, exc_info=True)
            raise

    def _validate_request_method(self, method: str):
        if method.upper() not in self.VALID_REQUEST_METHODS:
            valid_methods = ", ".join(self.VALID_REQUEST_METHODS)
            raise InvalidRequestMethod(
                f"{method} is not a valid request method (Options are: {valid_methods})"
            )

    def _handle_response(self, response: requests.Response) -> requests.Response:
        if response.ok:
            return response
        if response.status_code == 429:
            response.reason = self.TOO_MANY_REQUESTS_REASON
        return self._process_error_response(response)

    def _process_error_response(self, response: requests.Response) -> requests.Response:
        try:
            error_message = self._extract_error_message(response)
            raise requests.RequestException(f"Response was {response.status_code} {response.reason}, "
                                            f"with message: {error_message}")
        except requests.RequestException as e:
            self._logger.error(e, exc_info=True)
            if not self._fail_http_400s and response.status_code in {403, 401}:
                self._logger.warning(
                    f"Response code {response.status_code} returned. Returning response for further processing.")
                return response
            raise e

    @staticmethod
    def _extract_error_message(response: requests.Response) -> str:
        try:
            return response.json().get('message', '').split('Authorization=')[0]
        except JSONDecodeError:
            return response.text.split('Authorization=')[0]


# noinspection SpellCheckingInspection
class _UtilityCloudAuth:
    CONFIG_SUFFIXES = ['cfg', 'config', 'ini']
    VALID_KEY_FILETYPES = ['json', 'config']
    DEFAULT_KEY_FORMAT = VALID_KEY_FILETYPES[0]
    AUTH_BASE_URL = "https://ucld.us/"
    EMAIL_REGEX = r'^[\w-]+@([\w-]+\.)+[\w-]{2,4}$'
    EXPIRED_ERROR_CODES = ['401', '403']

    def __init__(self, logger=None, key_dirpath=None, chosen_keyfile_format=None, **kwargs):
        self.auth = None
        self.auto_auth = kwargs.get('auto_auth', False)
        self.auth_initialized = False
        self.use_config = kwargs.get('use_config', False)
        self._auth_runtype_default = kwargs.get('auth_runtype_default')
        self._auth_credentials = kwargs.get('auth_credentials')

        self.user_email_suffix = kwargs.get('user_email_suffix')
        self.check_purge = kwargs.get('check_purge', False)
        self.purge_all = kwargs.get('purge_all', False)

        self._key_dirpath = key_dirpath
        self._auth_key_filename = 'auth_key'
        self._current_keyfile_format = chosen_keyfile_format or self.DEFAULT_KEY_FORMAT

        self._logger = logger or Logger("DUMMY_LOGGER")
        self.ER = EasyReq(logger=self._logger, fail_http_400s=True)

        self.config = self._process_kwargs_and_get_config(kwargs)
        self._setup_key_dirpath(key_dirpath)

        if self.auto_auth:
            self._logger.debug("auto_auth is enabled. Running authentication...")
            self.auth, self.auth_initialized = self.RunAuth()
        else:
            self._logger.info("Authentication needs to be run manually or enable auto_auth.")

    def _process_kwargs_and_get_config(self, kwargs):
        if kwargs:
            self._logger.info("__init__ kwargs detected")
            self._make_key_dirpath = kwargs.get('make_key_dirpath', True)
            if 'config' in kwargs:
                return self._validate_config(kwargs['config'])
        return None

    def _setup_key_dirpath(self, key_dirpath):
        if self.config and self.use_config:
            self._key_dirpath = self.config["AUTH"].get("key_dirpath", key_dirpath)
        elif self._key_dirpath is None:
            raise InvalidConfigError(
                "Key directory path (`key_dirpath`) must be set or specified in the config."
            )
        self._key_dirpath_check()

    def _validate_config(self, config):
        if isinstance(config, BetterConfig.BetterConfigAJM):
            self._logger.info("Config validated with BetterConfig.")
            return config.GetConfig()
        if isinstance(config, ConfigParser):
            self._logger.info("Config validated with ConfigParser.")
            return config
        else:
            raise InvalidConfigError("Config must be an instance of ConfigParser or BetterConfig.")

    def expired_auth_del(self, e):
        """
        deletes the auth key if it is expired, this is determined by the error passed in.
        :param e: Exception raised during API request
        :type e: Exception
        :return: None
        :rtype: None
        """
        if any(code in e.args[0] for code in self.EXPIRED_ERROR_CODES):
            auth_key_path = join(self.config['AUTH']['key_dirpath'], f"{self._auth_key_filename}.json").replace('\\',
                                                                                                                '/')
            warning_message = f"Auth key likely expired. Deleting {auth_key_path}, retry authentication."
            self._logger.warning(warning_message)
            remove(auth_key_path)
            raise RequestException(warning_message) from None
        self._logger.error(e, exc_info=True)
        raise e

    def RunAuth(self):
        self._logger.info("Attempting to initialize Auth...")
        if self._auth_runtype_default:
            cred_args = {'runtype': self._auth_runtype_default,
                         'credentials': self._auth_credentials} if self._auth_credentials else {
                'runtype': self._auth_runtype_default}
            self.auth = self._InitAuth(**cred_args)
        else:
            self.auth = self._InitAuth()

        if self.auth:
            self.auth_initialized = True
            self._logger.info("Authentication initialized successfully.")
        return self.auth, self.auth_initialized

    def _get_uc_login(self, **kwargs):
        def _email_check(candidate):
            import re
            email_pattern = re.compile(self.EMAIL_REGEX)
            res = re.fullmatch(email_pattern, candidate)
            return res

        def _get_user_loop():
            while True:
                user = input("UC Username: ")
                if user:
                    if self.user_email_suffix:
                        if not user.endswith(self.user_email_suffix):
                            user = user + self.user_email_suffix
                            return user
                    elif not self.user_email_suffix and not _email_check(user):
                        try:
                            raise InvalidUtilityCloudUserName("Invalid username format, please use your full email!")
                        except InvalidUtilityCloudUserName as e:
                            print(e)
                            self._logger.warning(e, exc_info=True)
                    if _email_check(user):
                        return user

        def _get_pass_loop():
            print(f"username: {user}")
            while True:
                password = getpass.getpass("Password: ")
                if password:
                    return password

        user = None
        password = None
        override_config_to_edit = False

        if kwargs:
            self._logger.debug("kwargs used in _get_uc_login.")
            if 'override_config_to_edit' in kwargs:
                override_config_to_edit = kwargs['override_config_to_edit']

        if not self.use_config or not self.config["AUTH"]["user"]:
            user = _get_user_loop()

        # if not self.use_config OR IF OVERRIDE_CONFIG_TO_EDIT IS TRUE
        if not self.use_config or override_config_to_edit:
            if not user:
                user = self.config['AUTH']["user"]
            else:
                self.config["AUTH"]["user"] = user
            password = _get_pass_loop()
            if password:
                if self.use_config:
                    self.config['AUTH']["password"] = password
                    user = self.config['AUTH']["user"]
                    if hasattr(self.config, "config_location"):
                        with open(self.config.config_location, 'w') as f:
                            self.config.write(f)
                    else:
                        self._logger.warning("Config could not be written to "
                                             "since there is no config.config_location parameter.")

        if self.use_config and not override_config_to_edit:
            if self.config and self.use_config:
                if not user:
                    user = self.config['AUTH']["user"]
                self.config["AUTH"]['user'] = user
                if self.user_email_suffix is not None and self.config['AUTH']["user"].endswith(self.user_email_suffix):
                    pass
                else:
                    if not user:
                        user = self.config['AUTH']["user"] + self.user_email_suffix
                try:
                    if not self.config['AUTH']["password"] or self.config['AUTH']["password"] == '':
                        self._get_uc_login(override_config_to_edit=True)
                    password = self.config['AUTH']["password"]
                except KeyError as e:
                    self._get_uc_login(override_config_to_edit=True)
                    password = self.config['AUTH']["password"]

            else:
                try:
                    raise MissingConfigError("self.Config must be set in order to use config file.")
                except MissingConfigError as e:
                    self._logger.error(e, exc_info=True)
                    raise e

        if user and password:
            return user, password
        else:
            try:
                raise AttributeError("Both user and password cannot be None.")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e

    def _InitAuth(self, **kwargs):
        def _runtype_read_logic():
            self._logger.info("attempting to read auth key")
            if (self.full_keypath.endswith("json") or
                    [x for x in self.CONFIG_SUFFIXES if self._full_keypath.endswith(x)]):
                if isfile(self.full_keypath):
                    self._logger.info(f"{self.full_keypath} detected, reading.")
                    self.auth = self.ReadAuth(self._full_keypath)
                else:
                    self._logger.info(f"{self.full_keypath} not detected, attempting to request new auth.")
                    user, password = self._get_uc_login(use_config=self.use_config)
                    self.auth = self.ReqNewAuth(username=user, password=password)
            else:
                try:
                    raise FileNotFoundError(f"{self.full_keypath} could not be found.")
                except FileNotFoundError as e:
                    self._logger.error(e, exc_info=True)
                    raise e
            return self.auth

        def _runtype_req_logic():
            self._logger.info("requesting new auth key")
            if 'username' in credentials.keys() and 'password' in credentials.keys():
                self._logger.info("logging in with credentials")
                self.auth = self.ReqNewAuth(credentials['username'], credentials['password'])
            else:
                self._logger.info("logging in with credentials")
                user, password = self._get_uc_login(use_config=self.use_config)
                self.auth = self.ReqNewAuth(user, password)
            return self.auth

        runtype = None
        credentials = None
        if kwargs:
            if 'runtype' in kwargs or runtype is not None:
                runtype = kwargs['runtype']
                if runtype not in ['read', 'req_new']:
                    try:
                        raise AttributeError('runtype attribute not recognized')
                    except AttributeError as e:
                        self._logger.error(e, exc_info=True)
                        raise e
            else:
                try:
                    raise AttributeError('runtype attribute not given!')
                except AttributeError as e:
                    self._logger.error(e, exc_info=True)
                    raise e

            if 'credentials' in kwargs and isinstance(kwargs['credentials'], dict):
                credentials = kwargs['credentials']
            else:
                if runtype == 'read':
                    pass
                else:
                    try:
                        raise AttributeError(f'Credentials needed for runtype {runtype}')
                    except AttributeError as e:
                        self._logger.error(e, exc_info=True)
                        raise e

        self._logger.info(f"runtype detected as {runtype or 'runtype is None'}")

        if runtype == 'read':
            self.auth = _runtype_read_logic()

        elif runtype == 'req_new':
            self.auth = _runtype_req_logic()

        elif not runtype:
            self._logger.info("no runtype detected, defaulting to \'read\' mode.")
            self.auth = _runtype_read_logic()
        return self.auth

    def _key_dirpath_check(self):
        try:
            if not isdir(self._key_dirpath) and self._make_key_dirpath:
                makedirs(self._key_dirpath)
                self._logger.info(f"{self._key_dirpath} created.")
            elif isdir(self._key_dirpath):
                self._logger.info(f"{self._key_dirpath} detected.")
                pass
            else:
                try:
                    raise NotADirectoryError(f"{self._key_dirpath} does not exist, "
                                             f"and self._make_key_dirpath kwarg is set to false")
                except NotADirectoryError as e:
                    self._logger.error(e, exc_info=True)
                    raise e
        except TypeError as e:
            try:
                raise ValueError(f"_key_dirpath is {self._key_dirpath}, this folder cannot be created. "
                                 f"Please use the key_dirpath attribute if key_dirpath "
                                 f"is not part of your config file.") from None
            except ValueError as e:
                self._logger.error(e, exc_info=True)
                raise e

    @property
    def key_dirpath(self):
        return self._key_dirpath

    @key_dirpath.setter
    def key_dirpath(self, value):
        self._key_dirpath = value

    @property
    def full_keypath(self):
        self._full_keypath = (join(self.key_dirpath, self._auth_key_filename).replace("\\", "/")
                              + '.' + self._current_keyfile_format)
        return self._full_keypath

    def ReadAuth(self, key_path=None):
        def _load_auth(f_obj):
            if abspath(f_obj.name).split('.')[-1].lower() == 'json':
                loaded = jload(fp=f_obj)
                l_auth = eval(jdumps(loaded, indent=4))
                l_auth = l_auth['auth']
            elif abspath(f_obj.name).split('.')[-1].lower() in self.CONFIG_SUFFIXES:
                # TODO: implement this
                try:
                    raise NotImplementedError("config is not implemented yet.")
                except NotImplementedError as e:
                    self._logger.error(e, exc_info=True)
                    raise e
            else:
                l_auth = f_obj.read()
            return l_auth

        if key_path:
            if isfile(key_path):
                with open(key_path) as f:
                    auth = _load_auth(f)
            else:
                user, password = self._get_uc_login(use_config=self.use_config)
                auth = self.ReqNewAuth(username=user, password=password)

        else:
            if isfile(self.full_keypath):
                if (not abspath(self.full_keypath).split('.')[-1]
                        or abspath(self.full_keypath).split('.')[-1] not in self.VALID_KEY_FILETYPES):
                    with open(self.full_keypath) as f:
                        auth = _load_auth(f)
                else:
                    with open(self.full_keypath) as f:
                        auth = _load_auth(f)
            else:
                try:
                    raise FileNotFoundError("keypath file not found, try running ReqNewAuth method.")
                except FileNotFoundError as e:
                    self._logger.error(e, exc_info=True)
                    raise e
        return auth

    def ReqNewAuth(self, username: str, password: str, ):
        self._logger.info("Getting authentication token...")
        auth_url = join(self.AUTH_BASE_URL, "api/authentication").replace("\\", "/")

        payload = jdumps({
            "UserName": username,
            "Password": password
        })
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json'
        }

        res = self.ER.make_request("POST", auth_url, headers, payload)

        auth = res.text

        self._WriteAuthToFile(file_type=self._current_keyfile_format, auth=auth)
        self._logger.info("Auth received, returning auth.")
        return auth

    def _WriteAuthToFile(self, file_type: str, auth: str = None, **kwargs):
        pw = None
        user = None

        if kwargs:
            if 'password' in kwargs:
                pw = kwargs['password']
            if 'username' in kwargs:
                user = kwargs['username']

        if file_type not in self.VALID_KEY_FILETYPES:
            try:
                raise AttributeError(f"File type is not valid, use {self.VALID_KEY_FILETYPES}")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e
        if auth:
            if self.full_keypath:
                pass
            with open(self.full_keypath, 'w') as f:
                if file_type == 'json':
                    auth_dict = {'auth': auth}
                    # this is where the auth file is written
                    jdump(obj=auth_dict, fp=f, indent=4)
                elif file_type == 'config':
                    try:
                        raise NotImplementedError("config portion is still in progress.")
                    except NotImplementedError as e:
                        self._logger.error(e, exc_info=True)
                        raise e
        else:
            if user and pw:
                auth = self.ReqNewAuth(password=pw, username=user)
                self._WriteAuthToFile('json', auth=auth)
            else:
                try:
                    raise AttributeError("User and password are required  if no auth is supplied.")
                except AttributeError as e:
                    self._logger.error(e, exc_info=True)
                    raise e

    def PurgeAuthkey(self, purge_age_minutes: int = 30, **kwargs):
        confirm_purge = kwargs.get('confirm_purge', True)

        PS = PurgeSecrets.PurgeSecrets(logger=self._logger, purge_age_minutes=purge_age_minutes)
        PS.confirm_purge = confirm_purge
        if PS.IsExpired(filepath=self._full_keypath):
            PS.PurgeFile()

    def PurgeAll(self, config_section_to_purge='AUTH',
                 config_fields_to_purge: list or None = None,
                 purge_age_minutes: int = 30, **kwargs):
        confirm_purge = True
        if kwargs:
            if 'confirm_purge' in kwargs:
                confirm_purge = kwargs['confirm_purge']

        if config_fields_to_purge is None:
            config_fields_to_purge = ['user', 'password']
        PS = PurgeSecrets.PurgeSecrets(logger=self._logger, purge_age_minutes=purge_age_minutes)
        PS.confirm_purge = confirm_purge
        PS.TotalPurge(self.config, self.config.config_location,
                      config_section_to_purge, config_fields_to_purge, filepath=self._full_keypath)


# noinspection SpellCheckingInspection
class UtilityCloudAPIWrapper(_UtilityCloudAuth):
    def __init__(self, base_url: str, logger: Logger = None, **kwargs):
        if logger:
            self._logger = logger
        else:
            self._logger = EasyLogger(project_name=kwargs.get('logger_project_name', module_name),
                                      log_spec=kwargs.get('log_spec', 'hourly')).logger

        self.base_url = base_url

        if hasattr(self, 'config') and self.config:
            self.init_config()
        else:
            self.config = UCWrapBetterConfig(config_dir="../cfg",
                                             config_filename=kwargs.get('config_filename',
                                                                        f"{module_name}ConfigAJM.ini"))

            self.config.GetConfig()
            self.init_config()

        kwargs['config'] = self.config

        super().__init__(self._logger, **kwargs)

        self.base_headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Authorization': self.auth
        }
        self.base_query = {
            "page": 1,
            "itemCount": "10",
            "search": "",
            "SearchFacets": "",
            "orderby": None,
            "isAdvanced": True,
            "filters": None,
            "isactive": True,
            "facets": ""
        }

        self.account_id_dict = self._GetAssignedAccounts()
        self.valid_asset_search_facets = self._GetAssetBasicFilterSearchFacetsList()

    def init_config(self):
        self.config['DEFAULT']['base_url'] = self.base_url
        self._logger.info("Attempting to write base_url to config...")
        if hasattr(self.config, "config_location"):
            with open(self.config.config_location, 'w') as f:
                self._logger.debug(f"Writing Config to {self.config.config_location}")
                self.config.write(fp=f)
        else:
            self._logger.warning("Config could not be written to "
                                 "since there is no config.config_location parameter.")

    def _check_auth(self):
        if not self.auth_initialized:
            try:
                raise AuthenticationError("self.RunAuth must be run before making requests.")
            except AuthenticationError as e:
                self._logger.error(e, exc_info=True)
                raise e
        else:
            self.base_headers['Authorization'] = self.auth
            return

    def GetWorkOrderDetails(self, **kwargs):
        def _GetIDLoop():
            while True:
                wo_id = input("Please enter workorder ID: ")
                if wo_id.isnumeric():
                    return wo_id
                else:
                    pass

        self._check_auth()
        # TODO: generalize this down to else: work_order_id - _GetIDLoop()
        print_response = False
        payload = {}
        if kwargs:
            if 'workorderid' in kwargs:
                if isinstance(kwargs['workorderid'], int) or kwargs['workorderid'].isnumeric():
                    work_order_id = kwargs['workorderid']
                else:
                    try:
                        raise AttributeError("Work Order ID can contain numbers only.")
                    except AttributeError as e:
                        self._logger.error(e, exc_info=True)
                        raise e
            else:
                work_order_id = _GetIDLoop()

            if 'print_response' in kwargs:
                print_response = kwargs['print_response']
        else:
            work_order_id = _GetIDLoop()

        if work_order_id:
            wod_url = f"workorder?workorderid={work_order_id}"
            url = self.base_url + wod_url
            res = self.ER.make_request("GET", url, headers=self.base_headers, payload=payload)
            if print_response:
                print(jdumps(res.json(), indent=4))
        else:
            try:
                raise AttributeError("work_order_id cannot be None")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e

    def QueryWorkOrders(self, search_query: str = '', **kwargs):
        try:
            raise NotImplementedError("non functional, see TODOs/fixmes")
        except NotImplementedError as e:
            self._logger.error(e, exc_info=True)
            raise e
        self._check_auth()
        print_response = False
        query_url = self.base_url + "workorder/getworkorders"
        if kwargs:
            if 'query_dict' in kwargs:
                query_dict = kwargs['query_dict']
            else:
                query_dict = self.base_query
            if 'print_response' in kwargs:
                print_response = kwargs['print_response']
        else:
            query_dict = self.base_query
        # TODO: figure out how this works
        query_dict['Search'] = search_query
        # TODO: figure out why this times out. maybe needs a search query?
        query_dict['ItemCount'] = '1'
        res = self.ER.make_request(method="post", url=query_url, headers=self.base_headers, payload=jdumps(query_dict))
        if print_response:
            print(jdumps(res.json(), indent=4))
        return res.json()

    def GetAssetsSearch(self, facets_string: str, **kwargs):
        self._check_auth()

        print_results = False
        item_count = None
        page = None
        search_url = self.base_url + "asset/getassets"
        search_type = None
        self.base_query['facets'] = facets_string

        if kwargs:
            if 'search_type' in kwargs:
                search_type = kwargs['search_type'].lower()
                if search_type in ['id', 'detail']:
                    self._logger.info(f'search_type kwarg {search_type} being used')
                    pass
                else:
                    try:
                        raise AttributeError("the search_type kwarg must be either \'id\' or \'detail\'")
                    except AttributeError as e:
                        self._logger.error(e, exc_info=True)
                        raise e

            if 'search_url' in kwargs:
                if search_type is not None:
                    self._logger.warning("search_type is also given, search_url will be ignored.")
                search_url = kwargs['search_url']

            if 'print_results' in kwargs:
                print_results = kwargs['print_results']
            if 'item_count' in kwargs:
                item_count = kwargs['item_count']
            if 'page' in kwargs:
                page = kwargs['page']

        real_id_search_url = 'https://wc.ucld.us/api/AssetSearchController/read'
        detail_search_url = 'https://wc.ucld.us/api/AssetDetailsController/GET_ASSET_DETAILS'

        if search_type == 'id':
            search_url = real_id_search_url
        elif search_type == 'detail' and 'assetId' in self.base_query.keys():
            search_url = detail_search_url
        elif search_type == 'detail' and 'assetId' not in self.base_query.keys():
            try:
                raise AttributeError('\'assetId\' not found in self.base_query')
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e
        print(search_url)

        if item_count:
            self.base_query['ItemCount'] = str(item_count)
        if page:
            self.base_query['page'] = page

        res = self.ER.make_request("POST", search_url, headers=self.base_headers, payload=jdumps(self.base_query))

        if print_results:
            print(jdumps(res.json(), indent=4))
        if search_type == 'id':
            return res.json()['data'][0]['id']
        return res.json()

    def _GetAssetBasicFilterSearchFacetsList(self, **kwargs):
        self._check_auth()

        print_response = False
        payload = {}
        if kwargs:
            if 'print_response' in kwargs:
                print_response = kwargs['print_response']
        url = self.base_url + "asset/basicfilters"
        res = self.ER.make_request("get", url, self.base_headers, payload)
        if res.text == '' or res.text == {}:
            res = None
            return res
        if print_response:
            print(jdumps(res.json(), indent=4))
        return res.json()

    def GetAssetByID(self, **kwargs):
        def _GetIDLoop():
            while True:
                asset_id = input("Please enter Asset ID: ")
                if asset_id:  # .isnumeric():
                    return asset_id
                else:
                    pass

        try:
            raise NotImplementedError("non functional, see TODOs/fixmes")
        except NotImplementedError as e:
            self._logger.error(e, exc_info=True)
            raise e
        self._check_auth()

        print_response = False
        payload = {}
        if kwargs:
            if 'assetid' in kwargs:
                if isinstance(kwargs['assetid'], int) or kwargs['assetid'].isnumeric():
                    asset_id = kwargs['assetid']
                else:
                    try:
                        raise AttributeError("Asset ID can contain numbers only.")
                    except AttributeError as e:
                        self._logger.error(e, exc_info=True)
                        raise e
            else:
                asset_id = _GetIDLoop()

            if 'print_response' in kwargs:
                print_response = kwargs['print_response']
        else:
            asset_id = _GetIDLoop()
        if asset_id:
            asset_url = f"api/asset/getassetbyid?assetid={asset_id}"
            url = self.base_url + asset_url
            # FIXME: this still doesnt seem to work
            get_asset_headers = {**self.base_headers, **{'Credential': '', 'Signature': '',
                                                         'SignedHeaders': '', 'Date': ''}}
            res = self.ER.make_request("GET", url, get_asset_headers, payload=payload)
            if print_response:
                try:
                    print(jdumps(res.json(), indent=4))
                except requests.exceptions.JSONDecodeError as e:
                    self._logger.warning(e)
                    print(res.text)
        else:
            try:
                raise AttributeError("asset_id cannot be None")
            except AttributeError as e:
                self._logger.error(e, exc_info=True)
                raise e
        return res.json()

    def _GetAssignedAccounts(self, **kwargs):
        self._check_auth()
        payload = {}
        print_response = kwargs.get('print_response', False)

        url = self.base_url + 'account/getaccounts'
        res = self.ER.make_request("GET", url, self.base_headers, payload)
        if res.text == '' or res.text == {}:
            res = None
            return res
        if print_response:
            print(jdumps(res.json(), indent=4))
        return res.json()

    def GetAssetClassByAccount(self, **kwargs):
        def _GetIDLoop():
            while True:
                acc_id = input("Please enter Account ID: ")
                if acc_id:
                    return acc_id
                else:
                    pass

        self._check_auth()

        payload = {}
        account_id = kwargs.get('accountid', _GetIDLoop())
        print_response = kwargs.get('print_results', False)

        account_url = self.base_url + f'assetclass/getassetclassbyaccount?accountkey={account_id}'
        res = self.ER.make_request("get", account_url, self.base_headers, payload)

        if print_response:
            print(jdumps(res.json(), indent=4))
        return res.json()


def initialize_uc_wrapper(config=None, logger=None, **kwargs):
    """
    :param config: Configuration object containing base URL for API requests.
    :type config: ConfigParser
    :param logger: Logger object for logging messages.
    :type logger: Logger
    :param kwargs: Additional keyword arguments to be passed to UtilityCloudAPIWrapper initialization.
    :return: Instance of UtilityCloudAPIWrapper initialized with provided configurations.
    :rtype: UtilityCloudAPIWrapper
    """
    if config and config.has_option('DEFAULT', 'base_url'):
        return UtilityCloudAPIWrapper(base_url=config['DEFAULT']['base_url'],
                                      logger=logger, config=config,
                                      use_config=True, auto_auth=True, **kwargs)
    elif config and not config.has_option('DEFAULT', 'base_url'):
        return UtilityCloudAPIWrapper(base_url=base_url_default,
                                      logger=logger, config=config, use_config=True,
                                      auto_auth=True, key_dirpath="../Misc_Project_Files", **kwargs)
    else:
        return UtilityCloudAPIWrapper(base_url=base_url_default,
                                      logger=logger, config=config, use_config=True,
                                      auto_auth=True, key_dirpath="../Misc_Project_Files", **kwargs)


if __name__ == '__main__':
    uc = initialize_uc_wrapper(check_purge=True)

    uc.GetWorkOrderDetails(print_response=True, workorderid=273391818)
    # uc.check_purge = True
    # uc.purge_all = True
    # defaults to False

    if uc.purge_all:
        uc.PurgeAll()
    elif uc.check_purge:
        uc.PurgeAuthkey()

# workorder ID
# 273391818

# permit asset id - this seems to be for any and all permits?
# 836790301
