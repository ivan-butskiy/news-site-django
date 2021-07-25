# Конвенционально так принято называть модуль, содержащий миксины
class MyMixin(object):
    mixin_prob = ''

    def get_prob(self):
        return self.mixin_prob.upper()

    def get_upper(self, s):
        return s.upper()
