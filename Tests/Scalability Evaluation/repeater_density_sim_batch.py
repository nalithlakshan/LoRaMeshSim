import concurrent.futures
import subprocess

def run_script(script_filename, script_args):
    try:
        command = ['python', script_filename] + script_args
        result = subprocess.run(command, check=True, capture_output=True)
        return f"Output of {script_filename} with arguments {script_args}:\n{result.stdout.decode()}"
    except subprocess.CalledProcessError as e:
        return f"Error executing {script_filename} with arguments {script_args}: {e}"

if __name__ == "__main__":
    # List of tuples: (script filename, script arguments)
    script_args_list = [
        ('repeater_density_sim.py',['1', '1']),
        ('repeater_density_sim.py',['1', '2']),
        ('repeater_density_sim.py',['1', '3']),
        ('repeater_density_sim.py',['1', '4']),
        ('repeater_density_sim.py',['1', '5']),
        ('repeater_density_sim.py',['1', '6']),
        ('repeater_density_sim.py',['1', '7']),
        ('repeater_density_sim.py',['1', '8']),
        ('repeater_density_sim.py',['1', '9']),
        ('repeater_density_sim.py',['2', '1']),
        ('repeater_density_sim.py',['2', '2']),
        ('repeater_density_sim.py',['2', '3']),
        ('repeater_density_sim.py',['2', '4']),
        ('repeater_density_sim.py',['2', '5']),
        ('repeater_density_sim.py',['2', '6']),
        ('repeater_density_sim.py',['2', '7']),
        ('repeater_density_sim.py',['2', '8']),
        ('repeater_density_sim.py',['2', '9']),
        ('repeater_density_sim.py',['3', '1']),
        ('repeater_density_sim.py',['3', '2']),
        ('repeater_density_sim.py',['3', '3']),
        ('repeater_density_sim.py',['3', '4']),
        ('repeater_density_sim.py',['3', '5']),
        ('repeater_density_sim.py',['3', '6']),
        ('repeater_density_sim.py',['3', '7']),
        ('repeater_density_sim.py',['3', '8']),
        ('repeater_density_sim.py',['3', '9'])
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use executor.map to parallelize the execution of run_script
        results = executor.map(lambda x: run_script(*x), script_args_list)

        # Print the results
        for result in results:
            print(result)
