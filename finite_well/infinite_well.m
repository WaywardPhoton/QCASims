function Ean = infinite_well(w)
    %INFINITE_WELL Summary of this function goes here
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
    t0=(hbar^2)/(2*m*(a^2))/q;
    L=w*10^-9;
    T=(2*t0*diag(ones(1,Np)))-(t0*diag(ones(1,Np-1),1))-(t0*diag(ones(1,Np-1),-1));
    [V,D]=eig(T);D=diag(D);[Enum,ind]=sort(D);
    
    E1=D(ind(1))
    psi1=abs(V(:,ind(1)));
    P1=psi1.*conj(psi1);
    
    E2=D(ind(10))
    psi2=abs(V(:,ind(10)));
    P2=psi2.*conj(psi2);
    
    %analytical eigenvalues
    Ean=(((hbar*pi)^2)/(2*m_eff*(L^2))/q)*[1:14].*[1:14]
    hold on
    
    %p=plot(Enum,'bx');% Part (a)
    %p=plot(Ean,'b');% Part (a)
    %h=plot(P1,'b');% Part (b)
    %h1=plot(P2,'b');% Part (b)
    set(h,'linewidth',[3.0])
    set(h1,'linewidth',[1.0])
    set(gca,'Fontsize',[25])
    %xlabel('Eigenvalue Number , m --->');% Part (a)
    %ylabel('E (eV) --->');% Part (a)
    xlabel(' Lattice site # ---> ');% Part (b)
    ylabel(' Probability ---> ');% Part (b)
    grid on
end

