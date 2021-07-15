import pickle
import unittest

from betfairlightweight import exceptions


class ExceptionsTest(unittest.TestCase):
    def test_betfair_error(self):
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.BetfairError("test")
        # pickle
        error = exceptions.PasswordError("test")
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_password_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.PasswordError("test")
        # pickle
        error = exceptions.PasswordError("test")
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_app_key_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.AppKeyError("test")
        # pickle
        error = exceptions.AppKeyError("test")
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_certs_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.CertsError("test")
        # pickle
        error = exceptions.CertsError("test")
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_status_code_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.StatusCodeError("test")
        # pickle
        error = exceptions.StatusCodeError("test")
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_invalid_response_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.InvalidResponse({})
        # pickle
        error = exceptions.InvalidResponse({})
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_login_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.LoginError({})
        # pickle
        error = exceptions.LoginError({})
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_keep_alive_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.KeepAliveError({})
        # pickle
        error = exceptions.KeepAliveError({})
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_api_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.APIError({}, "test", {})
        # pickle
        error = exceptions.APIError({}, "test", {})
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_logout_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.LogoutError({})
        # pickle
        error = exceptions.LogoutError({})
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_socket_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.SocketError("test")
        # pickle
        error = exceptions.SocketError("test")
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_listener_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.ListenerError("test", "test")
        # pickle
        error = exceptions.ListenerError("test", "test")
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_cache_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.CacheError("test")
        # pickle
        error = exceptions.CacheError("test")
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )

    def test_race_card_error(self):
        # raise
        with self.assertRaises(exceptions.BetfairError):
            raise exceptions.RaceCardError("test")
        # pickle
        error = exceptions.RaceCardError("test")
        self.assertEqual(
            str(pickle.loads(pickle.dumps(error))),
            str(error),
        )
