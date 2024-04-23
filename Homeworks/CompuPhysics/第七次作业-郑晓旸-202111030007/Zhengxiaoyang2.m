% All geographic values are multipuls of 'a' , and all charge are the
% multipuls of 'q'
% Building meshgrid
x = linspace(-10,10,200);
z = linspace(-10,10,100);
the = linspace(0,2*pi,100);
[X,Z,T] = meshgrid(x,z,the);
% Caculating range of charge infinitary
% caculating position of chage infinitary
x_charge = cos(T);
y_charge = sin(T);
r = sqrt((X-x_charge).^2 + y_charge.^2 + Z.^2);
% Caculate the potential at each point
dU = 1/100 .* r.^(-1);
U = trapz(dU,3);
[E_x,E_z] = gradient(U);

contourf(X(:,:,1),Z(:,:,1),U,'LevelList',linspace(min(min(U)),max(max(U))-0.2,30))
hold on
quiver(X(:,:,1),Z(:,:,1),E_x,E_z,5)

xlabel('r-direction(a)')
ylabel('z-direction(a)')
title('Electic field of a ring charge')
axis equal
hold off