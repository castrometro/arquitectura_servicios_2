import multiprocessing
import time
import subprocess

def run_comunidad_service():
    subprocess.run(['pipenv', 'run', 'python', 'servicios/comunidad_service.py'])

def run_user_service():
    subprocess.run(['pipenv', 'run', 'python', 'servicios/user_service.py'])

def run_foro_service():
    subprocess.run(['pipenv', 'run', 'python', 'servicios/foro_service.py'])

def tail_log(log_file):
    with open(log_file, 'r') as f:
        while True:
            line = f.readline()
            if line:
                print(line, end='')
            else:
                time.sleep(1)

if __name__ == "__main__":
    # Crear procesos
    comunidad_process = multiprocessing.Process(target=run_comunidad_service)
    user_process = multiprocessing.Process(target=run_user_service)
    foro_process = multiprocessing.Process(target=run_foro_service)

    # Iniciar procesos
    comunidad_process.start()
    user_process.start()
    foro_process.start()

    print("Services started. Type 'comunidad' or 'user' to view logs, or 'exit' to quit.")

    while True:
        command = input("> ").strip().lower()
        if command == 'comunidad':
            print("Showing comunidad service logs:")
            tail_log('comunidad_service.log')
        elif command == 'user':
            print("Showing user service logs:")
            tail_log('user_service.log')
        elif command == 'exit':
            print("Stopping services...")
            comunidad_process.terminate()
            user_process.terminate()
            comunidad_process.join()
            user_process.join()
            break
        else:
            print("Unknown command. Type 'comunidad', 'user', or 'exit'.")
