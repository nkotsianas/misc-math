    
    close all;
    clear all;
    
    % Put the path to the picture you want to analyze here.
    % If a path is not specified, will assume the current matlab path.
    imagepath = 'fusedsilica.png';
    
    % ------------------------------------------------------------------- %
    %      PLEASE CROP YOUR PICTURE SO THAT THE PIXELS ON THE BORDER      %
    %            CORRESPOND TO THE BOUNDARIES OF THE PLOT AREA            %
    % ------------------------------------------------------------------- %
    
    
    % Put the RGB triple for the color of your curve here.
    % You can also put tolerance values for each individual RGB.
    % (black = 0, white = 255)
    curve_color = [128,50,50];
    curve_color_tol = [128,50,50];
    % For example '[0,0,128]' and '[5,5,8]' will match colors between
    %   [0,0,120] and [5,5,136], which is a dark blue.
    % This works well for Bayer's Bayfol HX 102 transmission plot.
    
    
    % The x,y min and max values on the axes of your plot.
    xmin = 210; xmax = 3710; xunit = 'Wavelength (nm)';
    ymin = 1.375; ymax = 1.55; yunit = 'Index of Refraction, n';
    
    
    % We will print the x,y data to a file for reading/using later.
    % If a path is not specified, will print to the current path.
    filepath = 'datafile.txt';
    
    % We will also print the number of bytes written to the file
    %   at the MATLAB console when the program is finished.
    
    
    % ------------------------------------------------------------------- %
    % ------------------- THE PROGRAM'S CODE IS BELOW ------------------- %
    % --------------------- PLEASE DON'T MODIFY IT! --------------------- %
    % --------------- (UNLESS YOU KNOW WHAT YOU'RE DOING) --------------- %
    % ------------------------------------------------------------------- %
    
    im = int16( imread(imagepath) );
    im = flipdim(im,1);
    imy = size(im,1); imx = size(im,2);
    
    
    curve_color = int16( curve_color );
    curve_color_tol = int16( curve_color_tol );
    
    curve_color = repmat( permute( curve_color, [1 3 2] ), imy, imx );
    curve_color_tol = repmat( permute( curve_color_tol, [1 3 2] ), imy, imx );
    
    
    is_within_tol = all( abs( im - curve_color ) <= curve_color_tol, 3 );
    indices_within_tol = repmat((1:imy)',1,imx).*double(is_within_tol);
    
    avg_indices = sum(indices_within_tol)./sum(is_within_tol);
    % figure; plot(avg_indices);
    
    
    x = xmin + (xmax-xmin)/(imx-1) * (0:imx-1);
    y = ymin + (ymax-ymin)/(imy-1) * avg_indices;
    
    figure;
    plot(x,y);
    title(imagepath); xlabel(xunit); ylabel(yunit);
    
    
    fileID = fopen(filepath, 'a');
    nbytes = fprintf(fileID, '%f\t%f\r\n', cat(1,x,y));
    fclose(fileID);
    
    disp(['Bytes written to "', filepath, '": ', num2str(nbytes)]);



