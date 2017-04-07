
##############################################################
###        THIS IS THE SOURCE CODE FOR THE SCRIPT.         ###
### PLEASE SEE DOCUMENTATION FOR DESCRIPTION OF VARIABLES. ###
##############################################################

############################################
### DO NOT MODIFY ANYTHING IN THIS FILE! ###
### (UNLESS YOU KNOW WHAT YOU'RE DOING!) ###
############################################


from PIL import Image
pillow_site = r'http://pillow.readthedocs.org/en/3.0.x/index.html'
pillow_site_last_accessed = r'December 2015'
import time


def Plot_Image_Data_Extraction( image_path,
                                plot_range,
                                curve_color,
                                curve_color_tol,
                                unit_data_file_name,
                                pixel_data_file_name ):
    
    t0 = time.time()
    
##    im = Image.open(image_path)
    # Create the PIL image from the file.
    try:
        im = Image.open(image_path)
    except Exception as ex:
        print(' *** Error *** ')
        print('Image file was not found or could not be opened.')
        print('Here is the full error info:')
        print(ex)
        print('Make sure that the file is at the path specified,')
        print('    and that it ends with an appropriate image extension.')
        print('See "{}" for more info.'.format(pillow_site))
        print('(Site last accessed: {}.)'.format(pillow_site_last_accessed))
        input('Press Enter to exit: ')
        print('Exiting...')
        return -1
    else:
        print('Image loaded: "{}".'.format(image_path))
        


    # Convert to RGB if the image is not RGB or RGBA.
    # This script relies on the RGB data of the image.
    # (Note: it is okay if the image is RGBA, since we just
    #   ignore anything after the first three inputs.)
    if im.mode not in ('RGB', 'RGBA'):
        print('Image is {}.'.format(im.mode))
        try:
            im = im.convert('RGB')
        except:
            print(' *** Error *** ')
            print('Image could not be converted to RGB.')
            print('Processing may not be correct or script may fail.')
            inpt = input('Continue? (Y/N): ')
            if inpt.upper().startswith('N'):
                print('Exiting...')
                return -2
        else:
            print('Image successfully converted to RGB.')

    
    t00 = time.time()
        
    def is_curve_color(color):
        return not any( abs( color[n] - curve_color[n] ) > curve_color_tol[n]
                        for n in range(len(curve_color_tol)) )
    
    # Rotate so that x-values now run along the height, and y-values along the width.
    # Also puts the image origin at the plot origin.
    im = im.transpose(Image.ROTATE_270)
    im_data_flat = list(im.getdata())
    im_data = ( iter(im_data_flat[k: k+im.width])
                for k in range(0, len(im_data_flat), im.width) )
    t01 = time.time()

    def index_avg(iterable, condition=None):
        index_sum = 0
        count = 1
        for count,(i,val) in enumerate(filter(condition, enumerate(iterable)), 1):
            index_sum += i
        return index_sum/count
    
    x_curve_pix = []
    y_curve_pix = []
    for x,y_row in enumerate(im_data):
        y_vals_avg = index_avg(y_row, lambda z:is_curve_color(z[1]))
        if y_vals_avg:
            x_curve_pix.append(x)
            y_curve_pix.append(y_vals_avg)



    
##    # ~2800
##    im_data_flat = im.getdata()
##    im_data = zip(*[iter(im_data_flat)] * im.width)
##    x_curve_pix = []
##    y_curve_pix = []
##    for x,y_row in enumerate(im_data):
##        y_vals = [ y for y,pix in enumerate(y_row) if is_curve_color(pix) ]
##        if len(y_vals) > 0:
##            x_curve_pix.append(x)
##            y_curve_pix.append( sum(y_vals)/len(y_vals) )


##    # ~2800:
##    im_data_flat = list(im.getdata())
##    im_data = ( im_data_flat[k: k+im.width] for k in range(0, len(im_data_flat), im.width) )
##    x_curve_pix = []
##    y_curve_pix = []
##    for x,y_row in enumerate(im_data):
##        y_vals = [ y for y,pix in enumerate(y_row) if is_curve_color(pix) ]
##        if len(y_vals) > 0:
##            x_curve_pix.append(x)
##            y_curve_pix.append( sum(y_vals)/len(y_vals) )


##    # ~2800
##    im_data_flat = list(im.getdata())
##    def chunks(iterable, size):
##        for k in range(0, len(iterable), size):
##            yield iterable[k:k+size]
##    im_data = chunks(im_data_flat, im.width)
##    x_curve_pix = []
##    y_curve_pix = []
##    for x,y_row in enumerate(im_data):
##        y_vals = [ y for y,pix in enumerate(y_row) if is_curve_color(pix) ]
##        if len(y_vals) > 0:
##            x_curve_pix.append(x)
##            y_curve_pix.append( sum(y_vals)/len(y_vals) )


##    # ~3600:
##    im_data = im.getdata()
##    x_curve_pix = []
##    y_curve_pix = []
##    for x in range(im.height):
##        y_vals = [ y for y in range(im.width) if is_curve_color(im_data[im.width*x + y]) ]
##        if len(y_vals) > 0:
##            x_curve_pix.append(x)
##            y_curve_pix.append( sum(y_vals)/len(y_vals) )
    
    
    t02 = time.time()
    
    
    x_curve_unit = tuple( plot_range[0][0] + 
                          x_pix * (plot_range[0][1] - plot_range[0][0])/(im.height - 1)
                          for x_pix in x_curve_pix )
    
    y_curve_unit = tuple( plot_range[1][0] + 
                          y_pix * (plot_range[1][1] - plot_range[1][0])/(im.width - 1)
                          for y_pix in y_curve_pix )
    
    t03 = time.time()
    
    
    
    curve_pix = zip(x_curve_pix, y_curve_pix)
    curve_unit = zip(x_curve_unit, y_curve_unit)
    
    pix_chars = unit_chars = 0
    with open(pixel_data_file_name,'a') as pix_file:
        with open(unit_data_file_name,'a') as unit_file:
            for pix,unit in zip( curve_pix, curve_unit ):
                pix_chars += pix_file.write('{}\t{}\n'.format(*pix))
                unit_chars += unit_file.write('{}\t{}\n'.format(*unit))
    
    t04 = time.time()
    
    t1 = time.time()
    
    print()
    print(' ***** Timing sections: ***** ')
    print('Obtaining picture: {} ms'.format(1000*(t00-t0)))
    print('Pre-prcoessing picture and loading data : {} ms'.format(1000*(t01-t00)))
    print('Analyzing data: {} ms'.format(1000*(t02-t01)))
    print('Analyzing data: {} ms/pixel'.format(1000*(t02-t01)/(im.width*im.height)))
    print('Transforming to plot units: {} ms'.format(1000*(t03-t02)))
    print('Writing data to files: {} ms'.format(1000*(t04-t03)))
    print()

    print('Script ran in: {} ms'.format(1000.0*(t1-t0)))
    
    print()
    print('Characters written to "{}": {}'.format(pixel_data_file_name, pix_chars))
    print('Characters written to "{}": {}'.format(unit_data_file_name, unit_chars))
    print()
    
    print('Everything finished sucecssfully!')
    input('Press Enter to exit: ')
    print('Bye! Have a beautiful time!')

    return 1



if __name__ == '__main__':
    print('Running from self...')
    print()
    p0 = r'Hologram_Transmission_Spectrum_large_crop.png'
    p1 = ((340, 840), (0, 100))
    p2 = (0, 0, 128)
    p3 = (8, 8, 8)
    p4 = r'xy_unit_data.txt'
    p5 = r'xy_pix_data.txt'
    result = Plot_Image_Data_Extraction( p0, p1, p2, p3, p4, p5 )
    print()
    print('(Finished with return value: {})'.format(result))




# We need some extra packages to plot in Python.
# So this is omitted for now...
####import matplotlib
####import matplotlib.pyplot as plt
####plt.figure(1)
####plt.plot(x_curve_pix, y_curve_pix_s)
####plt.figure(2)
####plt.plot(x_curve_unit_val, y_curve_unit_val)
####plt.show()


# Copy/paste the following code into MATLAB to plot the data:
##xydata = importdata('C:\<Plot_Image_Data_Extraction_path>\xy_unit_data.txt','\t');
##x = xydata(:,1);
##y = xydata(:,2);
##figure(1);
##plot(x,y,'.-');







