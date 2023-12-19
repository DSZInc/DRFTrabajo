## this is file just for testing

from src.DRFTrabajo.FixedIncome import CLBond, FixedCoupon
from datetime import date


coupon = FixedCoupon(100,6,0,date(2023,12,1),date(2024,12,1))

coupons = [coupon]

bono_zero_cupon = CLBond(coupons)

value = bono_zero_cupon.get_value(1000000,5, date(2023,12,19))

print(value)
print(bono_zero_cupon.get_present_value(1000000,5, date(2023,12,19)))