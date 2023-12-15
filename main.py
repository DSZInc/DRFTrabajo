from src.DRFTrabajo.FixedIncome import CLBond, FixedCoupon
from datetime import date


coupondate=date(2023, 12, 15)
startdate = date(2023, 1, 1)

a = (coupondate - startdate).days

zero_coupon = [FixedCoupon(amortization=100, interest=5, residual=100, coupondate=date(2023, 12, 15), startdate=date(2023, 1, 1))]

bono_zero = CLBond(coupons=zero_coupon)

valor_bono = bono_zero.get_value(notional=100000,fecha=date(2023, 6, 1), rate=0.05)

print(bono_zero.get_dv01(10000000, 0.05,date(2023, 6, 1)))
