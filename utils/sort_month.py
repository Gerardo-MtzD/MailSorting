def sort_month(month: str) -> str:
    if len(month) < 2:
        month = f"0{month}"
    if month == '01':
        control_name = '01-Enero'
    elif month == '02':
        control_name = '02-Febrero'
    elif month == '03':
        control_name = '03-Marzo'
    elif month == '04':
        control_name = '04-Abril'
    elif month == '05':
        control_name = '05-Mayo'
    elif month == '06':
        control_name = '06-Junio'
    elif month == '07':
        control_name = '07-Julio'
    elif month == '08':
        control_name = '08-Agosto'
    elif month == '09':
        control_name = '09-Septiembre'
    elif month == '10':
        control_name = '10-Octubre'
    elif month == '11':
        control_name = '11-Noviembre'
    elif month == '12':
        control_name = '12-Diciembre'
    else:
        raise Exception
    return control_name