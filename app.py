from spider import spider

from datetime import datetime



def scheduler():
    # Determinar la fecha actual
    hoy = datetime.date.today()
    # hoy = datetime.date(int(hoy.year),int(hoy.month),int(hoy.day))

    # Determinar si hoy es miércoles o domingo
    dia_sorteo = hoy.isoweekday()

    fecha_ini = datetime.date(int(hoy.year), int(hoy.month), 1)
    month_days = monthrange(int(hoy.year), int(hoy.month))[1] # Calcula el número de días de un mes
    fecha_end = datetime.date(int(hoy.year), int(hoy.month), month_days)
    count = 0
    fechas_sorteo_semanal = []

    for d_ord in range(fecha_ini.toordinal(), fecha_end.toordinal()):
        d = date.fromordinal(d_ord)
        if (d.isoweekday() == 3 or d.isoweekday() == 7):
            fechas_sorteo_semanal.append(d)
            count += 1

    validar_fecha_semanal = hoy in fechas_sorteo_semanal

    if (validar_fecha_semanal == True):

        # hoy = datetime.now()
        current_time = hoy.strftime("%H:%M:%S")
        current_date = hoy.strftime("%Y-%m-%d")

        # Trigger scraper function everyday on 12 AM
        if current_time == "02:00:00" and current_date == '2022-02-11': 
            spider()

scheduler()