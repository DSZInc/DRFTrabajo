from datetime import date
import numpy as np
from scipy.optimize import fsolve
from .Coupons import FixedCoupon


class CLBond:
    def __init__(self, coupons: [FixedCoupon], **kwargs): 
        self.coupons =  coupons
        tera = kwargs.get('tera', None)
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
        ##actual/365
        days = (end_date - start_date).days
        return days / 365.0

    def get_value(self, notional: float, rate: float, fecha: date):
        future_coupons = [coupon for coupon in self.coupons if coupon.coupondate >= fecha]

        if not future_coupons:
            raise ValueError("No future coupons available for present value calculation.")

        pv = 0
        for i, coupon in enumerate(future_coupons):
            day_count_fraction = self.get_day_count_fraction(fecha, coupon.coupondate)
            pv += (coupon.flow*notional / (1 + rate ) **day_count_fraction) 
        day_count_fraction_last = self.get_day_count_fraction(fecha, future_coupons[-1].coupondate)
        pv += (future_coupons[-1].residual* notional / (1 + rate ) ** day_count_fraction_last) 

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