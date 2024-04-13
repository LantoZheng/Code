%get parameters of the system
charge = 1.6e-19;
r = 0.5;
center = [0,0];
region =[-2,2;-2,2]
% make meshgrid
grid_numbers = 1000
[X,Y] = meshgrid(linspace(region(1,1),region(1,2),grid_numbers),linspace(region(2,1),region(2,2),grid_numbers));
% calculate the charge distribution in meshes
% circle charge distribution

