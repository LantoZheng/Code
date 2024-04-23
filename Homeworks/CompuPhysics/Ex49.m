p = [1,-4,-6,-16,4];
root = limit(getreal(roots(p)),-1,4)
mini_position = getreal(roots(polyder(p)));
mini = (polyval(polyder(polyder(p)),mini_position)>=0);
mini_position = limit(mini_position(mini),-1,4)
minival = polyval(p,mini_position)

function ret = limit(x,a,b)
    position = ((x>=a) & (x<=b));
    ret = x(position);
end

function ret = getreal(x)
    position = (imag(x)==0);
    ret = x(position);
end