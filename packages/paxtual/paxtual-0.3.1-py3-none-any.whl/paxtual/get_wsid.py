import socket

def get_workstation_id():
    hostname = socket.gethostname()
    workstationMap = {'L-5CG0035QJ4': 'Eval2', 'L-5CG012F4P7': 'Config3', 'L-5CG9437NPP': 'Config2', 'L-5CG9258BPB': 'Config1'}
    try:
        return workstationMap.get(hostname)
    except KeyError:
        workStationId = "unidentfiedWS"
        return workStationId