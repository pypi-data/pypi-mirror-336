from pigmento import pnt


class A:
    def __init__(self):
        pnt.set_display_mode(use_instance_class=True, display_method_name=False, display_class_name=True)

    @staticmethod
    def call():
        pnt('hello')
