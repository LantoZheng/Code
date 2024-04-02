C0=[0,i,0.3+0.5i,0.11+0.66i];  %迭代式中的常数，可改变
for k=1:4
    C=C0(k);
    V=linspace(-2.0,2.0,400); %复数的范围及取点数
    [Re,lm]=meshgrid(V);
    Z=Re+i*lm;  %复平面上所有起始点
    B=0;
    for K=1:100 %迭代100次
        Z=Z.*Z+C;
        B=B+(abs(Z)<=3); %记录已经逃离的判据
    end;
end
imagesc(B); %表示成颜色图形
colormap(jet);
axis equal


%% 
C0=[3,i,0.3+0.5i,0.11+0.66i];    
v= linspace(-2,2,500);
[Re,Im] = meshgrid(V)
Z= Re + Im*i;    
B = 0;
for k = 1:100
    Z = Z.*Z + C0(mod(k,4)+1);
    B = B + (abs(Z)<=3);
end;
imagesc(B); %表示成颜色图形
colormap(jet);
axis equal
%%
k = [1,2,3,4,5];
diffrential=diff(k)

function out = diff(a)
    forward = a(2:end);
    local = a(1:end-1);
    out = forward - local;
end

%%

