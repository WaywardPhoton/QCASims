width_list = [2, 5, 10]; 
V_well_list = [0.3, 1, 10]; 
fig_num = 1;

for w=1:3
    for p=1:3
        eigenEs = finite_well(fig_num, width_list(w), V_well_list(p), 15, false);
        n = [1:1:length(eigenEs)];
        figure(fig_num),
        potential_name=strcat(num2str(V_well_list(p)),'eV') 
        if length(eigenEs) == 1
            hold on, graph(p) = plot(n, eigenEs(n), 'o', 'LineWidth',2,'DisplayName',potential_name);
        else
            hold on, graph(p) = plot(n, eigenEs(n), 'LineWidth',2,'DisplayName',potential_name);
        end
        set(gca,'FontSize',12)
    end
    legend(graph)
    graph = 0;
    fig_num = fig_num + 1;
end