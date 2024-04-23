% Units of All numbers are in International Standard Units 
v_p = 1578;
% Part 1
p = partition(0,1*v_p);
['从0~v_p的分子数占比为' , string(p) ]
% Part 2
p = partition(0,3.3*v_p);
['从0~3.3v_p的分子数占比为' , string(p) ]
%Part 3
p = partition(3e4,3e8);
['从3e4~3e8的分子数占比为' , string(p) ]
function P = partition(v_1,v_2)
    % 给定参数和特定函数
    v_p = 1578;
    k = 2/v_p.^2;
    f_v = @(v) 4/pi^(1/2) .* (v.^2 ./ v_p^3) .* exp(-v.^2 ./ v_p^2);
    %计算V_1~v_2的分子数占比
    P = integral(f_v,v_1,v_2,'RelTol',10e-8);
end