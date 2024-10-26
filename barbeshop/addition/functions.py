from datetime import datetime, timedelta
    
def time_plus_time(first_time: str, last_time: str):
    time_format = "%H:%M"
    time1 = datetime.strptime(first_time, time_format)
    time2 = datetime.strptime(last_time, time_format)

    delta1 = timedelta(hours=time1.hour, minutes=time1.minute)
    delta2 = timedelta(hours=time2.hour, minutes=time2.minute)
    result_delta = delta1 + delta2
    hours, remainder = divmod(result_delta.seconds, 3600)
    minutes = remainder // 60
    return f"{hours:02}:{minutes:02}"