#
# This source file is part of the firestore open source project.
#
# Copyright 2016-present Workenvoy Inc. and contributing firestore authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import socket
from google.cloud import firestore


GOOGLE_PUBLIC_DNS_A = "8.8.8.8"
GOOGLE_PUBLIC_DNS_TCP_PORT = 53
TIMEOUT = 3


db = firestore.Client()


_connection = {}
_connections = {}
_databases = {}


def is_online(host=GOOGLE_PUBLIC_DNS_A, port=GOOGLE_PUBLIC_DNS_TCP_PORT, timeout=TIMEOUT):
    """
    Check if this machine is online as to determine if it is necessary to save to fs
    simulating cloud firestore
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as e:
        # log(e) depending on logging preferences
        return False
    """
    pass


def connect(certificate):
    """
    Connect to the firestore cloud database using GCP provided certificate as a .json file
    or a dictionary containing parsed contents of the file.
    :param certificate: A path to the certificate file or the contents of the certificate as a dictionary
    :return:
    """
    pass
