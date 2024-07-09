draw_cantol(4)

function draw_cantol(n)    % 主函数,绘制康托尔集,n是迭代次数
    graph = cantol_set(n);  % 调用cantol_set函数生成康托尔集的坐标
    plot(graph(1,:),graph(2,:))  % 绘制康托尔集
end

function output = cantol_set(n)  % 递归函数,生成康托尔集的坐标
    if n == 0  % 返回初始线段的坐标
        output = double([0 , 1 ; 1 , 1]);
    else
        cant = cantol_set(n-1);  % 递归调用自身,生成上一次迭代的康托尔集坐标
        location = cant(1,end);  % 获取上一次迭代的康托尔集的最后一个点的x坐标
        shrinked = [cant(1,:) ./ 3 ; cant(2,:)];  % 将上一次迭代的康托尔集缩小为原来的1/3
        gap = [1/3,2/3;NaN,NaN];  % 生成中间空隙的坐标
        shrinked_plus = [shrinked(1,:) + 2/3;shrinked(2,:)];  % 将缩小后的康托尔集平移到右侧
        output = [shrinked,gap,shrinked_plus];  % 将左侧缩小的康托尔集、中间空隙和右侧平移后的康托尔集拼接起来
    end
end

%郑晓旸 202111030007

    