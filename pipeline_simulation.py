from m5.objects import *

# Create the system object
system = System()

# Set clock domain and memory range
system.clk_domain = SrcClockDomain(clock='2GHz', voltage_domain=VoltageDomain())
system.mem_ranges = [AddrRange('512MB')]

# Use DerivO3CPU with SMT (Simultaneous Multithreading) and pipelining
system.cpu = DerivO3CPU()
system.cpu.numThreads = 2  # SMT with 2 threads per core

# Memory bus configuration
system.membus = SystemXBar()

# L1 Instruction Cache configuration
system.l1i_cache = Cache(size='64kB', block_size=64)
system.l1i_cache.cpu_side = system.cpu.icache_port
system.l1i_cache.mem_side = system.membus.master

# L1 Data Cache configuration
system.l1d_cache = Cache(size='64kB', block_size=64)
system.l1d_cache.cpu_side = system.cpu.dcache_port
system.l1d_cache.mem_side = system.membus.master

# Set up CPU system port to the memory bus
system.cpu.icache_port = system.l1i_cache.cpu_side
system.cpu.dcache_port = system.l1d_cache.cpu_side
system.system_port = system.membus.cpu_side_ports

# Create two processes (one per thread)
process1 = Process()
process1.cmd = ['bash', '-c', 'echo "Hello, SMT - Thread 1 with pipeline!"']

process2 = Process()
process2.cmd = ['bash', '-c', 'echo "Hello, SMT - Thread 2 with pipeline!"']

# Assign each process to a thread
system.cpu.workload = [process1, process2]

# Run the simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print("Running SMT with pipeline simulation...")
exit_event = m5.simulate()

print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))
