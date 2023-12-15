class FixedCoupon:
## clase para cada cupon
## asumimos que además de los parametros pedidos era necesario agregar las fecha de cada cupon
## de lo contrario no podríamos calcular el vp o el dv01 más adelante
    def __init__(self, amortization: float, interest: float, residual: float, coupondate:date, startdate : date):
        self.startdate = startdate
        self.coupondate = coupondate
        self.amortization = float(amortization)
        self.interest = float(interest)
        self.residual = float(residual)
        self.flow = self.amortization+self.interest