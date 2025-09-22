
}


int main(int argc, char** argv) {
#ifndef INTELQS_HAS_MPI
    std::cout << "\nThis introductory code is thought to be run with MPI.\n"
              << "However the code will execute also without MPI.\n";
#endif

    iqs::mpi::Environment env(argc, argv);
    if (!env.IsUsefulRank()) return 0;

    int myid = env.GetStateRank();

    int num_processes = env.GetStateSize();  // Added: Get number of MPI processes

    // Added: Define your max cores limit here (change to your desired value)
    int max_cores = 1;

    // Added: Enforce max by checking/adjusting
    if (num_processes > max_cores) {
        if (myid == 0) {
            std::cout << "Error: Number of MPI processes (" << num_processes << ") exceeds max cores (" << max_cores << "). Aborting." << std::endl;
        }
        return 1;  // Or use env.Barrier() then MPI_Abort(env.GetComm(), 1);
    }

    // Added: Limit OpenMP threads per process to respect total max_cores
    int max_threads_per_process = std::max(1, max_cores / num_processes);
    omp_set_num_threads(max_threads_per_process);


    int num_qubits = 19;    
    iqs::QubitRegister<ComplexDP> psi(num_qubits);

    if (myid == 0) {
        auto now = std::chrono::system_clock::now();
        std::time_t now_time = std::chrono::system_clock::to_time_t(now);
        std::cout << "Execution starts: " << std::put_time(std::localtime(&now_time), "%Y-%m-%d %H:%M:%S") << std::endl;
    }

    // Vector para almacenar muestras de memoria y tiempos
    std::vector<long> memory_samples;
    std::vector<double> times;
    const int sample_interval_us = 10000; // Muestrear cada 10 ms
    bool stop_sampling = false;

    // Hilo para muestrear memoria en segundo plano
    std::thread memory_sampler;
    if (myid == 0) {
        memory_sampler = std::thread([&]() {
            while (!stop_sampling) {
                memory_samples.push_back(get_memory_usage());
                std::this_thread::sleep_for(std::chrono::microseconds(sample_interval_us));
            }
        });
    }

    // Ejecutar la simulación 10 veces
        auto start = std::chrono::high_resolution_clock::now();
        run_simulation(psi);
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> duration = end - start;
        if (myid == 0) {
            std::cout << "Duración de la iteración " << ": " << duration.count() << " ms" << std::endl;
        }
        if (myid == 0) {
            times.push_back(duration.count());
        }


    // Detener muestreo de memoria
    if (myid == 0) {
        stop_sampling = true;
        memory_sampler.join();
    }
    // Calcular tiempos finales en milisegundos
    double t_grover_final = 0.0, std_grover_final = 0.0;
    if (myid == 0 && !times.empty()) {
        double sum = std::accumulate(times.begin(), times.end(), 0.0);
        t_grover_final = sum / times.size(); // Mantener en milisegundos
        if (times.size() > 1) {
            double sq_sum = std::accumulate(times.begin(), times.end(), 0.0,
                [](double a, double b) { return a + b * b; });
            std_grover_final = std::sqrt(sq_sum / times.size() - (sum / times.size()) * (sum / times.size()));
        }
    }
    // Calcular uso medio y pico de memoria
    long peak_memory = 0;
    double avg_memory = 0.0;
    if (myid == 0 && !memory_samples.empty()) {
        long long sum = std::accumulate(memory_samples.begin(), memory_samples.end(), 0LL);
        avg_memory = static_cast<double>(sum) / memory_samples.size();
        peak_memory = *std::max_element(memory_samples.begin(), memory_samples.end());
    // Imprimir resultados
    if (myid == 0) {
        std::cout << std::fixed << std::setprecision(3);
        std::cout << "Tiempo de ejecución promedio: " << t_grover_final << " ms" << std::endl;
        std::cout << "Desviación estándar del tiempo: " << std_grover_final << " ms" << std::endl;
        std::cout << "Uso medio de RAM: " << avg_memory << " KB" << std::endl;
        std::cout << "Pico de uso de RAM: " << peak_memory << " KB" << std::endl;
        std::cout << "Qubits utilizados: " << num_qubits << std::endl;

        // Obtener la fecha actual para el nombre del fichero
        auto now = std::chrono::system_clock::now();
        std::time_t now_time = std::chrono::system_clock::to_time_t(now);
        std::tm* tm_ptr = std::localtime(&now_time);
        char date_str[32];
        std::strftime(date_str, sizeof(date_str), "%Y-%m-%d_%H-%M-%S", tm_ptr);

        std::string filename = "Resultados/resultadosEjecucionQV";
        filename += std::to_string(num_qubits);
        filename += "_qubit_";
        filename += ".csv";

        // Crear el directorio "Resultados" si no existe
        struct stat st = {0};
        if (stat("Resultados", &st) == -1) {
            mkdir("Resultados", 0700);
        }

        // Guardar resultados en un fichero CSV
        std::ofstream csv_file;
        bool write_header = false;
        // Si el archivo no existe, escribir cabecera
        std::ifstream test_file(filename);
        if (!test_file.good()) {
            write_header = true;
        }
        test_file.close();

        csv_file.open(filename, std::ios::app);
        if (csv_file.is_open()) {
            if (write_header) {
                csv_file << "Tiempo promedio (ms),Desviación estándar (ms),RAM media (KB),RAM pico (KB),Qubits,Iteraciones óptimas\n";
            }
            csv_file << std::fixed << std::setprecision(3)
                     << t_grover_final << ","
                     << std_grover_final << ","
                     << avg_memory << ","
                     << peak_memory << ","
                     << num_qubits << std::endl;
            csv_file.close();
        } else {
            std::cerr << "No se pudo abrir el fichero " << filename << " para escritura." << std::endl;
        }
    }

    return 0;
}

}