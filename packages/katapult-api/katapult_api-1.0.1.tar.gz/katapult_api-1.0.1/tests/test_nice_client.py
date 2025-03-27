import unittest
from katapult_api.katapult_nice import KatapultNice

class TestKatapultNice(unittest.TestCase):
    def test_clean_attributes(self):
        raw = {
            'GLC_(Circumference)': {'-Imported': '35'},
            'MR_type': {'-O9W7MEsTfq34ZZ3nxlp': 'Comm Rearrangement'},
            'PoleNumber': {'assessment': 'H14C484'},
            'communication_attachers': {
                '-O9PewIv8WtONnP0DtBo': {
                    'communication_type': 'CATV',
                    'joint_use_attacher_list': 'COMCAST CABLE'
                }
            },
            'done': {'-Imported': False},
            'field_completed': {'button_added': True, 'value': True},
            'grounded': {'-Imported': False},
            'grounding': {'assessment': 'Not Grounded'},
            'internal_note': {'auto_note': 'Node copied from Training_1014PA04_01'},
            'job_name': {'-Imported': '1014PA_PSA_314_MASTER'},
            'measured_attachments': {'-Imported': True},
            'mr_note': {
                '-O9W7Kd_tZCdgFY06AFl': 'lowered previous comms, detach comm anchor from pnm and have at least 5\' of space between comm anchors and pnm'
            },
            'mr_state': {'auto_calced': 'MR Resolved'},
            'node_type': {'-Imported': 'pole'},
            'photo_classified': {'-Imported': True},
            'pole_tag': {'-Imported': {'company': '', 'owner': False, 'tagtext': ''}},
            'scid': {'auto_button': '004'},
            'substation': {'-Imported': ''},
            'time_bucket': {
                '-O9Pm8hhO9Jj2eCQ0Wvf': {
                    'start': 1729173373276,
                    'stop': 1729173691328,
                    'uid': 'zBWTdVpgwoV1aBvZkXzc1uRfEXo2'
                },
                '-O9Pm9BaaFF_nAGqpaHX': {
                    'createdBy': '-NBNKVxx4eYYniFHrpXT',
                    'start': 1729173691328,
                    'stop': 1729173693306,
                    'uid': 'zBWTdVpgwoV1aBvZkXzc1uRfEXo2'
                },
                '-O9PmDqTj-mtPsXV7lGb': {
                    'start': 1729173693306,
                    'stop': 1729173712369,
                    'uid': 'zBWTdVpgwoV1aBvZkXzc1uRfEXo2'
                }
            }
        }

        clean = {
            'GLC_(Circumference)': '35',
            'MR_type': 'Comm Rearrangement',
            'PoleNumber': 'H14C484',
            'communication_attachers': {
                'communication_type': 'CATV',
                'joint_use_attacher_list': 'COMCAST CABLE'
            },
            'done': False,
            'field_completed': {'button_added': True, 'value': True},
            'grounded': False,
            'grounding': 'Not Grounded',
            'internal_note': 'Node copied from Training_1014PA04_01',
            'job_name': '1014PA_PSA_314_MASTER',
            'measured_attachments': True,
            'mr_note': 'lowered previous comms, detach comm anchor from pnm and have at least 5\' of space between comm anchors and pnm',
            'mr_state': 'MR Resolved',
            'node_type': 'pole',
            'photo_classified': True,
            'pole_tag': {'company': '', 'owner': False, 'tagtext': ''},
            'scid': '004',
            'substation': '',
            'time_bucket': {
                '-O9Pm8hhO9Jj2eCQ0Wvf': {
                    'start': 1729173373276,
                    'stop': 1729173691328,
                    'uid': 'zBWTdVpgwoV1aBvZkXzc1uRfEXo2'
                },
                '-O9Pm9BaaFF_nAGqpaHX': {
                    'createdBy': '-NBNKVxx4eYYniFHrpXT',
                    'start': 1729173691328,
                    'stop': 1729173693306,
                    'uid': 'zBWTdVpgwoV1aBvZkXzc1uRfEXo2'
                },
                '-O9PmDqTj-mtPsXV7lGb': {
                    'start': 1729173693306,
                    'stop': 1729173712369,
                    'uid': 'zBWTdVpgwoV1aBvZkXzc1uRfEXo2'
                }
            }
        }

        katapult_nice = KatapultNice('test')
        self.assertEqual(clean, katapult_nice.clean_attributes(raw))

if __name__ == '__main__':
    unittest.main()