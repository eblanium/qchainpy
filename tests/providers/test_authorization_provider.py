import os
import unittest
from pathlib import Path

from src.qchainpy.providers.authorization_provider import AuthorizationProvider


class TestAPMethods(unittest.TestCase):
    def setUp(self):
        key_path = os.path.join(Path(__file__).resolve().parent.parent, 'keys/private.key')
        passphrase = None
        self.ap = AuthorizationProvider(
            key_path=key_path,
            passphrase=passphrase
        )

    def test_sign(self):
        data = {
            'account': '22',
            'signdata': {
                'account': '22'
            }
        }
        sign = self.ap.get_sign(data)
        self.assertEqual(
            sign,
            'eFpj0rPIyb1VTzOEhY9bRna94UuSS89cpi9RznNUfV0rPHwZ15epv-LavglphHjYNm-QOzXj-tTUrJA6sRB6vWibgf2YI6Ly-pCgUSopQz_Vr7-X_7E9WvDM5ItUPb0erYBHsxLj7HpEFUI7mY5jNUDxxXOgOaEfpzmR4VdSu_RxzCWXq7KhQwvxitY9a0RpRH3b2fD131HvzDQXXzuluHtBjpKW2rsuzxgaABEQOCDqHLmHuPRYQsLvS8ELfNAAkj0Ga3f3zWeld6s_VbJZOST1Yp-WY61o4NnWoZ1_OfVsrcVFlduDCvX4tyQp3Rw6Xq42wMM2080vw_ColkH7ng'
        )


if __name__ == '__main__':
    unittest.main()
