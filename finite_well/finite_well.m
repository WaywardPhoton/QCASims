function [outputArg1,outputArg2] = finite_well(inputArg1,inputArg2)
    %FINITE_WELL Summary of this function goes here
    %   Detailed explanation goes here
    
    %Constants (all MKS, except energy which is in eV)
    hbar=1.055e-34;
    m=9.110e-31;
    m_eff=0.067*m;
    epsil=8.854e-12;
    q=1.602e-19;
    
    %Lattice
    Np=100;
    a=1e-10;
    X=a*[1:1:Np];
    
end

