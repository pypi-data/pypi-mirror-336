# SPDX-License-Identifier: MIT
# Copyright (C) 2025 Avnet
# Authors: Nikola Markovic <nikola.markovic@avnet.com> et al.

import configparser
import datetime
import json
import os
import pathlib
from collections.abc import MutableMapping
from typing import Optional, Tuple

import platformdirs
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID

from . import apiurl, accesstoken

# Environment constants
PF_AZ = "az"
PF_AWS = "aws"
PF_CHOICES = [PF_AWS, PF_AZ]
ENV_POC = "poc"
ENV_PROD = "prod"
ENV_AVNET = "avnet" # this is the UAT Avnet instance name
ENV_CHOICES = [ENV_POC, ENV_PROD, ENV_AVNET]

CONFIG_VERSION = "1.0"  # for future compatibility and potential conversion

SECTION_DEFAULT = 'default'
SECTION_SETTINGS = 'settings'
SECTION_USER = 'user'

# -- BEGIN CONFIGURABLE VALUES --- #

# credentials and environment setup ------
username: Optional[str] = os.environ.get('IOTC_USER') or None  # Recorded in settings for purposes of looking up the current user
pf: Optional[str] = os.environ.get('IOTC_PF') or "aws"
env: Optional[str] = os.environ.get('IOTC_ENV') or "poc"
skey: Optional[str] = os.environ.get('IOTC_SKEY')
access_token: Optional[str] = None
refresh_token = None
token_expiry = 0  # just initialize for "sense" purposes
token_time = 0

# app settings ------
# Note: Never write this setting, only read with os.environ taking precedence:
api_trace_enabled = True if os.environ.get("IOTC_API_TRACE") is not None else False

# -- END CONFIGURABLE VALUES --- #


_cp = configparser.ConfigParser()
_app_config_dir = platformdirs.AppDirs(appname="iotconnect").user_config_dir
_app_config_file = os.path.join(_app_config_dir, "apicfg.ini")
_is_initialized = False

def init() -> None:
    global _is_initialized, api_trace_enabled
    if _is_initialized:
        return
    _is_initialized = True  # we should not attempt to init after the attempt below:
    if not os.path.isdir(_app_config_dir):
        try:
            pathlib.Path(_app_config_dir).mkdir(mode=0o700, parents=True, exist_ok=True)
        except OSError:
            print("Could not create app config directory %s" % _app_config_dir)
            return
    try:
        pathlib.Path(_app_config_file).touch()
        os.chmod(_app_config_file, 0o700)
    except OSError:
        print("Could not write to %s" % _app_config_file)
        return
    # triple check?
    if not os.access(_app_config_file, os.W_OK):
        print("File %s is not Writeable" % _app_config_file)
        return
    _cp.read(_app_config_file)

    # override only if environment variable is not set by manually setting it in config
    if not api_trace_enabled:
        api_trace_enabled = _cp.has_section(SECTION_SETTINGS) and _cp.getboolean(SECTION_SETTINGS, "api_trace")

    section = get_section(SECTION_USER)
    if section.get('access_token') is not None:
        global pf, env, skey, username, access_token, refresh_token, token_time, token_expiry
        pf = section['pf']
        env = section['env']
        skey = section['skey']
        username = section['username']
        access_token = section['access_token']
        refresh_token = section['refresh_token']
        token_time = int(section['token_time'])
        token_expiry = int(section['token_expiry'])

        apiurl.configure_using_discovery()



def is_valid() -> bool:
    return _cp.has_section(SECTION_USER)


def write() -> bool:
    try:
        with open(_app_config_file, 'w') as app_config_file:
            if not _cp.has_section(SECTION_DEFAULT):
                _cp.add_section(SECTION_DEFAULT)
            default = get_section(SECTION_DEFAULT)
            # we may need to parse this version and support a version upgrade in the future.
            default['version'] = CONFIG_VERSION

            global skey, pf, env, access_token, refresh_token, token_time, token_expiry
            section = get_section(SECTION_USER)
            section['username'] = username
            section['pf'] = pf
            section['env'] = env
            section['skey'] = skey
            section['access_token'] = access_token
            section['refresh_token'] = refresh_token
            section['token_time'] = str(round(token_time))
            section['token_expiry'] = str(round(token_expiry))

            # PyCharm seems to get this wrong: Expected type 'SupportsWrite[str]', got 'TextIO' instead
            # noinspection PyTypeChecker
            _cp.write(app_config_file)
        return True
    except OSError:
        print("Could not write to %s" % _app_config_file)
        return False


# user can call this to lazy init section in preparation for read or write of individual section values
def get_section(section: str) -> MutableMapping:
    if not _cp.has_section(section):
        _cp[section] = {}
    return _cp[section]


def is_dedicated_instance() -> bool:
    """ Utility function for determining whether the MQTT ClientID needs to be prefixed with CPID, for example"""

    is_dedicated = accesstoken.decode_access_token().user.isCpidOptional
    if is_dedicated is not None:
        return is_dedicated
    else:
        # temporary workaround for issue https://avnet.iotconnect.io/support-info/2025012718120357
        return pf == PF_AWS and env == ENV_PROD


def get_mqtt_client_id(duid: str) -> str:
    """ If the instance is shared, the DUID needs to be prefixed with CPID to obtain the MQTT Client ID"""
    if is_dedicated_instance():
        return duid
    else:
        return f"{accesstoken.decode_access_token().user.cpId}-{duid}"

def generate_device_json(duid: str, auth_type: int = 2) -> str:
    """
    Generates a config json string that should be written to iotcDeviceConfig.json when running a python SDK
    :param duid: Device Uniqiue ID
    :param auth_type: 2 for Self-signed. 1 for CA-Signed authentication.
    :return:
    """
    device_json = {
        "ver": "2.1",
        "pf": pf,
        "cpid": accesstoken.decode_access_token().user.cpId,
        "env": env,
        "uid": duid,
        "did": get_mqtt_client_id(duid),
        "at": auth_type,
    }
    return json.dumps(device_json, indent=4) + os.linesep


def generate_ec_cert_and_pkey(duid: str, validity_days: int = 3650, curve=ec.SECP256R1()) -> Tuple[str, str]:
    """ Generates an Elliptic Curve private key and a self-signed certificate signed with the private key.
    :param duid: DUID to use for the certificate. For example "my-device-1234". This will be used to compose the Common Name.
    :param validity_days: How many days for the certificate to be valid. Default 10 years.
    :param curve: EC curve to use for the private key. Default is SECP256R1 (prime256v1) curve, as the most widely used.

    :return: Returns a tuple with the private key (first item) and certificate with PEM encoding as bytes.

    """
    private_key = ec.generate_private_key(curve)

    # Create a self-signed certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, get_mqtt_client_id(duid))
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=validity_days)
    ).sign(private_key, hashes.SHA256())

    cert_pem = cert.public_bytes(serialization.Encoding.PEM)
    key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    return key_pem.decode('ascii'), cert_pem.decode('ascii')





# automatically init when loading this module
init()
