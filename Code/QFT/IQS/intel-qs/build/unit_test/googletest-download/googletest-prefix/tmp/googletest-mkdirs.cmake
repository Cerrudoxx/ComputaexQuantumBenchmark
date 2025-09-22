# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-src"
  "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-build"
  "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-download/googletest-prefix"
  "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-download/googletest-prefix/tmp"
  "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-download/googletest-prefix/src/googletest-stamp"
  "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-download/googletest-prefix/src"
  "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-download/googletest-prefix/src/googletest-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-download/googletest-prefix/src/googletest-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-download/googletest-prefix/src/googletest-stamp${cfgdir}") # cfgdir has leading slash
endif()
