class Car:
    def __init__(self, make, model, color, msrp, quantity, mpg=-1, horsepower=-1):
        self.make = make
        self.model = model
        self.color = color
        self.msrp = msrp
        self.mpg = mpg
        self.horsepower = horsepower
        self.quantity = quantity

    @staticmethod
    def from_dict(source):
        # TODO: Implement from_dict

    def to_dict(self):
        # TODO: Implement to_dict

    def __repr__(self):
        repr = f"Car(\
                make={self.make}, \
                model={self.model}, \
                color={self.color}, \
                msrp={self.msrp}"
        if self.mpg != -1:
          repr += f", mpg={self.mpg}"
        if self.horsepower != -1:
          repr += f", horsepower={self.horsepower}"
        repr += f", quantity={self.quantity})"
        return repr