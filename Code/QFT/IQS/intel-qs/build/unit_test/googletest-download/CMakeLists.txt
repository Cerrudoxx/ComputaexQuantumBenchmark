cmake_minimum_required(VERSION 2.8.2)

project(googletest-download NONE)

include(ExternalProject)
ExternalProject_Add(googletest
  GIT_REPOSITORY    https://github.com/google/googletest.git
  GIT_TAG           main
  SOURCE_DIR        "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-src"
  BINARY_DIR        "/home/jesus-cerrudo/Escritorio/Computaex/TFG-Computaex/iqs-qft/intel-qs/build/unit_test/googletest-build"
  CONFIGURE_COMMAND ""
  BUILD_COMMAND     ""
  INSTALL_COMMAND   ""
  TEST_COMMAND      ""
)
