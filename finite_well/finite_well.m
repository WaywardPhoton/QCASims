function eigenEs = finite_well(fig_num, w, p, b, plot_gen)
    %Unit Definitions
    kg = 1;
    J = 1;
    C = 1;
    s = 1;
    m = 1;
    
    q = 1.602e-19 * C;
    eV = q * C * J;
    nm = 1E-9 * m;
    
    %Constants
    hbar=1.055e-34 *(J*s);
    m_e=9.110e-31 *(kg);
    m_eff=0.067*m_e *(kg);
    
    %Potential Well
    width = w *(nm);
    b = b *(nm); 
    tot_length = 2*b + width; %nm
    
        %Discretization
        dx = 0.1 *(nm);
        x = [-tot_length/2:dx:tot_length/2];  
    
    
    V = zeros(length(x),1);
    V(x<-width/2) = p;
    V(x>+width/2) = p;
    
    if plot_gen
        figure(fig_num), plot(x/nm, V,'k'),grid on
        xlabel('x [nm]'),ylabel('V [eV]')
    end
    
    %Hamiltonian
    t0 = (hbar^2)/(2*m_eff*(dx^2))/eV;
    T = ((2*t0+V).*diag(ones(1,length(x))))-(t0.*diag(ones(1,length(x)-1),1))-(t0.*diag(ones(1,length(x)-1),-1));
    [e,D]=eig(T);
    
    % Energy States
    sols = sum(diag(D)<p);
    if plot_gen
        figure(fig_num),
    end
    for sol = 1:sols
        En = D(sol,sol);
        psi = e(:,sol);
        scaling_factor = 0.5;
        
        if plot_gen
            psi_name=strcat('\Psi',num2str(sol)); 
            hold on, graph(sol) = plot(x/nm, psi*scaling_factor+En, 'LineWidth',2,'DisplayName',psi_name);
            hold on, plot(x/nm, En*ones(length(x)), '--k', 'LineWidth',1)
            
            
            set(gca,'FontSize',12)
        end
        
        eigenEs(sol) = En;
    end
    
    if plot_gen
        legend(graph)
    end
    
end

