Koch_plot(4,1)

function Koch_plot(n,l) %这个是主函数,n为迭代次数,l为初始线段长度
    S='F';              %初始字符串
    p='F+F--F+F';       %替换规则
    a=pi/3;             %旋转角度
    z=0;                %起始点坐标
    A=eps;              %起始角度
    for k=2:n           %迭代n次
        S=strrep(S,'F',p);%根据替换规则替换字符串
        l=(1/3)*l;      %每次迭代,线段长度缩短为原来的1/3
    end
    seq_plot(S,z,A,a,l) %调用seq_plot,之后定义
end

function seq_plot(seq,z,A,a,n)
    figure;             %创建一个新的图形窗口
    axis equal;         %使坐标刻度长度相等
    hold on             
    for k=1:length(seq) %遍历字符串中的每个字符
        switch seq(k)
            case'F'     %绘制一条线段
                plot([z,z+n*exp(1i*A)]);
                z=z+n*exp(1i*A);
            case'+'
                        %逆时针旋转a度
                A=A+a;
            case'-'
                        %顺时针旋转a度
                A=A-a;
            otherwise
        end
    end
end


%郑晓旸 202111030007