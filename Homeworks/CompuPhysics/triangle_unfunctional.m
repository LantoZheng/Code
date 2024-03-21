a = 2/3*pi;
A = eps;
hold on

draw(2,1,0)
r=1
function draw(n,l,loc)
    if n == 1 
        str="F+F+F+";
        for i = 1:length(str)
            switch str(i)
                case 'F'
                    plot([loc,loc+l*exp(i*A)])
                    loc=loc+l*exp(i*A);
                case '+'
                    A=A+a;
                otherwise
            end
        end
    else
        step = l/2;
        draw(n-1,step,loc)
        draw(n-1,step,loc+step)
        draw(n-1,step,loc+step*exp(i*pi/3))
    end 
end

