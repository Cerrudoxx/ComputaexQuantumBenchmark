// Include the header file including the declaration of the QubitRegister class.
#include "../include/qureg.hpp"


int main (int argc, char **argv)
{
  // Create the MPI environment, passing the same argument to all the ranks.
  iqs::mpi::Environment env(argc, argv);
  // qHiPSTER is structured so that only even number of ranks are used to store
  // and manipulate the quantum state. In case the number of ranks is not supported,
  // try to decrease it by 1 until it is.
  if (env.IsUsefulRank() == false) return 0;
  // qHiPSTER has functions that simplify some MPI instructions. However, it is important
  // to keep trace of the current rank.
  int myid = env.GetRank();
  
  int N = 4; // Number of qubits in the quantum register.
  std::size_t tmpSize = 0;

  if (myid == 0) printf("\n --- GROVER ATTEMPT --- \n");
  int Ngrover = 4;

  iqs::QubitRegister<ComplexDP> psig(Ngrover, "base", 0);
  psig.Print("Initial State =");

  for (unsigned q = 0; q < Ngrover; ++q)
  {
      psig.ApplyHadamard(q);
  }
  psig.ApplyHadamard(Ngrover - 1);
  psig.ApplyCPauliX()
  // TODO: Oracle

  return 0;
}