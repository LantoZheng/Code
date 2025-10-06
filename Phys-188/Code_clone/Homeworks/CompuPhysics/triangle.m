
a = 2/3 * pi;
figure;
draw(4, 1, 0);
axis equal;
function draw(n, l, loc)
    hold on;
    if n == 1
        str = 'F+F+F+';
        A = 0;
        for k = 1:length(str)
            if str(k) == 'F'
                new_loc = loc + l * exp(1i * A);
                plot([real(loc), real(new_loc)], [imag(loc), imag(new_loc)]);
                loc = new_loc;
            elseif str(k) == '+'
                A = A + a;
            end
        end
    else
        step = l / 2;
        draw(n-1, step, loc);
        draw(n-1, step, loc + step);
        draw(n-1, step, loc + step * exp(1j * pi/3));
    end
end

%该函数用于绘制凯宾斯基分型三角形，但是不报错且无法绘制图像

