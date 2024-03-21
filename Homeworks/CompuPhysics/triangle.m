
turn=exp(2/3*pi*i)

draw(1,1,0)

function draw(n,l,loc)
    switch n
        case 1
            drawlines('F+F+F',l,loc)
        otherwise
            draw(n-1,l/2,loc)
            draw(n-1,l/2,loc+l/2)
            draw(n-1,l/2,loc+l/2*exp(pi/3*i))
    end 
end

function drawlines(str,step,location)
    for i = 1:length(str)
        switch str(i)
            case 'F'
                forward=[location,location+step];
                location=location+step;
                plot(forward)
            case '+'
                step=step*turn;
        end
    end
end


