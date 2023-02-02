
class TotalPriceCounterCls:
    def __init__(self):
        self.total_count = 0

    def total_counter(self, price):
        self.total_count += price
        return self.total_count

total_price_counter = TotalPriceCounterCls()
