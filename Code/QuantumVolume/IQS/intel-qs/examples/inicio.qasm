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
#include <sys/stat.h>
#include <sys/types.h>
#include <omp.h>


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



void run_simulation(iqs::QubitRegister<ComplexDP>& psi) {

