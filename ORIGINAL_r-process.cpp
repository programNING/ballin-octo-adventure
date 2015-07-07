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

int main(int, char**) {
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

  double T0 = 1.0;
  double Ye = 0.3;
  double s = 10.0;
  double tau = 15.0;
  
  const double ENUE = 12.0; 
  const double ENUB = 12.0; 
  const double LNUE = 1.e53; 
  const double LNUB = 1.e53;
  const double RAD  = 1.e8; 
  std::unique_ptr<NeutrinoHistory> nuHist( new NeutrinoHistoryThermal (
      LNUE, ENUE, LNUB, ENUB, {0.0, 1.e20}, {RAD, RAD}, false) );
  
  net.LoadNeutrinoHistory(nuHist);
  
  // run NSE with the temperature and entropy to find the initial density
  auto nseResult = NSE::CalcFromTemperatureAndEntropy(T0, s, Ye,
    net.GetNuclideLibrary(), &helm);

  auto densityProfile = ExpTMinus3(nseResult.Rho(), tau / 1000.0);

  auto output = net.EvolveSelfHeatingWithInitialTemperature(nseResult.Y(), 0.0,
      1.0E9, T0, &densityProfile, "SkyNet_r-process");

  std::vector<double> finalYVsA = output.FinalYVsA();

  FILE * f = fopen("final_y_r-process", "w");
  for (unsigned int A = 0; A < finalYVsA.size(); ++A)
    fprintf(f, "%6i  %30.20E\n", A, finalYVsA[A]);
}

