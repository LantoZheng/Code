%test code

k=[];
for i = 1:10
    k(i)=fippo(i);
end
k

function y = fippo(n)
    switch n
        case 1
            y=1;
        case 2
            y=1;
        otherwise
            y = fippo(n-1)+fippo(n-2);
    end
end
%Computational Physics Homework 2 By 郑晓旸 202111030007