%Minkowski_plot(3,1)

function Minkowski_plot(n,l)%这个是主函数,n为迭代次数,l为初始线段长度
    S='F';%初始元
    p='F+F-F-FF+F+F-F';%替换规则
    a=pi*3/2;%旋转角度
    z=0;%起始点坐标
    A=2*pi;%起始角度
    for k=1:n%迭代n次
        S=strrep(S,'F',p);%根据替换规则替换字符串
        l=(1/4)*l;%每次迭代,线段长度缩短为原来的1/4
    end
    seq_plot(S,z,A,a,l)%调用seq_plot函数绘制Minkowski曲线
end

function seq_plot(seq,z,A,a,n)
    figure;%创建一个新的图形窗口
    axis equal;%使坐标刻度长度相等
    hold on%保持图形,便于在同一图形上绘制多条曲线
    for k=1:length(seq)%遍历字符串中的每个字符
        switch seq(k)
            case'F'%若为'F',则绘制一条线段
                plot([z,z+n*exp(1i*A)]);%绘制从z到z+n*exp(1i*A)的线段
                z=z+n*exp(1i*A);%更新当前点的坐标
            case'+'%若为'+',则逆时针旋转a度
                A=A+a;
            case'-'%若为'-',则顺时针旋转a度
                A=A-a;
            otherwise
        end
    end
end
