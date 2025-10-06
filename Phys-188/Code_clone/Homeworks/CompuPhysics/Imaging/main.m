%构建空间片元数据集，上色（绘制一个Imobject的圣诞树）
tree = imObject();
r1 = 15;%树干半径
r2 = 40;%树枝半径
h1 = 80;%树干高度
h2 = 100;%树枝高度
basedots = [r1 .* cos(2.*pi.*(1:10)./10);r1 .* sin(2.*pi.*(1:10)./10);zeros(1,10)]';%树干底部点
upperdots =  [r1 .* cos(2.*pi.*(1:10)./10 + pi/10);r1 .* sin(2.*pi.*(1:10)./10 + pi/10);h1.*ones(1,10)]';%树干上部点
treedots =  [r2 .*cos(2.*pi.*(1:10)./10);r2 .*sin(2.*pi.*(1:10)./10);h1.*ones(1,10)]';%树枝下部点
topdots = [0 0 h1+h2];%树顶点
tree.points = [basedots;upperdots;treedots;topdots;[0 0 0]];%所有点

for i = 1:10%间隔构建三角形面片
    nextIndex = mod(i, 10) + 1;
    tree.slides(i,:) =  [i,10+i,nextIndex];
    tree.slides(i+10,:) =  [10+i,nextIndex,10+nextIndex];
    tree.slides(i+20,:) =  [i+20,10+i,nextIndex+20];
    tree.slides(i+30,:) =  [10+i,20+nextIndex,10+nextIndex];
    tree.slides(i+40,:) = [31,20+i,20+nextIndex];
    tree.slides(i+50,:) = [32,i,nextIndex];
end

tree.additional.activate = true;%启用附加特性
tree.additional.brightness = ones(1,size(tree.slides,1));%固定所有面片亮度（反射率）相等
tree.additional.color = [[128.*ones(20,1) 42.*ones(20,1) 42.*ones(20,1)];[0.*ones(30,1) 201.*ones(30,1) 87.*ones(30,1)];[128.*ones(10,1) 42.*ones(10,1) 42.*ones(10,1)]];%树干部分面片为棕色（128，42，42），树枝部分为绿色（0，201，87）

tree = tree.move(0,150,-50);%将三维模型移动到y轴100mm处


%构建屏幕空间
r = 2;%小孔半径
d = 20;%屏幕到小孔距离
screenSize = 50;%屏幕尺寸
dots = 3000;%屏幕分辨率
dotSize = screenSize/dots;
[X,Y] = meshgrid(dotSize .*(1-dots/2:dots/2),dotSize .*(1-dots/2:dots/2));%屏幕空间坐标
Image = zeros([size(X),3]);%初始化屏幕空间亮度

%划分深度组
n = 5; %划分组数
group = tree.SlidesGroupByDistance([0 0 0],5);



%绘制点投影深度图
for i = 1:n
    ImageTemp = zeros([size(X),3]);
    slideIndices = group(i).index;
    for j = 1:length(slideIndices)
        slide = tree.slides(slideIndices(j), :);
        % 获取面片的三个顶点
        p = tree.points(slide, :);

        % 投影到屏幕空间
        screenP = [-(p(:,1) ./ p(:,2)) .* d, -(p(:,3) ./ p(:,2)) .* d];

        % 转换到像素坐标
        screenPixelP = round((screenP + screenSize ./ 2) ./ dotSize);

        % 确保投影点在屏幕范围内
        if all(screenPixelP > 0 & screenPixelP <= dots)
            % 获取三角形顶点的列和行坐标
            cols = screenPixelP(:,1);
            rows = screenPixelP(:,2);

            % 使用poly2mask创建三角形掩码
            mask = poly2mask(cols, rows, dots, dots);
            mask = reshape(mask,[dots,dots,1]);
            % 渲染亮度
            for k = 1:3
                adding = mask .* tree.additional.color(slideIndices(j),k).*tree.additional.brightness(slideIndices(j));%获取图像片元的色度数据
                ImageTemp(:,:,k) = ImageTemp(:,:,k) + adding;%将色度数据叠加到色彩空间中
            end
        end
    end
    meanColor = mean(tree.additional.color(group(i).index,:),1);
    lambda = rgb2wavelength(meanColor);%根据片元的色彩数据推算其波长
    kernel1 = pinholePattern(lambda,group(i).distance,r,d,screenSize/10,dots/10);%根据片元距离和小孔性质，计算片元衍射班形状
    kernel2 = ones(round(r/dotSize) + 1);%几何光学光斑
    for channel = 1:3%分别使用两种光斑在RGB图像空间中进行卷积，模拟光学因素引起的模糊
        ImageTemp(:,:,channel) = conv2(reshape(ImageTemp(:,:,channel),[dots,dots]),kernel1,'same');
        ImageTemp(:,:,channel) = conv2(reshape(ImageTemp(:,:,channel),[dots,dots]),kernel2,'same');
    end
    Image = Image + ImageTemp;
    mask = d./sqrt(X.^2 + Y.^2 + d^2);%产生由余弦分布产生的暗角滤镜
    Image = Image .* mask; %使用滤镜
end
imshow(Image)








