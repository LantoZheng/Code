function ins = insertf(x,y)
    f = @(t)0;
    if length(x)~=length(y)
        ins = 'error x,y size incooresbonding!';
        return
    end
    for i = 1:length(x)
        r = 1;
        s = @(t)1;
        for j = [1:i-1 i+1:length(x)]
            r = r*(x(i)-x(j));
            s = @(t)(s(t) * (t - x(j)));
        end
        k = @(t)(s(t) * y(i) / r(t));
        f = @(t)(f(t)+k(t));
    end
    ins = f;
end