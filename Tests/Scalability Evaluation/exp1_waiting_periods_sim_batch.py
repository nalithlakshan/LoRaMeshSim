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
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '1']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '2']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '3']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '4']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '5']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '6']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '7']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '8']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '9']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '10']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '11']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '12']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '13']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '14']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '15']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '16']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '17']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '18']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '19']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '20']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '21']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '22']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '23']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '24']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '25']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '26']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '27']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '28']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '29']),
        # ('exp1_waiting_periods_sim.py',['-load', '6', '-density', '1', '-no_of_repeaters', '10', '-repeater_delay_multiplier', '30']),
        
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '2']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '3']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '4']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '5']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '6']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '7']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '8']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '9']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '10']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '11']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '12']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '13']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '14']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '15']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '16']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '17']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '18']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '19']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '20']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '21']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '22']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '23']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '24']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '25']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '26']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '27']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '28']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '29']),
        # ('exp1_waiting_periods_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '30'])
        
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '1']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '2']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '3']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '4']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '5']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '6']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '7']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '8']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '9']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '10']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '11']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '12']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '13']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '14']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '15']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '16']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '17']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '18']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '19']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '20']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '21']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '22']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '23']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '24']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '25']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '26']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '27']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '28']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '29']),
        # ('exp1_waiting_periods_sim.py',['-load', '2', '-density', '3', '-no_of_repeaters', '30', '-repeater_delay_multiplier', '30'])
        
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use executor.map to parallelize the execution of run_script
        results = executor.map(lambda x: run_script(*x), script_args_list)

        # Print the results
        for result in results:
            print(result)
