# Ricky Galliani
# Hanna
# src/holdingclass Security:

import json


class Holding:

    def __init__(self, security, num_shares, value):
        if num_shares <= 0:
            raise Exception(
                "Holding must be instantiated with a positive number of shares"
            )
        if value <= 0:
            raise Exception(
                "Holding must be instantiated with a positive value"
            )
        self.__security = security
        self.__num_shares = num_shares
        self.__value = value

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_security(self):
        return self.__security

    def get_num_shares(self):
        return self.__num_shares

    def get_value(self):
        return self.__value

    def set_num_shares(self, num_shares):
        self.__num_shares = num_shares

    def set_value(self, value):
        self.__value = value

    def to_dict(self):
        return {
            'security': self.get_security().to_dict(),
            'num_shares': self.get_num_shares(),
            'value': self.get_value()
        }

    def add(self, other_holding):
        """
        Buys the specified quantity of this holding at the specified price,
        updating the state of this security.
        """
        if self.get_security() != other_holding.get_security():
            raise Exception(
                "Can only add holding of {} to this holding.".format(
                    self.get_security().get_id()
                )
            )
        cur_num_shares = self.get_num_shares()
        other_num_shares = other_holding.get_num_shares()
        cur_value = self.get_value()
        other_value = other_holding.get_value()
        self.set_num_shares(cur_num_shares + other_num_shares)
        self.set_value(cur_value + other_value)
