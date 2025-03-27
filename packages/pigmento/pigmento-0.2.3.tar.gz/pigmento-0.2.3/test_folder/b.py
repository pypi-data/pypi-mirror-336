from pigmento import pnt
from test_folder.a import A


class B(A):
    @staticmethod
    def ask():
        pnt('world')
