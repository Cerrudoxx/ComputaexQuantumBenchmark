import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_DIR = os.path.join(BASE_DIR, "environments")

SUPPORTED_SIMULATORS = {
    "qiskit": {
        "env_name": "qiskit",
        "env_file": os.path.join(ENV_DIR, "qiskit_environment.yml"),
        "folders": ["Code/Grover/Qiskit", "Code/QFT/Qiskit", "Code/QuantumVolume/Qiskit"]
    },
    "qulacs": {
        "env_name": "qulacs",
        "env_file": os.path.join(ENV_DIR, "qulacs_environment.yml"),
        "folders": ["Code/Grover/Qulacs", "Code/QFT/Qulacs", "Code/QuantumVolume/Qulacs"]
    },
    "cirq": {
        "env_name": "cirq",
        "env_file": os.path.join(ENV_DIR, "cirq_environment.yml"),
        "folders": ["Code/Grover/Cirq", "Code/QFT/Cirq", "Code/QuantumVolume/Cirq"]
    },
    "pennylane": {
        "env_name": "pennylane",
        "env_file": os.path.join(ENV_DIR, "pennylane_environment.yml"),
        "folders": ["Code/Grover/Pennylane", "Code/QFT/Pennylane", "Code/QuantumVolume/Pennylane"]
    },
    "qibo": {
        "env_name": "qibo",
        "env_file": os.path.join(ENV_DIR, "qibo_environment.yml"),
        "folders": ["Code/Grover/Qibo", "Code/QFT/Qibo", "Code/QuantumVolume/Qibo"]
    },
#    "iqs": {
#        "env_name": "hpc_iqs",
#        "env_file": os.path.join(ENV_DIR, "iqs_environment.yml"),
#         "folders": ["Code/Grover/IQS", "Code/QFT/IQS", "Code/QuantumVolume/IQS"]
#    },
    "qsimov": {
        "env_name": "qsimov",
        "env_file": os.path.join(ENV_DIR, "qsimov_environment.yml"),
        "folders": ["Code/Grover/Qsimov", "Code/QFT/Qsimov", "Code/QuantumVolume/Qsimov"]
    }
}

def get_available_simulators():
    return list(SUPPORTED_SIMULATORS.keys())