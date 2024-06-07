x = 0:0.01:1;
t = 0:0.01:100;
[X,T] = meshgrid(x,t);

a = -1;
A = 10;
omega = 0.3;
ult = A*sin(omega .* t);
u0t = zeros(size(t));
ux0 = zeros(size(x));

u = zeros(size(X));
u(1,:)=ux0;
u(:,1) = u0t;
u(:,end) = ult;

for i = 3:1001
    u(i,2:100) = 2*u(i-1,2:100)-u(i-2,2:100)+a*(u(i-2,3:101)-2*u(i-2,2:100)+u(i-2,1:99));
    plot(x,u(i,1:101));
    pause(0.1)
end

%% 

