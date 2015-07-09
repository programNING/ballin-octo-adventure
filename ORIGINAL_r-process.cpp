/// \file r-process.cpp
/// \author jlippuner
/// \since Sep 3, 2014
///
/// \brief
///
///

#include "BuildInfo.hpp"
#include "EquationsOfState/HelmholtzEOS.hpp"
#include "Network/ReactionNetwork.hpp"
#include "Network/NSE.hpp"
#include "DensityProfiles/ExpTMinus3.hpp"
#include "Reactions/REACLIBReactionLibrary.hpp"
#include "Reactions/Neutrino.hpp" 
#include "Reactions/NeutrinoReactionLibrary.hpp" 

#include <iostream>
#include <fstream>
#include <cstring>

int main(int argc, char *argv[]) {
  auto nuclib = NuclideLibrary::CreateFromWebnucleoXML(
      SkyNetRoot + "/data/webnucleo_nuc_v2.0.xml");

  NetworkOptions opts;
  opts.ConvergenceCriterion = NetworkConvergenceCriterion::Mass;
  opts.MassDeviationThreshold = 1.0E-10;
  opts.IsSelfHeating = true;
  opts.NetworkEvolutionMaxT9 = 1.E1; 

  REACLIBReactionLibrary weakReactionLibrary(SkyNetRoot + "/data/reaclib",
      ReactionType::Weak, false, "Weak reactions", nuclib, opts);
  REACLIBReactionLibrary strongReactionLibrary(SkyNetRoot + "/data/reaclib",
      ReactionType::Strong, true, "Strong reactions", nuclib, opts);
  REACLIBReactionLibrary symmetricFission(SkyNetRoot +
      "/data/netsu_panov_symmetric_0neut", ReactionType::Strong, false,
      "Symmetric neutron induced fission with 0 free neutrons", nuclib, opts);
  REACLIBReactionLibrary spontaneousFission(SkyNetRoot +
      "/data/netsu_sfis_Roberts2010rates", ReactionType::Strong, false,
      "Spontaneous fission", nuclib, opts);
  NeutrinoReactionLibrary neutrinoLibrary("neutrino_reactions.dat", ReactionType::Weak,
      "Neutrino Reactions", nuclib, opts);

  HelmholtzEOS helm(SkyNetRoot + "/data/helm_table.dat");

  ReactionNetwork net(nuclib, { &weakReactionLibrary, &strongReactionLibrary,
      &symmetricFission, &spontaneousFission, &neutrinoLibrary }, &helm, opts);
  
  // might wanna add multiple files for loop

  double T0 = 50.0;
  double Ye = 0.05;
  double s = 10.0;
  double tau = 10.0;

  double ENUE = 12.0; // wont work w const double?
  double ENUB = 12.0;
  double LNUE = 1.e53;
  double LNUB = 1.e53;
  double IRAD = 1.e8;
  double FRAD = 1.e8;

  char filename[50] = "baseinputs"

  if (argc > 1) 
  {
    std::fstream infile;
    infile.open(argv[1], ios::in);
    if (infile.is_open()) 
    {
      infile.getline(filename, 50, '\n');
      infile >> T0;
      infile >> Ye;
      infile >> s;
      infile >> tau;
      infile >> ENUE;
      infile >> ENUB;
      infile >> LNUE;
      infile >> LNUB;
      infile >> IRAD;
      infile >> FRAD;
      infile.close();
    }
    else 
    {
      std::cout << "Could not open file.";
    }

  std::unique_ptr<NeutrinoHistory> nuHist( new NeutrinoHistoryThermal (
      LNUE, ENUE, LNUB, ENUB, {0.0, 1.e20}, {IRAD, FRAD}, false) );
  
  net.LoadNeutrinoHistory(nuHist);
  
  // run NSE with the temperature and entropy to find the initial density
  
  auto nseResult = NSE::CalcFromTemperatureAndEntropy(T0, s, Ye,
    net.GetNuclideLibrary(), &helm);

  auto densityProfile = ExpTMinus3(nseResult.Rho(), tau / 1000.0);

  auto output = net.EvolveSelfHeatingWithInitialTemperature(nseResult.Y(), 0.0,
      1.0E9, T0, &densityProfile, filename);

  std::vector<double> finalYVsA = output.FinalYVsA();

  FILE * f = fopen(strcat(filename, "_final_y"), "w");
  for (unsigned int A = 0; A < finalYVsA.size(); ++A)
    fprintf(f, "%6i  %30.20E\n", A, finalYVsA[A]);
}

