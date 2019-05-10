# Ricky Galliani
# Minerva
# security.py

from src.robinhood_holding import RobinhoodHolding

import json

class Security:

    def __init__(self,
                 security_id,
                 name=None,
                 price=None,
                 quantity=None,
                 holdings=None):
        self.id = security_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.holdings = holdings

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        sec = { 'id': self.id }
        if self.name:
            sec['name'] = self.name
        if self.price:
            sec['price'] = self.price
        if self.quantity:
            sec['quantity'] = self.quantity
        if self.holdings:
            sec['holdings'] = self.holdings
        return sec

    def with_cents(self):
        """
        Returns this Security but with dollar amounts represented in cents,
        not dollars.
        """
        return Security(
            self.id,
            self.name,
            int(self.price * 100),
            self.quantity,
            self.holdings
        )

    def update(self, robinhood_holding):
        """
        Updates this security with given Robinhood holding data.
        """
        assert(isinstance(robinhood_holding, RobinhoodHolding))
        self.name = robinhood_holding.name
        self.price = robinhood_holding.price
        self.quantity = robinhood_holding.quantity
        self.holdings = robinhood_holding.equity
