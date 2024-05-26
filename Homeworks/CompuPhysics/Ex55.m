%矩阵方法
syms k m M
JK = [k,-k,0; -k,2*k,-k; 0,-k,k];
JM = [m,0,0; 0,M,0; 0,0,m];
[JS,JB] = eig(JM\JK);
BS1 = dsolve("D2y = -k/m*y");  % 求解用本征值构成的三个本征方程
BS2 = dsolve("D2y = -k*(M+2*m)/M/m*y");
BS3 = dsolve("D2y = 0");
Bw = sqrt(JB);
BW = subs(Bw,{m,M,k},{3,4,50});
w = double(diag(BW))

%解微分方程
global m M k
m = 1;M = 2;k=1;
x0 = [0.2;0.35;-0.3;0;0;0];

[t,u] = ode45(dydt,[0,40],x0);
hold on
title('耦合振动');
xlabel('time(s)');
ylabel('Distance(m)');
plot(t(1:2000),u(1:2000))

function dy = dydt(t,y)
    global m M k
    dy = [y(4); y(5); y(6); -k*(y(1)-y(2))/m; -k(y(1)+2*y(2)-y(3))/M;-k(y(3)-y(2))/m];
end
