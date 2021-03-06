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


class ConnectionError(Exception):
    """
    Error raised when connection to firestore could not be established
    """

    def __init__(self, *args, **kwargs):
        super(ConnectionError, self).__init__(args, kwargs)
        try:
            msg = args[0]
        except IndexError:
            msg = "Unfortunately we could not connect to the firestore cloud database service"
        self.message = msg
