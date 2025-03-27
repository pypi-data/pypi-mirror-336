import unittest
import json
import tempfile
from ldif2json.cli import parse_ldif, nest_entries

class TestLDIF2JSON(unittest.TestCase):
    def test_parse_ldif(self):
        ldif_data = [
            "dn: cn=test,dc=example\n",
            "objectClass: top\n",
            "objectClass: person\n",
            "cn: test\n",
            "cn: test2\n"
        ]
        result = parse_ldif(ldif_data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['dn'], "cn=test,dc=example")
        self.assertEqual(result[0]['objectClass'], ["top", "person"])
        self.assertEqual(result[0]['cn'], ["test", "test2"])

    def test_nest_entries(self):
        entries = [
            {"dn": "o=example"},
            {"dn": "ou=people,o=example"},
            {"dn": "cn=user,ou=people,o=example"}
        ]
        nested = nest_entries(entries)
        self.assertEqual(len(nested), 1)
        self.assertIn("subEntries", nested[0])
        self.assertEqual(len(nested[0]["subEntries"]), 1)

if __name__ == '__main__':
    unittest.main()
