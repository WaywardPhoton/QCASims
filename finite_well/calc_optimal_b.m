%Selecting b
width_list = [2, 5, 10]; 
V_well_list = [0.3, 1, 10]; 
fig_num = 1;

for p=1:3
    for w=1:3
        lasteigenEs = finite_well(fig_num, width_list(w), V_well_list(p), 10, false);

        for b = 11:100
            eigenEs = finite_well(fig_num, width_list(w), V_well_list(p), b, false);

            if abs((norm(eigenEs)-norm(lasteigenEs))) < 1E-5
                break
            end

            lasteigenEs = eigenEs;
        end
        b_vals(fig_num) = b;
        fig_num = fig_num + 1;
    end
end

b_vals
b_final = max(b_vals)
    

b = 5;    

b = 10;    
%eigenEs = finite_well(2, width_list(1), V_well_list(3), 10)
b = 30;    
%eigenEs = finite_well(3, width_list(1), V_well_list(3), 30)
b = 50;    
%eigenEs = finite_well(4, width_list(1), V_well_list(3), 50)

