RGB = imread("weihnachtsbaum.jpg");
imshow(RGB);
RGB = double(RGB);
r1 = rank(RGB(:,:,1));
r2 = rank(RGB(:,:,2));
r3 = rank(RGB(:,:,3));
[U1, S1, Vt1] = svd(RGB(:,:,1));
[U2, S2, Vt2] = svd(RGB(:,:,2));
[U3, S3, Vt3] = svd(RGB(:,:,3));

k = r1;
for i = (k+1):r1
    S1(i,i) = 0;
    S2(i,i) = 0;
    S3(i,i) = 0;
end
R = uint8(U1*S1*(Vt1'));
G = uint8(U2*S2*(Vt2'));
B = uint8(U3*S3*(Vt3'));

[m, n, o] = size(RGB);
RGB_2 = zeros(m, n, 3);

RGB_2(:,:,1) = R;
RGB_2(:,:,2) = G;
RGB_2(:,:,3) = B;
imshow(uint8(RGB_2));

sqrt(sum((RGB - RGB_2).^2, "all"))
sqrt(sum((RGB - RGB_2).^2, "all")) / sqrt(sum(RGB.^2, "all"))