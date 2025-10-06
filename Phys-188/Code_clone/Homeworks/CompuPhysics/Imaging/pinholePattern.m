function diffraction_pattern = pinholePattern(lambda_nm, z, a, d, screen_size, L)
% lambda: 光的波长，单位为nm
% z: 点光源与小孔的水平距离，单位为mm
% a: 小孔半径，单位为mm
% d: 小孔到成像屏的距离，单位为mm
% screen_size: 成像屏大小，单位为mm
% L: 成像屏分辨率

% 将波长从nm转换为mm
lambda = lambda_nm * 1e-6; % 1 nm = 1e-6 mm
N = screen_size/d;%空间范围
[x, y]=meshgrid(linspace(-N,N,L));%网格
% 菲涅尔衍射-圆孔
%  三维--快速傅里叶变换
z=a^(2)*pi/4/lambda*100;
z1=zeros(L,L);
z2=zeros(L,L);
for i =1:L
    for j =1:L
        if x(i,j)^2+y(i,j)^2<=a
            z1(i,j)=1;
            z2(i,j)=x(i,j)^2+y(i,j)^2;
        end
    end
end
d=fftshift(abs((fft2(z1.*exp(1i*2*pi/lambda/2/z*z2))).^2));
i_2=d.^2;
diffraction_pattern = i_2/sum(i_2,'all');
end