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

psi.ApplyHadamard(19);
psi.ApplyRotationZ(19, 1.5707933307386701);
psi.ApplyCPauliX(19,18);
psi.ApplyRotationZ(18, -M_PI/4);
psi.ApplyCPauliX(19,18);
psi.ApplyRotationZ(18, M_PI/4);
psi.ApplyHadamard(18);
psi.ApplyRotationZ(18, 1.5707903346824437);
psi.ApplyCPauliX(19,17);
psi.ApplyRotationZ(17, -M_PI/8);
psi.ApplyCPauliX(19,17);
psi.ApplyRotationZ(17, M_PI/8);
psi.ApplyCPauliX(18,17);
psi.ApplyRotationZ(17, -M_PI/4);
psi.ApplyCPauliX(18,17);
psi.ApplyRotationZ(17, M_PI/4);
psi.ApplyHadamard(17);
psi.ApplyRotationZ(17, 1.570784342569991);
psi.ApplyCPauliX(19,16);
psi.ApplyRotationZ(16, -M_PI/16);
psi.ApplyCPauliX(19,16);
psi.ApplyRotationZ(16, M_PI/16);
psi.ApplyCPauliX(18,16);
psi.ApplyRotationZ(16, -M_PI/8);
psi.ApplyCPauliX(18,16);
psi.ApplyRotationZ(16, M_PI/8);
psi.ApplyCPauliX(17,16);
psi.ApplyRotationZ(16, -M_PI/4);
psi.ApplyCPauliX(17,16);
psi.ApplyRotationZ(16, M_PI/4);
psi.ApplyHadamard(16);
psi.ApplyRotationZ(16, 1.5707723583450857);
psi.ApplyCPauliX(19,15);
psi.ApplyRotationZ(15, -M_PI/32);
psi.ApplyCPauliX(19,15);
psi.ApplyRotationZ(15, M_PI/32);
psi.ApplyCPauliX(18,15);
psi.ApplyRotationZ(15, -M_PI/16);
psi.ApplyCPauliX(18,15);
psi.ApplyRotationZ(15, M_PI/16);
psi.ApplyCPauliX(17,15);
psi.ApplyRotationZ(15, -M_PI/8);
psi.ApplyCPauliX(17,15);
psi.ApplyRotationZ(15, M_PI/8);
psi.ApplyCPauliX(16,15);
psi.ApplyRotationZ(15, -M_PI/4);
psi.ApplyCPauliX(16,15);
psi.ApplyRotationZ(15, M_PI/4);
psi.ApplyHadamard(15);
psi.ApplyRotationZ(15, 1.570748389895275);
psi.ApplyCPauliX(19,14);
psi.ApplyRotationZ(14, -M_PI/64);
psi.ApplyCPauliX(19,14);
psi.ApplyRotationZ(14, M_PI/64);
psi.ApplyCPauliX(18,14);
psi.ApplyRotationZ(14, -M_PI/32);
psi.ApplyCPauliX(18,14);
psi.ApplyRotationZ(14, M_PI/32);
psi.ApplyCPauliX(17,14);
psi.ApplyRotationZ(14, -M_PI/16);
psi.ApplyCPauliX(17,14);
psi.ApplyRotationZ(14, M_PI/16);
psi.ApplyCPauliX(16,14);
psi.ApplyRotationZ(14, -M_PI/8);
psi.ApplyCPauliX(16,14);
psi.ApplyRotationZ(14, M_PI/8);
psi.ApplyCPauliX(15,14);
psi.ApplyRotationZ(14, -M_PI/4);
psi.ApplyCPauliX(15,14);
psi.ApplyRotationZ(14, M_PI/4);
psi.ApplyHadamard(14);
psi.ApplyRotationZ(14, 1.5707004529956536);
psi.ApplyCPauliX(19,13);
psi.ApplyRotationZ(13, -M_PI/128);
psi.ApplyCPauliX(19,13);
psi.ApplyRotationZ(13, M_PI/128);
psi.ApplyCPauliX(18,13);
psi.ApplyRotationZ(13, -M_PI/64);
psi.ApplyCPauliX(18,13);
psi.ApplyRotationZ(13, M_PI/64);
psi.ApplyCPauliX(17,13);
psi.ApplyRotationZ(13, -M_PI/32);
psi.ApplyCPauliX(17,13);
psi.ApplyRotationZ(13, M_PI/32);
psi.ApplyCPauliX(16,13);
psi.ApplyRotationZ(13, -M_PI/16);
psi.ApplyCPauliX(16,13);
psi.ApplyRotationZ(13, M_PI/16);
psi.ApplyCPauliX(15,13);
psi.ApplyRotationZ(13, -M_PI/8);
psi.ApplyCPauliX(15,13);
psi.ApplyRotationZ(13, M_PI/8);
psi.ApplyCPauliX(14,13);
psi.ApplyRotationZ(13, -M_PI/4);
psi.ApplyCPauliX(14,13);
psi.ApplyRotationZ(13, M_PI/4);
psi.ApplyHadamard(13);
psi.ApplyRotationZ(13, 1.5706045791964107);
psi.ApplyCPauliX(19,12);
psi.ApplyRotationZ(12, -M_PI/256);
psi.ApplyCPauliX(19,12);
psi.ApplyRotationZ(12, M_PI/256);
psi.ApplyCPauliX(18,12);
psi.ApplyRotationZ(12, -M_PI/128);
psi.ApplyCPauliX(18,12);
psi.ApplyRotationZ(12, M_PI/128);
psi.ApplyCPauliX(17,12);
psi.ApplyRotationZ(12, -M_PI/64);
psi.ApplyCPauliX(17,12);
psi.ApplyRotationZ(12, M_PI/64);
psi.ApplyCPauliX(16,12);
psi.ApplyRotationZ(12, -M_PI/32);
psi.ApplyCPauliX(16,12);
psi.ApplyRotationZ(12, M_PI/32);
psi.ApplyCPauliX(15,12);
psi.ApplyRotationZ(12, -M_PI/16);
psi.ApplyCPauliX(15,12);
psi.ApplyRotationZ(12, M_PI/16);
psi.ApplyCPauliX(14,12);
psi.ApplyRotationZ(12, -M_PI/8);
psi.ApplyCPauliX(14,12);
psi.ApplyRotationZ(12, M_PI/8);
psi.ApplyCPauliX(13,12);
psi.ApplyRotationZ(12, -M_PI/4);
psi.ApplyCPauliX(13,12);
psi.ApplyRotationZ(12, M_PI/4);
psi.ApplyHadamard(12);
psi.ApplyRotationZ(12, 1.570412831597925);
psi.ApplyCPauliX(19,11);
psi.ApplyRotationZ(11, -M_PI/512);
psi.ApplyCPauliX(19,11);
psi.ApplyRotationZ(11, M_PI/512);
psi.ApplyCPauliX(18,11);
psi.ApplyRotationZ(11, -M_PI/256);
psi.ApplyCPauliX(18,11);
psi.ApplyRotationZ(11, M_PI/256);
psi.ApplyCPauliX(17,11);
psi.ApplyRotationZ(11, -M_PI/128);
psi.ApplyCPauliX(17,11);
psi.ApplyRotationZ(11, M_PI/128);
psi.ApplyCPauliX(16,11);
psi.ApplyRotationZ(11, -M_PI/64);
psi.ApplyCPauliX(16,11);
psi.ApplyRotationZ(11, M_PI/64);
psi.ApplyCPauliX(15,11);
psi.ApplyRotationZ(11, -M_PI/32);
psi.ApplyCPauliX(15,11);
psi.ApplyRotationZ(11, M_PI/32);
psi.ApplyCPauliX(14,11);
psi.ApplyRotationZ(11, -M_PI/16);
psi.ApplyCPauliX(14,11);
psi.ApplyRotationZ(11, M_PI/16);
psi.ApplyCPauliX(13,11);
psi.ApplyRotationZ(11, -M_PI/8);
psi.ApplyCPauliX(13,11);
psi.ApplyRotationZ(11, M_PI/8);
psi.ApplyCPauliX(12,11);
psi.ApplyRotationZ(11, -M_PI/4);
psi.ApplyCPauliX(12,11);
psi.ApplyRotationZ(11, M_PI/4);
psi.ApplyHadamard(11);
psi.ApplyRotationZ(11, 1.5700293364009537);
psi.ApplyCPauliX(19,10);
psi.ApplyRotationZ(10, -M_PI/1024);
psi.ApplyCPauliX(19,10);
psi.ApplyRotationZ(10, M_PI/1024);
psi.ApplyCPauliX(18,10);
psi.ApplyRotationZ(10, -M_PI/512);
psi.ApplyCPauliX(18,10);
psi.ApplyRotationZ(10, M_PI/512);
psi.ApplyCPauliX(17,10);
psi.ApplyRotationZ(10, -M_PI/256);
psi.ApplyCPauliX(17,10);
psi.ApplyRotationZ(10, M_PI/256);
psi.ApplyCPauliX(16,10);
psi.ApplyRotationZ(10, -M_PI/128);
psi.ApplyCPauliX(16,10);
psi.ApplyRotationZ(10, M_PI/128);
psi.ApplyCPauliX(15,10);
psi.ApplyRotationZ(10, -M_PI/64);
psi.ApplyCPauliX(15,10);
psi.ApplyRotationZ(10, M_PI/64);
psi.ApplyCPauliX(14,10);
psi.ApplyRotationZ(10, -M_PI/32);
psi.ApplyCPauliX(14,10);
psi.ApplyRotationZ(10, M_PI/32);
psi.ApplyCPauliX(13,10);
psi.ApplyRotationZ(10, -M_PI/16);
psi.ApplyCPauliX(13,10);
psi.ApplyRotationZ(10, M_PI/16);
psi.ApplyCPauliX(12,10);
psi.ApplyRotationZ(10, -M_PI/8);
psi.ApplyCPauliX(12,10);
psi.ApplyRotationZ(10, M_PI/8);
psi.ApplyCPauliX(11,10);
psi.ApplyRotationZ(10, -M_PI/4);
psi.ApplyCPauliX(11,10);
psi.ApplyRotationZ(10, M_PI/4);
psi.ApplyHadamard(10);
psi.ApplyRotationZ(10, 1.5692623460070108);
psi.ApplyCPauliX(19,9);
psi.ApplyRotationZ(9, -M_PI/2048);
psi.ApplyCPauliX(19,9);
psi.ApplyRotationZ(9, M_PI/2048);
psi.ApplyCPauliX(18,9);
psi.ApplyRotationZ(9, -M_PI/1024);
psi.ApplyCPauliX(18,9);
psi.ApplyRotationZ(9, M_PI/1024);
psi.ApplyCPauliX(17,9);
psi.ApplyRotationZ(9, -M_PI/512);
psi.ApplyCPauliX(17,9);
psi.ApplyRotationZ(9, M_PI/512);
psi.ApplyCPauliX(16,9);
psi.ApplyRotationZ(9, -M_PI/256);
psi.ApplyCPauliX(16,9);
psi.ApplyRotationZ(9, M_PI/256);
psi.ApplyCPauliX(15,9);
psi.ApplyRotationZ(9, -M_PI/128);
psi.ApplyCPauliX(15,9);
psi.ApplyRotationZ(9, M_PI/128);
psi.ApplyCPauliX(14,9);
psi.ApplyRotationZ(9, -M_PI/64);
psi.ApplyCPauliX(14,9);
psi.ApplyRotationZ(9, M_PI/64);
psi.ApplyCPauliX(13,9);
psi.ApplyRotationZ(9, -M_PI/32);
psi.ApplyCPauliX(13,9);
psi.ApplyRotationZ(9, M_PI/32);
psi.ApplyCPauliX(12,9);
psi.ApplyRotationZ(9, -M_PI/16);
psi.ApplyCPauliX(12,9);
psi.ApplyRotationZ(9, M_PI/16);
psi.ApplyCPauliX(11,9);
psi.ApplyRotationZ(9, -M_PI/8);
psi.ApplyCPauliX(11,9);
psi.ApplyRotationZ(9, M_PI/8);
psi.ApplyCPauliX(10,9);
psi.ApplyRotationZ(9, -M_PI/4);
psi.ApplyCPauliX(10,9);
psi.ApplyRotationZ(9, M_PI/4);
psi.ApplyHadamard(9);
psi.ApplyRotationZ(9, 1.5677283652191252);
psi.ApplyCPauliX(19,8);
psi.ApplyRotationZ(8, -M_PI/4096);
psi.ApplyCPauliX(19,8);
psi.ApplyRotationZ(8, M_PI/4096);
psi.ApplyCPauliX(18,8);
psi.ApplyRotationZ(8, -M_PI/2048);
psi.ApplyCPauliX(18,8);
psi.ApplyRotationZ(8, M_PI/2048);
psi.ApplyCPauliX(17,8);
psi.ApplyRotationZ(8, -M_PI/1024);
psi.ApplyCPauliX(17,8);
psi.ApplyRotationZ(8, M_PI/1024);
psi.ApplyCPauliX(16,8);
psi.ApplyRotationZ(8, -M_PI/512);
psi.ApplyCPauliX(16,8);
psi.ApplyRotationZ(8, M_PI/512);
psi.ApplyCPauliX(15,8);
psi.ApplyRotationZ(8, -M_PI/256);
psi.ApplyCPauliX(15,8);
psi.ApplyRotationZ(8, M_PI/256);
psi.ApplyCPauliX(14,8);
psi.ApplyRotationZ(8, -M_PI/128);
psi.ApplyCPauliX(14,8);
psi.ApplyRotationZ(8, M_PI/128);
psi.ApplyCPauliX(13,8);
psi.ApplyRotationZ(8, -M_PI/64);
psi.ApplyCPauliX(13,8);
psi.ApplyRotationZ(8, M_PI/64);
psi.ApplyCPauliX(12,8);
psi.ApplyRotationZ(8, -M_PI/32);
psi.ApplyCPauliX(12,8);
psi.ApplyRotationZ(8, M_PI/32);
psi.ApplyCPauliX(11,8);
psi.ApplyRotationZ(8, -M_PI/16);
psi.ApplyCPauliX(11,8);
psi.ApplyRotationZ(8, M_PI/16);
psi.ApplyCPauliX(10,8);
psi.ApplyRotationZ(8, -M_PI/8);
psi.ApplyCPauliX(10,8);
psi.ApplyRotationZ(8, M_PI/8);
psi.ApplyCPauliX(9,8);
psi.ApplyRotationZ(8, -M_PI/4);
psi.ApplyCPauliX(9,8);
psi.ApplyRotationZ(8, M_PI/4);
psi.ApplyHadamard(8);
psi.ApplyRotationZ(8, 1.5646604036433538);
psi.ApplyCPauliX(19,7);
psi.ApplyRotationZ(7, -M_PI/8192);
psi.ApplyCPauliX(19,7);
psi.ApplyRotationZ(7, M_PI/8192);
psi.ApplyCPauliX(18,7);
psi.ApplyRotationZ(7, -M_PI/4096);
psi.ApplyCPauliX(18,7);
psi.ApplyRotationZ(7, M_PI/4096);
psi.ApplyCPauliX(17,7);
psi.ApplyRotationZ(7, -M_PI/2048);
psi.ApplyCPauliX(17,7);
psi.ApplyRotationZ(7, M_PI/2048);
psi.ApplyCPauliX(16,7);
psi.ApplyRotationZ(7, -M_PI/1024);
psi.ApplyCPauliX(16,7);
psi.ApplyRotationZ(7, M_PI/1024);
psi.ApplyCPauliX(15,7);
psi.ApplyRotationZ(7, -M_PI/512);
psi.ApplyCPauliX(15,7);
psi.ApplyRotationZ(7, M_PI/512);
psi.ApplyCPauliX(14,7);
psi.ApplyRotationZ(7, -M_PI/256);
psi.ApplyCPauliX(14,7);
psi.ApplyRotationZ(7, M_PI/256);
psi.ApplyCPauliX(13,7);
psi.ApplyRotationZ(7, -M_PI/128);
psi.ApplyCPauliX(13,7);
psi.ApplyRotationZ(7, M_PI/128);
psi.ApplyCPauliX(12,7);
psi.ApplyRotationZ(7, -M_PI/64);
psi.ApplyCPauliX(12,7);
psi.ApplyRotationZ(7, M_PI/64);
psi.ApplyCPauliX(11,7);
psi.ApplyRotationZ(7, -M_PI/32);
psi.ApplyCPauliX(11,7);
psi.ApplyRotationZ(7, M_PI/32);
psi.ApplyCPauliX(10,7);
psi.ApplyRotationZ(7, -M_PI/16);
psi.ApplyCPauliX(10,7);
psi.ApplyRotationZ(7, M_PI/16);
psi.ApplyCPauliX(9,7);
psi.ApplyRotationZ(7, -M_PI/8);
psi.ApplyCPauliX(9,7);
psi.ApplyRotationZ(7, M_PI/8);
psi.ApplyCPauliX(8,7);
psi.ApplyRotationZ(7, -M_PI/4);
psi.ApplyCPauliX(8,7);
psi.ApplyRotationZ(7, M_PI/4);
psi.ApplyHadamard(7);
psi.ApplyRotationZ(7, 1.5585244804918112);
psi.ApplyCPauliX(19,6);
psi.ApplyRotationZ(6, -M_PI/16384);
psi.ApplyCPauliX(19,6);
psi.ApplyRotationZ(6, M_PI/16384);
psi.ApplyCPauliX(18,6);
psi.ApplyRotationZ(6, -M_PI/8192);
psi.ApplyCPauliX(18,6);
psi.ApplyRotationZ(6, M_PI/8192);
psi.ApplyCPauliX(17,6);
psi.ApplyRotationZ(6, -M_PI/4096);
psi.ApplyCPauliX(17,6);
psi.ApplyRotationZ(6, M_PI/4096);
psi.ApplyCPauliX(16,6);
psi.ApplyRotationZ(6, -M_PI/2048);
psi.ApplyCPauliX(16,6);
psi.ApplyRotationZ(6, M_PI/2048);
psi.ApplyCPauliX(15,6);
psi.ApplyRotationZ(6, -M_PI/1024);
psi.ApplyCPauliX(15,6);
psi.ApplyRotationZ(6, M_PI/1024);
psi.ApplyCPauliX(14,6);
psi.ApplyRotationZ(6, -M_PI/512);
psi.ApplyCPauliX(14,6);
psi.ApplyRotationZ(6, M_PI/512);
psi.ApplyCPauliX(13,6);
psi.ApplyRotationZ(6, -M_PI/256);
psi.ApplyCPauliX(13,6);
psi.ApplyRotationZ(6, M_PI/256);
psi.ApplyCPauliX(12,6);
psi.ApplyRotationZ(6, -M_PI/128);
psi.ApplyCPauliX(12,6);
psi.ApplyRotationZ(6, M_PI/128);
psi.ApplyCPauliX(11,6);
psi.ApplyRotationZ(6, -M_PI/64);
psi.ApplyCPauliX(11,6);
psi.ApplyRotationZ(6, M_PI/64);
psi.ApplyCPauliX(10,6);
psi.ApplyRotationZ(6, -M_PI/32);
psi.ApplyCPauliX(10,6);
psi.ApplyRotationZ(6, M_PI/32);
psi.ApplyCPauliX(9,6);
psi.ApplyRotationZ(6, -M_PI/16);
psi.ApplyCPauliX(9,6);
psi.ApplyRotationZ(6, M_PI/16);
psi.ApplyCPauliX(8,6);
psi.ApplyRotationZ(6, -M_PI/8);
psi.ApplyCPauliX(8,6);
psi.ApplyRotationZ(6, M_PI/8);
psi.ApplyCPauliX(7,6);
psi.ApplyRotationZ(6, -M_PI/4);
psi.ApplyCPauliX(7,6);
psi.ApplyRotationZ(6, M_PI/4);
psi.ApplyHadamard(6);
psi.ApplyRotationZ(6, 1.5462526341887262);
psi.ApplyCPauliX(19,5);
psi.ApplyRotationZ(5, -M_PI/32768);
psi.ApplyCPauliX(19,5);
psi.ApplyRotationZ(5, M_PI/32768);
psi.ApplyCPauliX(18,5);
psi.ApplyRotationZ(5, -M_PI/16384);
psi.ApplyCPauliX(18,5);
psi.ApplyRotationZ(5, M_PI/16384);
psi.ApplyCPauliX(17,5);
psi.ApplyRotationZ(5, -M_PI/8192);
psi.ApplyCPauliX(17,5);
psi.ApplyRotationZ(5, M_PI/8192);
psi.ApplyCPauliX(16,5);
psi.ApplyRotationZ(5, -M_PI/4096);
psi.ApplyCPauliX(16,5);
psi.ApplyRotationZ(5, M_PI/4096);
psi.ApplyCPauliX(15,5);
psi.ApplyRotationZ(5, -M_PI/2048);
psi.ApplyCPauliX(15,5);
psi.ApplyRotationZ(5, M_PI/2048);
psi.ApplyCPauliX(14,5);
psi.ApplyRotationZ(5, -M_PI/1024);
psi.ApplyCPauliX(14,5);
psi.ApplyRotationZ(5, M_PI/1024);
psi.ApplyCPauliX(13,5);
psi.ApplyRotationZ(5, -M_PI/512);
psi.ApplyCPauliX(13,5);
psi.ApplyRotationZ(5, M_PI/512);
psi.ApplyCPauliX(12,5);
psi.ApplyRotationZ(5, -M_PI/256);
psi.ApplyCPauliX(12,5);
psi.ApplyRotationZ(5, M_PI/256);
psi.ApplyCPauliX(11,5);
psi.ApplyRotationZ(5, -M_PI/128);
psi.ApplyCPauliX(11,5);
psi.ApplyRotationZ(5, M_PI/128);
psi.ApplyCPauliX(10,5);
psi.ApplyRotationZ(5, -M_PI/64);
psi.ApplyCPauliX(10,5);
psi.ApplyRotationZ(5, M_PI/64);
psi.ApplyCPauliX(9,5);
psi.ApplyRotationZ(5, -M_PI/32);
psi.ApplyCPauliX(9,5);
psi.ApplyRotationZ(5, M_PI/32);
psi.ApplyCPauliX(8,5);
psi.ApplyRotationZ(5, -M_PI/16);
psi.ApplyCPauliX(8,5);
psi.ApplyRotationZ(5, M_PI/16);
psi.ApplyCPauliX(7,5);
psi.ApplyRotationZ(5, -M_PI/8);
psi.ApplyCPauliX(7,5);
psi.ApplyRotationZ(5, M_PI/8);
psi.ApplyCPauliX(6,5);
psi.ApplyRotationZ(5, -M_PI/4);
psi.ApplyCPauliX(6,5);
psi.ApplyRotationZ(5, M_PI/4);
psi.ApplyHadamard(5);
psi.ApplyRotationZ(5, 1.521708941582556);
psi.ApplyCPauliX(19,4);
psi.ApplyRotationZ(4, -M_PI/65536);
psi.ApplyCPauliX(19,4);
psi.ApplyRotationZ(4, M_PI/65536);
psi.ApplyCPauliX(18,4);
psi.ApplyRotationZ(4, -M_PI/32768);
psi.ApplyCPauliX(18,4);
psi.ApplyRotationZ(4, M_PI/32768);
psi.ApplyCPauliX(17,4);
psi.ApplyRotationZ(4, -M_PI/16384);
psi.ApplyCPauliX(17,4);
psi.ApplyRotationZ(4, M_PI/16384);
psi.ApplyCPauliX(16,4);
psi.ApplyRotationZ(4, -M_PI/8192);
psi.ApplyCPauliX(16,4);
psi.ApplyRotationZ(4, M_PI/8192);
psi.ApplyCPauliX(15,4);
psi.ApplyRotationZ(4, -M_PI/4096);
psi.ApplyCPauliX(15,4);
psi.ApplyRotationZ(4, M_PI/4096);
psi.ApplyCPauliX(14,4);
psi.ApplyRotationZ(4, -M_PI/2048);
psi.ApplyCPauliX(14,4);
psi.ApplyRotationZ(4, M_PI/2048);
psi.ApplyCPauliX(13,4);
psi.ApplyRotationZ(4, -M_PI/1024);
psi.ApplyCPauliX(13,4);
psi.ApplyRotationZ(4, M_PI/1024);
psi.ApplyCPauliX(12,4);
psi.ApplyRotationZ(4, -M_PI/512);
psi.ApplyCPauliX(12,4);
psi.ApplyRotationZ(4, M_PI/512);
psi.ApplyCPauliX(11,4);
psi.ApplyRotationZ(4, -M_PI/256);
psi.ApplyCPauliX(11,4);
psi.ApplyRotationZ(4, M_PI/256);
psi.ApplyCPauliX(10,4);
psi.ApplyRotationZ(4, -M_PI/128);
psi.ApplyCPauliX(10,4);
psi.ApplyRotationZ(4, M_PI/128);
psi.ApplyCPauliX(9,4);
psi.ApplyRotationZ(4, -M_PI/64);
psi.ApplyCPauliX(9,4);
psi.ApplyRotationZ(4, M_PI/64);
psi.ApplyCPauliX(8,4);
psi.ApplyRotationZ(4, -M_PI/32);
psi.ApplyCPauliX(8,4);
psi.ApplyRotationZ(4, M_PI/32);
psi.ApplyCPauliX(7,4);
psi.ApplyRotationZ(4, -M_PI/16);
psi.ApplyCPauliX(7,4);
psi.ApplyRotationZ(4, M_PI/16);
psi.ApplyCPauliX(6,4);
psi.ApplyRotationZ(4, -M_PI/8);
psi.ApplyCPauliX(6,4);
psi.ApplyRotationZ(4, M_PI/8);
psi.ApplyCPauliX(5,4);
psi.ApplyRotationZ(4, -M_PI/4);
psi.ApplyCPauliX(5,4);
psi.ApplyRotationZ(4, M_PI/4);
psi.ApplyHadamard(4);
psi.ApplyRotationZ(4, 1.4726215563702154);
psi.ApplyCPauliX(19,3);
psi.ApplyRotationZ(3, -M_PI/131072);
psi.ApplyCPauliX(19,3);
psi.ApplyRotationZ(3, M_PI/131072);
psi.ApplyCPauliX(18,3);
psi.ApplyRotationZ(3, -M_PI/65536);
psi.ApplyCPauliX(18,3);
psi.ApplyRotationZ(3, M_PI/65536);
psi.ApplyCPauliX(17,3);
psi.ApplyRotationZ(3, -M_PI/32768);
psi.ApplyCPauliX(17,3);
psi.ApplyRotationZ(3, M_PI/32768);
psi.ApplyCPauliX(16,3);
psi.ApplyRotationZ(3, -M_PI/16384);
psi.ApplyCPauliX(16,3);
psi.ApplyRotationZ(3, M_PI/16384);
psi.ApplyCPauliX(15,3);
psi.ApplyRotationZ(3, -M_PI/8192);
psi.ApplyCPauliX(15,3);
psi.ApplyRotationZ(3, M_PI/8192);
psi.ApplyCPauliX(14,3);
psi.ApplyRotationZ(3, -M_PI/4096);
psi.ApplyCPauliX(14,3);
psi.ApplyRotationZ(3, M_PI/4096);
psi.ApplyCPauliX(13,3);
psi.ApplyRotationZ(3, -M_PI/2048);
psi.ApplyCPauliX(13,3);
psi.ApplyRotationZ(3, M_PI/2048);
psi.ApplyCPauliX(12,3);
psi.ApplyRotationZ(3, -M_PI/1024);
psi.ApplyCPauliX(12,3);
psi.ApplyRotationZ(3, M_PI/1024);
psi.ApplyCPauliX(11,3);
psi.ApplyRotationZ(3, -M_PI/512);
psi.ApplyCPauliX(11,3);
psi.ApplyRotationZ(3, M_PI/512);
psi.ApplyCPauliX(10,3);
psi.ApplyRotationZ(3, -M_PI/256);
psi.ApplyCPauliX(10,3);
psi.ApplyRotationZ(3, M_PI/256);
psi.ApplyCPauliX(9,3);
psi.ApplyRotationZ(3, -M_PI/128);
psi.ApplyCPauliX(9,3);
psi.ApplyRotationZ(3, M_PI/128);
psi.ApplyCPauliX(8,3);
psi.ApplyRotationZ(3, -M_PI/64);
psi.ApplyCPauliX(8,3);
psi.ApplyRotationZ(3, M_PI/64);
psi.ApplyCPauliX(7,3);
psi.ApplyRotationZ(3, -M_PI/32);
psi.ApplyCPauliX(7,3);
psi.ApplyRotationZ(3, M_PI/32);
psi.ApplyCPauliX(6,3);
psi.ApplyRotationZ(3, -M_PI/16);
psi.ApplyCPauliX(6,3);
psi.ApplyRotationZ(3, M_PI/16);
psi.ApplyCPauliX(5,3);
psi.ApplyRotationZ(3, -M_PI/8);
psi.ApplyCPauliX(5,3);
psi.ApplyRotationZ(3, M_PI/8);
psi.ApplyCPauliX(4,3);
psi.ApplyRotationZ(3, -M_PI/4);
psi.ApplyCPauliX(4,3);
psi.ApplyRotationZ(3, M_PI/4);
psi.ApplyHadamard(3);
psi.ApplyRotationZ(3, 7*M_PI/16);
psi.ApplyCPauliX(19,2);
psi.ApplyRotationZ(2, -M_PI/262144);
psi.ApplyCPauliX(19,2);
psi.ApplyRotationZ(2, M_PI/262144);
psi.ApplyCPauliX(18,2);
psi.ApplyRotationZ(2, -M_PI/131072);
psi.ApplyCPauliX(18,2);
psi.ApplyRotationZ(2, M_PI/131072);
psi.ApplyCPauliX(17,2);
psi.ApplyRotationZ(2, -M_PI/65536);
psi.ApplyCPauliX(17,2);
psi.ApplyRotationZ(2, M_PI/65536);
psi.ApplyCPauliX(16,2);
psi.ApplyRotationZ(2, -M_PI/32768);
psi.ApplyCPauliX(16,2);
psi.ApplyRotationZ(2, M_PI/32768);
psi.ApplyCPauliX(15,2);
psi.ApplyRotationZ(2, -M_PI/16384);
psi.ApplyCPauliX(15,2);
psi.ApplyRotationZ(2, M_PI/16384);
psi.ApplyCPauliX(14,2);
psi.ApplyRotationZ(2, -M_PI/8192);
psi.ApplyCPauliX(14,2);
psi.ApplyRotationZ(2, M_PI/8192);
psi.ApplyCPauliX(13,2);
psi.ApplyRotationZ(2, -M_PI/4096);
psi.ApplyCPauliX(13,2);
psi.ApplyRotationZ(2, M_PI/4096);
psi.ApplyCPauliX(12,2);
psi.ApplyRotationZ(2, -M_PI/2048);
psi.ApplyCPauliX(12,2);
psi.ApplyRotationZ(2, M_PI/2048);
psi.ApplyCPauliX(11,2);
psi.ApplyRotationZ(2, -M_PI/1024);
psi.ApplyCPauliX(11,2);
psi.ApplyRotationZ(2, M_PI/1024);
psi.ApplyCPauliX(10,2);
psi.ApplyRotationZ(2, -M_PI/512);
psi.ApplyCPauliX(10,2);
psi.ApplyRotationZ(2, M_PI/512);
psi.ApplyCPauliX(9,2);
psi.ApplyRotationZ(2, -M_PI/256);
psi.ApplyCPauliX(9,2);
psi.ApplyRotationZ(2, M_PI/256);
psi.ApplyCPauliX(8,2);
psi.ApplyRotationZ(2, -M_PI/128);
psi.ApplyCPauliX(8,2);
psi.ApplyRotationZ(2, M_PI/128);
psi.ApplyCPauliX(7,2);
psi.ApplyRotationZ(2, -M_PI/64);
psi.ApplyCPauliX(7,2);
psi.ApplyRotationZ(2, M_PI/64);
psi.ApplyCPauliX(6,2);
psi.ApplyRotationZ(2, -M_PI/32);
psi.ApplyCPauliX(6,2);
psi.ApplyRotationZ(2, M_PI/32);
psi.ApplyCPauliX(5,2);
psi.ApplyRotationZ(2, -M_PI/16);
psi.ApplyCPauliX(5,2);
psi.ApplyRotationZ(2, M_PI/16);
psi.ApplyCPauliX(4,2);
psi.ApplyRotationZ(2, -M_PI/8);
psi.ApplyCPauliX(4,2);
psi.ApplyRotationZ(2, M_PI/8);
psi.ApplyCPauliX(3,2);
psi.ApplyRotationZ(2, -M_PI/4);
psi.ApplyCPauliX(3,2);
psi.ApplyRotationZ(2, M_PI/4);
psi.ApplyHadamard(2);
psi.ApplyRotationZ(2, 3*M_PI/8);
psi.ApplyCPauliX(19,1);
psi.ApplyRotationZ(1, -M_PI/524288);
psi.ApplyCPauliX(19,1);
psi.ApplyRotationZ(1, M_PI/524288);
psi.ApplyCPauliX(18,1);
psi.ApplyRotationZ(1, -M_PI/262144);
psi.ApplyCPauliX(18,1);
psi.ApplyRotationZ(1, M_PI/262144);
psi.ApplyCPauliX(17,1);
psi.ApplyRotationZ(1, -M_PI/131072);
psi.ApplyCPauliX(17,1);
psi.ApplyRotationZ(1, M_PI/131072);
psi.ApplyCPauliX(16,1);
psi.ApplyRotationZ(1, -M_PI/65536);
psi.ApplyCPauliX(16,1);
psi.ApplyRotationZ(1, M_PI/65536);
psi.ApplyCPauliX(15,1);
psi.ApplyRotationZ(1, -M_PI/32768);
psi.ApplyCPauliX(15,1);
psi.ApplyRotationZ(1, M_PI/32768);
psi.ApplyCPauliX(14,1);
psi.ApplyRotationZ(1, -M_PI/16384);
psi.ApplyCPauliX(14,1);
psi.ApplyRotationZ(1, M_PI/16384);
psi.ApplyCPauliX(13,1);
psi.ApplyRotationZ(1, -M_PI/8192);
psi.ApplyCPauliX(13,1);
psi.ApplyRotationZ(1, M_PI/8192);
psi.ApplyCPauliX(12,1);
psi.ApplyRotationZ(1, -M_PI/4096);
psi.ApplyCPauliX(12,1);
psi.ApplyRotationZ(1, M_PI/4096);
psi.ApplyCPauliX(11,1);
psi.ApplyRotationZ(1, -M_PI/2048);
psi.ApplyCPauliX(11,1);
psi.ApplyRotationZ(1, M_PI/2048);
psi.ApplyCPauliX(10,1);
psi.ApplyRotationZ(1, -M_PI/1024);
psi.ApplyCPauliX(10,1);
psi.ApplyRotationZ(1, M_PI/1024);
psi.ApplyCPauliX(9,1);
psi.ApplyRotationZ(1, -M_PI/512);
psi.ApplyCPauliX(9,1);
psi.ApplyRotationZ(1, M_PI/512);
psi.ApplyCPauliX(8,1);
psi.ApplyRotationZ(1, -M_PI/256);
psi.ApplyCPauliX(8,1);
psi.ApplyRotationZ(1, M_PI/256);
psi.ApplyCPauliX(7,1);
psi.ApplyRotationZ(1, -M_PI/128);
psi.ApplyCPauliX(7,1);
psi.ApplyRotationZ(1, M_PI/128);
psi.ApplyCPauliX(6,1);
psi.ApplyRotationZ(1, -M_PI/64);
psi.ApplyCPauliX(6,1);
psi.ApplyRotationZ(1, M_PI/64);
psi.ApplyCPauliX(5,1);
psi.ApplyRotationZ(1, -M_PI/32);
psi.ApplyCPauliX(5,1);
psi.ApplyRotationZ(1, M_PI/32);
psi.ApplyCPauliX(4,1);
psi.ApplyRotationZ(1, -M_PI/16);
psi.ApplyCPauliX(4,1);
psi.ApplyRotationZ(1, M_PI/16);
psi.ApplyCPauliX(3,1);
psi.ApplyRotationZ(1, -M_PI/8);
psi.ApplyCPauliX(3,1);
psi.ApplyRotationZ(1, M_PI/8);
psi.ApplyCPauliX(2,1);
psi.ApplyRotationZ(1, -M_PI/4);
psi.ApplyCPauliX(2,1);
psi.ApplyRotationZ(1, M_PI/4);
psi.ApplyHadamard(1);
psi.ApplyRotationZ(1, M_PI/4);
psi.ApplyCPauliX(19,0);
psi.ApplyRotationZ(0, -M_PI/1048576);
psi.ApplyCPauliX(19,0);
psi.ApplyRotationZ(0, M_PI/1048576);
psi.ApplyCPauliX(18,0);
psi.ApplyRotationZ(0, -M_PI/524288);
psi.ApplyCPauliX(18,0);
psi.ApplyRotationZ(0, M_PI/524288);
psi.ApplyCPauliX(17,0);
psi.ApplyRotationZ(0, -M_PI/262144);
psi.ApplyCPauliX(17,0);
psi.ApplyRotationZ(0, M_PI/262144);
psi.ApplyCPauliX(16,0);
psi.ApplyRotationZ(0, -M_PI/131072);
psi.ApplyCPauliX(16,0);
psi.ApplyRotationZ(0, M_PI/131072);
psi.ApplyCPauliX(15,0);
psi.ApplyRotationZ(0, -M_PI/65536);
psi.ApplyCPauliX(15,0);
psi.ApplyRotationZ(0, M_PI/65536);
psi.ApplyCPauliX(14,0);
psi.ApplyRotationZ(0, -M_PI/32768);
psi.ApplyCPauliX(14,0);
psi.ApplyRotationZ(0, M_PI/32768);
psi.ApplyCPauliX(13,0);
psi.ApplyRotationZ(0, -M_PI/16384);
psi.ApplyCPauliX(13,0);
psi.ApplyRotationZ(0, M_PI/16384);
psi.ApplyCPauliX(12,0);
psi.ApplyRotationZ(0, -M_PI/8192);
psi.ApplyCPauliX(12,0);
psi.ApplyRotationZ(0, M_PI/8192);
psi.ApplyCPauliX(11,0);
psi.ApplyRotationZ(0, -M_PI/4096);
psi.ApplyCPauliX(11,0);
psi.ApplyRotationZ(0, M_PI/4096);
psi.ApplyCPauliX(10,0);
psi.ApplyRotationZ(0, -M_PI/2048);
psi.ApplyCPauliX(10,0);
psi.ApplyRotationZ(0, M_PI/2048);
psi.ApplyCPauliX(9,0);
psi.ApplyRotationZ(0, -M_PI/1024);
psi.ApplyCPauliX(9,0);
psi.ApplyRotationZ(0, M_PI/1024);
psi.ApplyCPauliX(8,0);
psi.ApplyRotationZ(0, -M_PI/512);
psi.ApplyCPauliX(8,0);
psi.ApplyRotationZ(0, M_PI/512);
psi.ApplyCPauliX(7,0);
psi.ApplyRotationZ(0, -M_PI/256);
psi.ApplyCPauliX(7,0);
psi.ApplyRotationZ(0, M_PI/256);
psi.ApplyCPauliX(6,0);
psi.ApplyRotationZ(0, -M_PI/128);
psi.ApplyCPauliX(6,0);
psi.ApplyRotationZ(0, M_PI/128);
psi.ApplyCPauliX(5,0);
psi.ApplyRotationZ(0, -M_PI/64);
psi.ApplyCPauliX(5,0);
psi.ApplyRotationZ(0, M_PI/64);
psi.ApplyCPauliX(4,0);
psi.ApplyRotationZ(0, -M_PI/32);
psi.ApplyCPauliX(4,0);
psi.ApplyRotationZ(0, M_PI/32);
psi.ApplyCPauliX(3,0);
psi.ApplyRotationZ(0, -M_PI/16);
psi.ApplyCPauliX(3,0);
psi.ApplyRotationZ(0, M_PI/16);
psi.ApplyCPauliX(2,0);
psi.ApplyRotationZ(0, -M_PI/8);
psi.ApplyCPauliX(2,0);
psi.ApplyRotationZ(0, M_PI/8);
psi.ApplyCPauliX(1,0);
psi.ApplyRotationZ(0, -M_PI/4);
psi.ApplyCPauliX(1,0);
psi.ApplyRotationZ(0, M_PI/4);
psi.ApplyHadamard(0);

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
    int max_cores = 2;

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


    int num_qubits = 20;    
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
    const int n_iterations_in = 10;
    //run_simulation(psi);
    for (int i = 0; i < n_iterations_in; ++i) {
        auto start = std::chrono::high_resolution_clock::now();
        run_simulation(psi);
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double, std::milli> duration = end - start;
        if (myid == 0) {
            std::cout << "Duración de la iteración " << i + 1 << ": " << duration.count() << " ms" << std::endl;
        }
        if (myid == 0) {
            times.push_back(duration.count());
        }
    }

    // Calcular media y desviación estándar de los tiempos iniciales
    double t_grover = 0.0, std_grover = 0.0;
    double sum = std::accumulate(times.begin(), times.end(), 0.0);
    t_grover = sum / times.size();
    std::cout << "Tiempo de ejecución promedio inicial: " << std::fixed << std::setprecision(12) << t_grover << " ms" << std::endl;
        if (times.size() > 1) {
            double sq_sum = std::accumulate(times.begin(), times.end(), 0.0,
                            [](double a, double b) { return a + b * b; });
            std_grover = std::sqrt(sq_sum / times.size() - (sum / times.size()) * (sum / times.size()));
            std::cout << "Desviación estándar inicial: " << std::fixed << std::setprecision(12) << std_grover << " ms" << std::endl;
        }
    

    // Verificar si el tiempo excede las 2.4 horas
    if (myid == 0 && t_grover > 8640000) { // 8640000 ms = 24 horas
        std::cout << "El algoritmo tarda más de un día en ejecutarse. Deteniendo la ejecución." << std::endl;
        stop_sampling = true;
        memory_sampler.join();
        return 0;
    }

    // Calcular el número óptimo de iteraciones
    int iterations_number = n_iterations_in;
    if (myid == 0 && t_grover > 0) {
        iterations_number = static_cast<int>(std::ceil(std::pow((2 * 1.96 * std_grover) / (0.05 * t_grover), 2)));
        std::cout << "Optimal number of iterations: " << iterations_number << std::endl;
    }

    // Sincronizar iterations_number entre procesos MPI
    //env.Bcast(&iterations_number, 1);

    // Ejecutar iteraciones adicionales si es necesario
    if (iterations_number > n_iterations_in) {
       for (int i = 0; i < iterations_number - n_iterations_in; ++i) { //i < iterations_number - n_iterations_in
            auto start = std::chrono::high_resolution_clock::now();
            run_simulation(psi);
            auto end = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double, std::milli> duration = end - start;
            if (myid == 0) {
                times.push_back(duration.count());
            }
        }
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
        std::cout << "Iteraciones óptimas: " << iterations_number << std::endl;

        // Obtener la fecha actual para el nombre del fichero
        auto now = std::chrono::system_clock::now();
        std::time_t now_time = std::chrono::system_clock::to_time_t(now);
        std::tm* tm_ptr = std::localtime(&now_time);
        char date_str[32];
        std::strftime(date_str, sizeof(date_str), "%Y-%m-%d_%H-%M-%S", tm_ptr);

        std::string filename = "Resultados/resultadosGrover";
        filename += std::to_string(num_qubits);
        filename += "_qubit_";
        filename += date_str;
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
                     << num_qubits << ","
                     << iterations_number << std::endl;
            csv_file.close();
        } else {
            std::cerr << "No se pudo abrir el fichero " << filename << " para escritura." << std::endl;
        }
    }

    return 0;
}

}