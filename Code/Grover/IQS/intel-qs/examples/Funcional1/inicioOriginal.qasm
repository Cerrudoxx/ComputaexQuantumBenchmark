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


long get_memory_usage() {
    std::ifstream stat_stream("/proc/self/stat", std::ios_base::in);
    if (!stat_stream.is_open()) {
        std::cerr << "Error al abrir /proc/self/stat" << std::endl;
        return 0;
    }

    // Variables para los campos de /proc/self/stat
    std::string pid, comm, state, ppid, pgrp, session, tty_nr, tpgid, flags;
    unsigned long minflt, cminflt, majflt, cmajflt, utime, stime, cutime, cstime;
    long priority, nice, num_threads, itrealvalue, starttime, vsize, rss;

    // Leer los campos hasta llegar a rss (24º campo)
    stat_stream >> pid >> comm >> state >> ppid >> pgrp >> session >> tty_nr
                >> tpgid >> flags >> minflt >> cminflt >> majflt >> cmajflt
                >> utime >> stime >> cutime >> cstime >> priority >> nice
                >> num_threads >> itrealvalue >> starttime >> vsize >> rss;

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

    int num_qubits =  &NUM_QUBITS&;

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


