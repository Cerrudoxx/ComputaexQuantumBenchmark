#include "../include/qureg.hpp"
#include "../include/gate_counter.hpp"
#include <iostream>
#include <cmath>
#include <chrono>
#include <iomanip>
#include <fstream>
#include <unistd.h>
#include <vector>
#include <thread>


// Función para obtener uso de memoria en Linux (en kilobytes)
long get_memory_usage() {
    std::ifstream stat_stream("/proc/self/stat", std::ios_base::in);
    if (!stat_stream.is_open()) {
        std::cerr << "Error al abrir /proc/self/stat" << std::endl;
        return 0;
    }

    std::string pid, comm, state, ppid, pgrp, session, tty_nr, tpgid, flags;
    unsigned long vsize;
    long rss;

    stat_stream >> pid >> comm >> state >> ppid >> pgrp >> session >> tty_nr
                >> tpgid >> flags >> vsize >> vsize >> vsize >> vsize >> vsize
                >> vsize >> vsize >> vsize >> vsize >> vsize >> vsize >> vsize
                >> vsize >> vsize >> vsize >> vsize >> vsize >> vsize >> vsize
                >> vsize >> vsize >> vsize >> vsize >> rss;
    stat_stream.close();

    long page_size_kb = sysconf(_SC_PAGE_SIZE) / 1024; // Tamaño de página en KB
    return rss * page_size_kb; // Memoria residente en KB
}


int main(int argc, char** argv) {

#ifndef INTELQS_HAS_MPI
    std::cout << "\nThis introductory code is thought to be run with MPI.\n"
        << "However the code will execute also without MPI.\n";
#endif

    iqs::mpi::Environment env(argc, argv);
    if (!env.IsUsefulRank()) return 0;

    int myid = env.GetStateRank();

    int num_qubits =  5;

    iqs::QubitRegister<ComplexDP> psi(num_qubits);

    std::size_t index = 0;
    psi.Initialize("base", 0); 


// psi.Print("Qubits: ");
if (myid == 0) std::cout << std::endl;

auto start = std::chrono::high_resolution_clock::now();

    // Vector para almacenar muestras de memoria
    std::vector<long> memory_samples;
    const int sample_interval_us = 1000; // Muestrear cada 1ms

    // Hilo para muestrear memoria en segundo plano
    bool stop_sampling = false;
    std::thread memory_sampler([&]() {
        while (!stop_sampling) {
            memory_samples.push_back(get_memory_usage());
            std::this_thread::sleep_for(std::chrono::microseconds(sample_interval_us));
        }
    });

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


psi.Print("Measurement =");

 if(myid==0){std::cout << "Qubits utilizados: " << num_qubits << std::endl;}
  


 }
 
