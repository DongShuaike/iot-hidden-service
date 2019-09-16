"""
The script is try to solve the condition to trigger "telnetd" in
'/home/dsk/Documents/Experiments/firmware/DLink/DAP-1350__1146__Firmware (1.13)
/_dap1350_fw_113.bin.extracted/squashfs-root/usr/bin/system_manager'

In its main function, function "task_loop" is called and it is a very big switch-case
structure, one of its cases is to execute system("telnetd -l /bin/sh &")

The goal is to solve how can we trigger that branch
The address of that block is 0x4056bc
"""
import angr

def getFuncAddress(funcName, plt=None):
    found = [
        addr for addr, func in cfg.kb.functions.items()
        if funcName == func.name and (plt is None or func.is_plt == plt)
    ]
    if len(found) > 0:
        print("Found " + funcName + "'s address at " + hex(found[0]) + "!")
        return found[0]
    else:
        raise Exception("No address found for function : " + funcName)

def getFuncofAddr(addr, functions):
    for func in functions:
        if addr == func[0]:
            return func[1]
    return None

def getReferences2addr(cfg, addr):
    func_node = cfg.get_any_node(addr)
    predecessors = cfg.get_predecessors(func_node)
    return predecessors

proj = angr.Project('/home/dsk/Documents/Experiments/firmware/DLink/DAP-1350__1146__Firmware (1.13)/_dap1350_fw_113.bin.extracted/squashfs-root/usr/bin/system_manager',
                    load_options={'auto_load_libs': True})
cfg = proj.analyses.CFGFast()

start_addr = 0x406388
start_state = proj.factory.blank_state(addr=start_addr)

target_addr = 0x40532c
sm = proj.factory.simulation_manager(start_state, save_unconstrained=True)

sm.explore(find=target_addr)
