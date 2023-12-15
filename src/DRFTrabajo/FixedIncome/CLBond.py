from datetime import date
import numpy as np
from scipy.optimize import fsolve


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

class CLBond:
    def __init__(self, coupons: [FixedCoupon], tera: None): 
        self.coupons =  coupons
        tera = tera
        self.tera = tera if tera is not None else self.set_tera()

    def set_tera(self):
        notional = 100
        start_date = self.coupons[0].startdate

        def objective_function(tera):
            return self.get_value(tera, start_date, notional) - notional

        initial_guess = 0.05

        tera = fsolve(objective_function, initial_guess)[0]

        return tera


    def get_day_count_fraction(self, start_date: date, end_date: date):
        days = (end_date - start_date).days
        return days / 365.0

    def get_value(self, rate: float, initial_date: date, notional: float):
        future_coupons = [coupon for coupon in self.coupons if coupon.coupondate >= initial_date]

        if not future_coupons:
            raise ValueError("No future coupons available for present value calculation.")

        pv = 0
        for i, coupon in enumerate(future_coupons):
            day_count_fraction = self.get_day_count_fraction(initial_date, coupon.coupondate)
            pv += (coupon.flow / (1 + rate ) **day_count_fraction) * notional
        day_count_fraction_last = self.get_day_count_fraction(initial_date, future_coupons[-1].coupondate)
        pv += (future_coupons[-1].residual / (1 + rate ) ** day_count_fraction_last) * notional

        return pv

    def calculate_duration(self, discount_rate: float, initial_date: date, notional: float):
        future_coupons = [coupon for coupon in self.coupons if coupon.coupondate >= initial_date]

        if not future_coupons:
            raise ValueError("No future coupons available for duration calculation.")

        weighted_sum = 0
        pv = self.get_value(discount_rate, initial_date, notional)

        for i, coupon in enumerate(future_coupons):
            day_count_fraction = self.get_day_count_fraction(initial_date, coupon.coupondate)
            weighted_sum += day_count_fraction * (coupon.flow / (1 + discount_rate) ** day_count_fraction) * notional

        day_count_fraction_last = self.get_day_count_fraction(initial_date, future_coupons[-1].coupondate)
        weighted_sum += day_count_fraction_last * (future_coupons[-1].residual / (1 + discount_rate) ** day_count_fraction_last) * notional

        duration = weighted_sum / pv

        return duration

    
    def get_dv01(self, notional: float, rate: float, initial_date: date) ->float:
        duration = self.calculate_duration(rate, initial_date, notional)
        pv = self.get_value(rate, initial_date, notional)
        dv01 = -pv*duration/10000


