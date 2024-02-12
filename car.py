class Car:
    def __init__(self, uuid, make, model, color, msrp, quantity, mpg=-1, horsepower=-1):
        self.uuid = uuid
        self.make = make
        self.model = model
        self.color = color
        self.msrp = msrp
        self.mpg = mpg
        self.horsepower = horsepower
        self.quantity = quantity

    @staticmethod
    def from_dict(source):
       return Car(source['uuid'], source['make'], source['model'], source['color'], source['msrp'], source['quantity'],
                   source.get('mpg', -1), source.get('horsepower', -1))

    def to_dict(self):
      car_dict = {
            'uuid': self.uuid,
            'make': self.make,
            'model': self.model,
            'color': self.color,
            'msrp': self.msrp,
            'quantity': self.quantity,
            'mpg': self.mpg,
            'horsepower': self.horsepower
        }
      return car_dict
       
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