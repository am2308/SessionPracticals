import sys
from typing import List

def read_input() -> tuple:
    """Read and parse input from STDIN"""
    instance_cpu = int(sys.stdin.readline().strip())
    pod_cpus = list(map(int, sys.stdin.readline().strip().split(',')))
    return instance_cpu, pod_cpus

def schedule_pods(instance_cpu: int, pod_cpus: List[int]) -> List[List[int]]:
    """
    Schedule pods across instances using First-Fit Decreasing algorithm
    Returns list of instance allocations
    """
    # Sort pods in descending order for better packing
    pod_cpus.sort(reverse=True) #  7 6 4 3 1
    
    instances = [] # 7 6 4
    
    for cpu in pod_cpus:
        allocated = False
        
        # Try to fit in existing instances
        for instance in instances:
            if sum(instance) + cpu <= instance_cpu:
                instance.append(cpu)
                allocated = True
                break
                
        # Create new instance if needed
        if not allocated:
            instances.append([cpu])
    print(instances)
    return instances

def main():
    try:
        instance_cpu, pod_cpus = read_input()
        allocations = schedule_pods(instance_cpu, pod_cpus)
        print(allocations)  # Debug: Print allocations for verification
        
        # Format output as specified
        for alloc in allocations:
            print(','.join(map(str, alloc)))
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
