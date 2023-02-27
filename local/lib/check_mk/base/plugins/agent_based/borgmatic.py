from .agent_based_api.v1 import *
from datetime import datetime

def discover_borgmatic(section):
    yield Service()

def check_borgmatic_age(params, section):
    age = int(section[0][0])
    warn = int(params['age'][0])
    crit = int(params['age'][1])
    dt = datetime.fromtimestamp(age)
    if age < warn:
        if age < crit:
            yield Result(state=State.CRIT, summary="Backup way too old. Last backup: {}".format(dt.strftime("%Y-%m-%d %H:%M:%S")))
        else:
            yield Result(state=State.WARN, summary="Backup too old. Last backup: {}".format(dt.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        yield Result(state=State.OK, summary="Backups ok. Last backup: {}".format(dt.strftime("%Y-%m-%d %H:%M:%S")))

register.check_plugin(
    name = "borgmatic_backup",
    service_name = "Borgmatic backup",
    discovery_function = discover_borgmatic,
    check_function = check_borgmatic_age,
    check_default_parameters={"age": (108000, 172800)},
    check_ruleset_name="borgmatic",
)

def parse_borgmatic(string_table):
    return string_table

register.agent_section(
    name = "borgmatic_backup",
    parse_function = parse_borgmatic,
)
