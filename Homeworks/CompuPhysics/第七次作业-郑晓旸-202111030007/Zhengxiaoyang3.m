% Preperations
format long;
Func = @(x) cos(log(x)./x)./x;
T_k = [];
k = 1;
T=0;
t=1;
N = 0;
n=100;
% Part 1&2: Caculating T_k then get T
    % finding zero points
    X_k=[1];
% In this part we can find out that approximated accuracy is 10e-10
while abs(T-t)>=10e-10
    t = T;
    for i = N+1:n
        f = @(x)log(x)/x+(i-1/2)*pi;
        x = fzero(f,[eps 1]);
        X_k(i+1) = x;
    end
    % Caculating T_k
    for i = N+1:n
        T_k(i) = integral(Func,X_k(i+1),X_k(i));
    end
    T = 1/2*(sum(T_k(1:end))+sum(T_k(1:end-1)));
    N = n;
    n = 2*n;
end
T
%%
% Part 3: Aitken acceleration method
% SRDS 书中给出的Aitken加速方法并不能求出积分值，Aitken方法的正确表达式应当按如下方法书写。
% \tilta{T}_k=\sum_1^n T_k + (T_k - T_{k-1})^2/(T_k-2*T_{k-1}+T_{k-2})。
% 接下来，我们用正确的方法计算。
format long;
Func = @(x) cos(log(x)./x)./x;
f = @(c)@(x)log(x)/x+(c-1/2)*pi;  
n=2;
x = fzero(f(1),[eps 1]);
T = integral(Func,x,1);
T_k = T;
T_tilta = [0 1];
while abs(T_tilta(length(T_tilta))-T_tilta(length(T_tilta)-1)) >= 10e-15
    x(n) = fzero(f(n),[eps 1]);
    T_k(n)= integral(Func,x(n),x(n-1));
    T(n) = T(n-1) + T_k(n);
    T_tilta(n) = T(n) - T_k(n)^2/(T_k(n)-T_k(n-1));
    n = n+1; 
end
T_tilta(length(T_tilta))










