""" Our Asynchronously Interchangeable Objects Data Structures

"""
import dataclasses
import datetime

from ast import literal_eval
from dataclasses import dataclass, field
from typing import Any, Mapping, MutableMapping, Optional, Sequence

from ae.base import NOW_STR_FORMAT, now_str, defuse                                             # type: ignore


__version__ = '0.3.12'


# oaio access right values, also used to sort the username lists (to place the oaio creator in the first list item)
CREATE_ACCESS_RIGHT = 'C'           #: create, delete and update rights, see access_right field in Pubz and Userz
DELETE_ACCESS_RIGHT = 'D'           #: delete and update rights
UPDATE_ACCESS_RIGHT = 'U'           #: only update rights
READ_ACCESS_RIGHT = 'r'             #: read-only access
NO_ACCESS_RIGHT = 'x'               #: no or not yet granted access right (not valid for Pubz.access_right)
ACCESS_RIGHTS = (CREATE_ACCESS_RIGHT, DELETE_ACCESS_RIGHT, READ_ACCESS_RIGHT, UPDATE_ACCESS_RIGHT)
""" access rights (stored in the access_right db column of the Pubz table). access right names and their translations
are provided, using the text prefix 'access_right' followed by an underscore and the access right character, in the
optional loc/*/Msg*.txt files provided by the :mod:`ae.i18n` portion """

DELETE_ACTION = 'delete'            #: object got deleted, not used in Logz.action field (records get deleted instead)
DOWNLOAD_ACTION = 'download'        #: object got downloaded/synced
REGISTER_ACTION = 'register'        #: oaio got registered
UPLOAD_ACTION = 'upload'            #: object got uploaded/updated
LOG_DB_ACTIONS = (REGISTER_ACTION, UPLOAD_ACTION, DOWNLOAD_ACTION)  #: see Logz.action field
LOG_ACTIONS = LOG_DB_ACTIONS + (DELETE_ACTION, )
UPDATE_ACTIONS = (REGISTER_ACTION, UPLOAD_ACTION)

NAME_VALUES_KEY = '_name'           #: oaio values key of optional object name
ROOT_VALUES_KEY = '_root_path'      #: oaio values key of optional files root path
FILES_VALUES_KEY = '_file_paths'    #: oaio values key of paths list of optional files attached to an oaio

OBJECTS_DIR = 'objz'                #: name of folder to store infos of oai objects not yet synced with server
FILES_DIR = 'filez'                 #: name of folder to store file names attached to an oaio

HTTP_HEADER_USR_ID = 'X-OAIO-user'  #: user name
HTTP_HEADER_APP_ID = 'X-OAIO-app'   #: app id
HTTP_HEADER_DVC_ID = 'X-OAIO-dvc'   #: device id

MAX_STAMP_DIFF = 69.0               #: maximum accepted UTC time difference in seconds between client and server
OLDEST_SYNC_STAMP = '20221231111111012345'      #: oldest complete stamp ("" is even older)
STAMP_FORMAT = NOW_STR_FORMAT.format(sep="")    #: stamp format string


now_stamp = now_str                 #: function alias used to create a new oaio stamp


ActionType = str                    #: register/upload/download... action type

OaioAccessRightType = str           #: oaio access rights (:attr:`oaio_server.oapi.models.Pubz.access_right`)
OaioAppIdType = str                 #: app id
OaioCshIdType = str                 #: cloud storage host id
OaioCtxType = Mapping[str, str]     #: dict-like mapping keeping the oaio-specific http header field names and values
OaioDeviceIdType = str              #: device id
OaioDictType = dict[str, Any]       #: type of oai object converted into a dictionary
OaioFilesType = Sequence[str]       #: item type of the :data:`FILES_VALUES_KEY` within :attr:`OaiObject.client_values`
OaioIdType = str                    #: oai object id
OaioRootPathType = str              #: default root path (containing :data:`~ae.paths.PATH_PLACEHOLDERS`)
OaioStampType = str                 #: oaio stamp
OaioUserIdType = str                #: Userz.Uid/auth.User.username
OaioValuesType = dict[str, Any]     #: oaio client_values and server_values


@dataclass
class OaiObject:
    """ oaio data types and structures """
    oaio_id: OaioIdType

    client_stamp: OaioStampType = ''                                #: timestamp of register or newest upload
    server_stamp: OaioStampType = ''                                #: timestamp of previous version

    client_values: OaioValuesType = field(default_factory=dict)     #: actual object values
    server_values: OaioValuesType = field(default_factory=dict)     #: previous object values (for debugging/monitoring)

    csh_id: Optional[OaioCshIdType] = None                          #: cloud storage host id (for attached file/folders)
    username: OaioUserIdType = ''                                   #: name of the actual user
    device_id: OaioDeviceIdType = ''                                #: id of the actual device
    app_id: OaioAppIdType = ''                                      #: id of the actual application
    csh_access_right: OaioAccessRightType = ''                      #: csh+values access right of the actual user


OaioMapType = MutableMapping[OaioIdType, OaiObject]


# *************************  helpers  ************************************************************


def context_encode(user_name: OaioUserIdType, device_id: OaioDeviceIdType, app_id: OaioAppIdType = '') -> OaioCtxType:
    """ encode the extra http header context fields with user/device/app ids as ASCII/latin1 byte literals.

    :param user_name:           id of the user.
    :param device_id:           id of the client device.
    :param app_id:              id of the app.
    :return:                    mapping with http header context field names/values (each of them with Unicode chars
                                will be encoded as UTF8-byte-value-literal using only ASCII/latin-1 characters).
    """
    return {
        HTTP_HEADER_USR_ID: repr(user_name.encode()),
        HTTP_HEADER_DVC_ID: repr(device_id.encode()),
        HTTP_HEADER_APP_ID: repr(app_id.encode()),
        }


def context_decode(header: OaioCtxType) -> tuple[OaioUserIdType, OaioDeviceIdType, OaioAppIdType]:
    """ decode and return the request/session http header context fields containing user/device/app ids.

    :param header:              mapping with http header fields and values, having at least the extra context fields
                                with the user/device/app ids.
    :return:                    tuple with the decoded user/device/app ids.
    """
    # noinspection PyTypeChecker
    return tuple(literal_eval(header[_]).decode() for _ in (HTTP_HEADER_USR_ID, HTTP_HEADER_DVC_ID, HTTP_HEADER_APP_ID))


def object_dict(oai_obj: OaiObject) -> OaioDictType:
    """ convert OaiObject dataclass instance into the corresponding mapping/dict object.

    :param oai_obj:             oai object to convert.
    :return:                    converted dict object.
    """
    # Pycharm bug https://youtrack.jetbrains.com/issue/PY-76070
    # noinspection PyTypeChecker
    return dataclasses.asdict(oai_obj)


def object_id(user_name: OaioUserIdType, device_id: OaioDeviceIdType, app_id: OaioAppIdType,
              stamp: OaioStampType, values: OaioValuesType) -> OaioIdType:
    """ generate object id (of type OaioIdType) from the specified arguments.

    :param user_name:           username of the object creator/registrar.
    :param device_id:           id of the device from where the object get registered.
    :param app_id:              id of the registering application.
    :param stamp:               timestamp when the object got registered.
    :param values:              values of the object.
    :return:                    oai object id (can be used as file name on most OS).
    :raises:                    AssertionError if one of the following arguments is empty:
                                :paramref:`object_id.user_name`, :paramref:`object_id.device_id`,
                                :paramref:`object_id.app_id` or :paramref:`object_id.stamp`.
    """
    assert user_name and device_id and app_id and stamp, f"empty {user_name=} {device_id=} {app_id=} {stamp=}"
    obj_url = f'{app_id}://{user_name}@{device_id}'

    if NAME_VALUES_KEY in values:
        obj_url += '/' + values[NAME_VALUES_KEY]
    elif ROOT_VALUES_KEY in values:
        obj_url += '/' + values[ROOT_VALUES_KEY].strip('/')     # remove leading/trailing path separator character
    elif len(values.get(FILES_VALUES_KEY, [])) == 1:
        obj_url += '/' + values[FILES_VALUES_KEY][0]

    obj_url += '/' + stamp

    return defuse(obj_url)


def stamp_diff(stamp1: OaioStampType, stamp2: OaioStampType) -> float:
    """ determine the difference in seconds between the two specified stamps in the format %Y%m%d%H%M%S%f.

    :param stamp1:              time stamp string 1 (return positive seconds value if older than stamp2).
    :param stamp2:              time stamp string 2.
    :return:                    float with the difference in seconds between both specified stamps (stamp2 - stamp1).
    """
    parser = datetime.datetime.strptime
    return (parser(stamp2, STAMP_FORMAT) - parser(stamp1, STAMP_FORMAT)).total_seconds()
