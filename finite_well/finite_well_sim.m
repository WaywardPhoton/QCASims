width_list = [2, 5, 10]; 
V_well_list = [0.3, 1, 10]; 
fig_num = 1;

for p=1:3
    for w=1:3
        eigenEs = finite_well(fig_num, width_list(w), V_well_list(p), 15, true)

        fig_num = fig_num + 1;
    end
end