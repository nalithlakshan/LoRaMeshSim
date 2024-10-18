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
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '9000', '-total_sim_packets', '1000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '9000', '-total_sim_packets', '2000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '9000', '-total_sim_packets', '3000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '9000', '-total_sim_packets', '4000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '9000', '-total_sim_packets', '5000']),

        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '8000', '-total_sim_packets', '1000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '8000', '-total_sim_packets', '2000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '8000', '-total_sim_packets', '3000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '8000', '-total_sim_packets', '4000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '8000', '-total_sim_packets', '5000']),

        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '7000', '-total_sim_packets', '1000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '7000', '-total_sim_packets', '2000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '7000', '-total_sim_packets', '3000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '7000', '-total_sim_packets', '4000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '7000', '-total_sim_packets', '5000']),

        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '6000', '-total_sim_packets', '1000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '6000', '-total_sim_packets', '2000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '6000', '-total_sim_packets', '3000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '6000', '-total_sim_packets', '4000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '6000', '-total_sim_packets', '5000']),

        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5500', '-total_sim_packets', '1000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5500', '-total_sim_packets', '2000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5500', '-total_sim_packets', '3000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5500', '-total_sim_packets', '4000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5500', '-total_sim_packets', '5000']),

        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5200', '-total_sim_packets', '1000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5200', '-total_sim_packets', '2000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5200', '-total_sim_packets', '3000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5200', '-total_sim_packets', '4000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5200', '-total_sim_packets', '5000']),

        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5000', '-total_sim_packets', '1000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5000', '-total_sim_packets', '2000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5000', '-total_sim_packets', '3000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5000', '-total_sim_packets', '4000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '5000', '-total_sim_packets', '5000']),

        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '4000', '-total_sim_packets', '1000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '4000', '-total_sim_packets', '2000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '4000', '-total_sim_packets', '3000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '4000', '-total_sim_packets', '4000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '4000', '-total_sim_packets', '5000']),

        ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '3000', '-total_sim_packets', '1000']),
        ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '3000', '-total_sim_packets', '2000']),
        ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '3000', '-total_sim_packets', '3000']),
        ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '3000', '-total_sim_packets', '4000']),
        ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '3000', '-total_sim_packets', '5000']),

        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '4800', '-total_sim_packets', '1000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '4800', '-total_sim_packets', '2000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '4800', '-total_sim_packets', '3000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '4800', '-total_sim_packets', '4000']),
        # ('exp3_max_traffic_sim.py',['-load', '3', '-density', '2', '-no_of_repeaters', '20', '-repeater_delay_multiplier', '1', '-avg_send_time', '4800', '-total_sim_packets', '5000']),
        
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use executor.map to parallelize the execution of run_script
        results = executor.map(lambda x: run_script(*x), script_args_list)

        # Print the results
        for result in results:
            print(result)
