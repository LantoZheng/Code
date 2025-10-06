function wavelength = rgb2wavelength(rgb)
    % 将RGB值转换为波长
    % R, G, B: RGB值，范围从0到255
    % wavelength: 波长，单位为纳米

    % 将RGB值归一化到0到1之间
    R = rgb(1) / 255;
    G = rgb(2) / 255;
    B = rgb(3) / 255;

    % 根据RGB值估算波长
    if R == 0 && G == 0 && B == 0
        wavelength = NaN; % 黑色，没有对应的波长
        return;
    end

    % 色度坐标系
    X = 0.4124*R + 0.3576*G + 0.1805*B;
    Y = 0.2126*R + 0.7152*G + 0.0722*B;
    Z = 0.0193*R + 0.1192*G + 0.9505*B;

    % 色品坐标
    x = X / (X + Y + Z);
    y = Y / (X + Y + Z);

    % 近似波长计算（仅适用于可见光范围）
    if x >= 0.167 && x <= 0.408
        wavelength = -1500*x + 2200*y + 440;
    elseif x > 0.408 && x <= 0.625
        wavelength = -4600*x + 1800*y + 680;
    else
        wavelength = NaN; % 超出范围
    end
end

%Ref:
% Wyszecki, G., & Stiles, W. S. (2000). Color Science: Concepts and Methods, Quantitative Data and Formulae. Wiley.
% Smith, T., & Guild, J. (1931). The C.I.E. colorimetric standards and their use. Transactions of the Optical Society, 33(3), 73.