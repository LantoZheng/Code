S='F+F+F';%初始元
p='F+F+F+FF';%生成元
a=2*pi/3;%转角
z=0;
A=eps;%起点与方向角
for k=2:4 %迭代次数
    S=strrep(S,'F',p); %用生成元替代初始元
    n=(1/3)^(k-1);%压缩比
end
figure;
axis equal;
hold on
for k=1:length(S)
    switch S(k);
        case 'F'
            plot([z,z+n*exp(i*A)],'linewidth',2);
            z=z+n*exp(i*A);%新起点
        case '+'
            A=A+a;
        otherwise
    end%退出
end

