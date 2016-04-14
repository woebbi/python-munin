# Cork - Authentication module for the Bottle web framework
# Copyright (C) 2013 Federico Ceratto and others, see AUTHORS file.
# Released under LGPLv3+ license, see LICENSE.txt

"""
.. module:: json_backend
   :synopsis: JSON file-based storage backend.
"""

from logging import getLogger
import os
import shutil
import sys

try:
    import json
except ImportError:  # pragma: no cover
    import simplejson as json


class BackendIOException(Exception):
    """Generic Backend I/O Exception"""
    pass

is_py3 = (sys.version_info.major == 3)

log = getLogger(__name__)

try:
    dict.iteritems
    py23dict = dict
except AttributeError:
    class py23dict(dict):
        iteritems = dict.items


class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_py3 and isinstance(obj, bytes):
            return obj.decode()

        return json.JSONEncoder.default(self, obj)


class JsonBackend(object):
    """JSON file-based storage backend."""

    def __init__(self, fname='errors', initialize=False):
        """Data storage class. Handles JSON files

        :param users_fname: users file name (without .json)
        :type users_fname: str.
        :param roles_fname: roles file name (without .json)
        :type roles_fname: str.
        :param pending_reg_fname: pending registrations file name (without .json)
        :type pending_reg_fname: str.
        :param initialize: create empty JSON files (defaults to False)
        :type initialize: bool.
        """
        self.errors = py23dict()
        self._fname = fname
        self._mtimes = py23dict()
        if initialize:
            self._initialize_storage()

    def _loadjson(self, fname, dest):
        """Load JSON file located under self._directory, if needed

        :param fname: short file name (without path and .json)
        :type fname: str.
        :param dest: destination
        :type dest: dict
        """
        try:
            fname = "%s.json" % (fname)
            mtime = os.stat(fname).st_mtime

            if self._mtimes.get(fname, 0) == mtime:
                # no need to reload the file: the mtime has not been changed
                return

            with open(fname) as f:
                json_data = f.read()
        except Exception as e:
            raise BackendIOException("Unable to read json file %s: %s" % (fname, e))

        try:
            json_obj = json.loads(json_data)
            dest.clear()
            dest.update(json_obj)
            self._mtimes[fname] = os.stat(fname).st_mtime
        except Exception as e:
            raise BackendIOException("Unable to parse JSON data from %s: %s" \
                % (fname, e))

    def _savejson(self, fname, obj):
        """Save obj in JSON format in a file in self._directory"""
        fname = "%s.json" % (fname)
        try:
            with open("%s.tmp" % fname, 'w') as f:
                json.dump(obj, f, cls=BytesEncoder)
                f.flush()
            shutil.move("%s.tmp" % fname, fname)
        except Exception as e:
            raise BackendIOException("Unable to save JSON file %s: %s" \
                % (fname, e))

    def save_errors(self):
        """Save users in a JSON file"""
        self._savejson(self._fname, self.errors)

    def _store(self, dct, backend, obj, name):
        try:
            dct[backend] = getattr(obj, name)
        except AttributeError:
            self.remove_backend(backend)
            return False
        return True

    def error(self, error_name):
        """Existing user

        :returns: User() instance if the user exist, None otherwise
        """
        # print("ALL ERRORS: {}".format(self.errors))
        # if not error_name and error_name in self.errors:
        #     print("Come : {} Error: {}".format(error_name, Errors(error_name, self)))
        return Errors(error_name, self)
        # return None

    def update_error(self, nerror, ntime, ncounted):
        error = self.error(nerror)
        print("--Error: {}".format(error))
        if error is None:
            raise AAAException("Nonexistent error.")

        if ntime is None or not ntime:
            ntime = ntime

        if ncounted is not 0:
            ncounted = ncounted

        error.update(error=nerror, time=ntime, counted=ncounted)


class AAAException(Exception):
    """Generic Authentication/Authorization Exception"""
    pass


class Errors(object):

    def __init__(self, error_name, cork_obj, session=None):
        """Represent an authenticated user, exposing useful attributes:
        email_addr, role, level, description, email_addr, session_creation_time,
        session_accessed_time, session_id. The session-related attributes are
        available for the current user only.

        :param email_addr: email_addr
        :type email_addr: str.
        :param cork_obj: instance of :class:`Cork`
        """
        self.errors = JsonBackend(fname='errors', initialize=False)
        self._cork = cork_obj
        assert error_name in self.errors, "Unknown error"
        self.error_name = error_name
        error = self._cork.errors[error_name]
        self.time = error['time']
        self.counted = error['counted']

        if session is not None:
            try:
                self.session_creation_time = session['_creation_time']
                self.session_accessed_time = session['_accessed_time']
                self.session_id = session['_id']
            except:
                pass

    def update(self, error, time=None, counted=0):
        """Update an user account data

        :param role: change user role, if specified
        :type role: str.
        :param pwd: change user password, if specified
        :type pwd: str.
        :param email_addr: change user email address, if specified
        :type email_addr: str.
        :raises: AAAException on nonexistent user or role.
        """
        # error = self.error
        # if error not in self._cork.errors:
        #     raise AAAException("Error does not exist.")

        if time is not None:
            self._cork.errors[error]['time'] = time

        if counted > 0:
            self._cork.errors[error]['counted'] = counted

        self._cork.save_errors()

    def delete(self):
        """Delete user account

        :raises: AAAException on nonexistent user.
        """
        try:
            self._cork.errors.pop(self.error)
        except KeyError:
            raise AAAException("Nonexistent user.")
        self._cork.save_errors()
