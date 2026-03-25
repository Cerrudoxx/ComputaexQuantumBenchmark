
// Detener muestreo
stop_sampling = true;
memory_sampler.join();

// Momento final
auto end = std::chrono::high_resolution_clock::now();

// Calcular duración en milisegundos con decimales
std::chrono::duration<double, std::milli> duration = end - start;

// Imprimir resultado
std::cout << "Tiempo de ejecución: " << duration.count() << " milisegundos" << std::endl;


// Calcular uso medio y pico de memoria
long peak_memory = 0;
double avg_memory = 0.0;
if (!memory_samples.empty()) {
    long long sum = 0;
    for (long mem : memory_samples) {
        sum += mem;
        if (mem > peak_memory) peak_memory = mem;
    }
    avg_memory = static_cast<double>(sum) / memory_samples.size();
    }

std::cout << std::fixed << std::setprecision(3);
std::cout << "Uso medio de RAM: " << avg_memory << " KB" << std::endl;
std::cout << "Pico de uso de RAM: " << peak_memory << " KB" << std::endl;


//psi.Print("Measurement =");

 if(myid==0){std::cout << "Qubits utilizados: " << num_qubits << std::endl;}
  


}

