f = @(x)(4*cos(x)-exp(x));
root_binary = binary(f,pi/2,pi/4,1/10000)
newton_root = newton(f,pi/4,1/10000)
cutline_root = cutline(f,pi/2,pi/4,1/10000)
fzero_root = fzero(f,[pi/4 pi/2])

% 对分法求零点
function ret = binary(f,a,b,tol)
    if f(a)*f(b) > 0
        ret = 'Error,value with same sign';
    end
    while abs(a-b) > tol
        c = (a + b) / 2;
        if f(a) * f(c) < 0
            b = c;
        elseif f(b)*f(c) < 0
            a = c;
        else
            ret = c;
        end
    end
    ret = c;
end
%牛顿法求零点
function ret = newton(f,a,tol)
    sol = a;
    prev = a + 2*tol;
    while abs(sol - prev) > tol
        slope = (f(a+eps)-f(a))/eps;
        prev = sol;
        sol = sol - f(sol)/slope; 
    end
    ret = sol;
end

%切线法求根
function ret = cutline(f,a,b,tol)
    if f(a)*f(b) > 0
        ret = 'Error,value with same sign';
    end
    while abs(a-b) > tol
        c = a - f(a)*(a-b)/(f(a)-f(b));
        a = b;
        b = c;
    end
    ret = c;
end