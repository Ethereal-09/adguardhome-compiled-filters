import unittest
from unittest.mock import patch, MagicMock

import dns_utils as app


class RuleTests(unittest.TestCase):
    def test_semantics(self):
        self.assertEqual(app.parse_line('0.0.0.0 a.example.com b.example.com'), ['|a.example.com|', '|b.example.com|'])
        self.assertEqual(app.parse_line('example.com'), ['|example.com|'])
        self.assertEqual(app.parse_line('example.com##.ad'), [app.UNSUPPORTED])
        self.assertEqual(app.parse_line('||example.com^$important'), ['||example.com^$important'])
        self.assertEqual(app.parse_line('||example.com/path^'), [app.UNSUPPORTED])
        self.assertEqual(app.parse_line('127.0.0.1'), [app.UNSUPPORTED])

    def test_html_rejected(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.url = 'https://test.example/rules'
        response.read.return_value = b'<html>Error</html>'
        with patch.object(app, 'urlopen', return_value=response):
            with self.assertRaisesRegex(ValueError, 'HTML'):
                app.fetch(response.url, 1, 1)

    def test_partial_http_and_truncated_body_are_rejected(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.url = 'https://test.example/rules'
        response.getcode.return_value = 206
        with patch.object(app, 'urlopen', return_value=response):
            with self.assertRaisesRegex(ValueError, 'HTTP response'):
                app.fetch(response.url, 1, 1)
        response.getcode.return_value = 200
        response.headers.get.return_value = '999'
        response.read.return_value = b'||ads.example^'
        with patch.object(app, 'urlopen', return_value=response):
            with self.assertRaisesRegex(ValueError, 'Truncated response'):
                app.fetch(response.url, 1, 1)
        response.headers.get.return_value = None
        response.read.return_value = b'! |Count: 500 rules!\n||ads.example^\n'
        with patch.object(app, 'urlopen', return_value=response):
            with self.assertRaisesRegex(ValueError, 'header declares'):
                app.fetch(response.url, 1, 1)

    def test_entries_header_detects_incomplete_source_even_with_matching_http_length(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.url = 'https://test.example/rules'
        response.getcode.return_value = 200
        for newline in (b'\n', b'\r\n'):
            with self.subTest(newline=newline):
                body = newline.join((b'! Entries: 1,000', b'||ads.example^', b'||partial'))
                response.headers.get.return_value = str(len(body))
                response.read.return_value = body
                with patch.object(app, 'urlopen', return_value=response):
                    with self.assertRaisesRegex(ValueError, 'header declares 1000'):
                        app.fetch(response.url, 1, 1)

        # The header counts raw entries, including unsupported DNS syntax.
        body = b'! Entries: 3\n||ads.example^\n||invalid_name.example^\n@@||safe.example^\n'
        response.headers.get.return_value = str(len(body))
        response.read.return_value = body
        with patch.object(app, 'urlopen', return_value=response):
            self.assertEqual(app.fetch(response.url, 1, 1), body.decode())


if __name__ == '__main__':
    unittest.main()
