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
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '6', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '9', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '12', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '15', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '18', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '21', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '24', '-repeater_delay_multiplier', '1']),
        ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '27', '-repeater_delay_multiplier', '1']),
        ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '33', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '36', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '39', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '42', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '45', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '48', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '51', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '54', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '57', '-repeater_delay_multiplier', '1']),
        # ('exp2_repeaters_sf_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '60', '-repeater_delay_multiplier', '1'])
        
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use executor.map to parallelize the execution of run_script
        results = executor.map(lambda x: run_script(*x), script_args_list)

        # Print the results
        for result in results:
            print(result)
