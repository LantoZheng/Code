a = 2/3*pi;
A = 0;

lines = draw(2,1,0)

function plot_list=draw(n,l,loc)
    if n == 1 
        str="F+F+F+";
        for k = 1:length(str)
            switch str(k)
                case 'F'
                    add = [loc,loc+l*exp(i*A)]
                    plot_list = [plot_list;add]
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

