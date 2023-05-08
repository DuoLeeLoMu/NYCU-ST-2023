import angr
import sys

EQUATION_CNT = 14
VARIABLE_CNT = 15

main_addr = 0x4011a9
find_addr = 0x401371
avoid_addr = 0x40134d
solve_input = []

class my_scanf(angr.SimProcedure):
    def run(self,fmt,n): 
        simfd = self.state.posix.get_fd(0) 
        data,real_size = simfd.read_data(4) 
        self.state.memory.store(n,data) 
        return 1 

proj = angr.Project('./src/prog', load_options={'auto_load_libs': False})
proj.hook_symbol('__isoc99_scanf', my_scanf(), replace=True)
proj.hook_symbol('printf', angr.SIM_PROCEDURES['stubs']['ReturnUnconstrained'](), replace=True)

state = proj.factory.blank_state(addr=main_addr)

simgr = proj.factory.simulation_manager(state)
simgr.explore(find=find_addr, avoid_addr=avoid_addr)
if simgr.found:
    print(simgr.found[0].posix.dumps(sys.stdin.fileno()))
    data = simgr.found[0].posix.dumps(sys.stdin.fileno())
    for i in range(0, len(data), 4):
        input = data[i:i+4]
        input = int.from_bytes(input, byteorder='little', signed=True)
        solve_input.append(input)
        print(f'x{int(i/4)} : {input}')
else :
    print('Failed')    

with open('solve_input', 'w') as f:
    for a in solve_input:
        f.write(f'{a}\n')