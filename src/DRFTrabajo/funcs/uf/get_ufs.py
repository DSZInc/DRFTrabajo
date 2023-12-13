from calendar import monthrange
from datetime import date
from datetime import timedelta

def get_ufs(last_uf_known_date: date, last_uf_value: float, new_ipc: float) -> dict[date, float]:
    day=last_uf_known_date
    month_days=monthrange(day.year,day.month)[1] #Calcula la cantidad de dias a proyectar
    UFs={day:last_uf_value} #Se crea el diccionario con el valor diario de la UF
    while day != (last_uf_known_date + timedelta(days=month_days)): #Finaliza el 9 del siguiente mes
        day= day + timedelta(days=1) #Avanza un dia hacia adelante
        uf=round(last_uf_value*(1+new_ipc)**(((day-last_uf_known_date).days)/month_days),2) #Calcula la UF del dia 
        UFs.update({day:uf}) #Guarda el nuevo dia y su UF en el diccionario
    return(UFs)