cantor(1,4)

function cant = cantor(l,n)
    if n == 1;
        cant = [l/3,2*l/3,l];
    else
        cant = [cantor(l,n-1) ./ 3, zeros(size(cantor(l,n-1))), l/3 + cantor(l,n-1) ./ 3];
    end
end

function draw(list)
    output=[]
    for i = 1:length(list)
        output =
        plot([list(i),list(i)],[0,1],'k-');
    end
end


