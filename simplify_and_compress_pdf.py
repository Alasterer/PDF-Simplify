# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import re
import subprocess
import sys
import easygui
from pathlib import Path


def translate_string_from_de_to_en(orig_string):
    '''
    Parameters
    ----------
    orig_string : TYPE
        String that needs some characters changed so that it is usable in the english language and has no chance of corrupting file names

    Returns
    -------
    TYPE
        String with some characters changed:
            * 'ä' --> 'ae'
            * 'ü' --> 'ue'
            * 'ö' --> 'oe'
            * 'ß' --> 'ss'
    '''
    special_char_map = {ord('ä'):'ae', ord('ü'):'ue', ord('ö'):'oe', ord('ß'):'ss'}
    return orig_string.translate(special_char_map)


def main():
    # Select all files (not used)
    # files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    # Select files with EasyGui window:
    files = easygui.fileopenbox("Select files to simplify", "PDF simplify", filetypes= "*.pdf", multiple=True)
    
    # Select image resolution with EasyGui input window:
    dpi = easygui.enterbox("Enter desired DPI resolution of pdf-internal images.\n\n250 DPI is the normal resolution for good compression and still good readability.", "PDF simplify - DPI input", "250")
    print('---')
    
    for f in files:
        # 1. Get file name and extension
        print('Processing: ', f)
        filename, file_extension = os.path.splitext(f)
        filename = translate_string_from_de_to_en(filename.replace(' ','_'))
        #print('filename: ', filename)
        #print('file_extension: ', file_extension)
        
        # 2. Test if output file already exists
        ps_filename = filename + '.ps'
        output_filename = filename + '_simpl' + file_extension
        process_flag = True
        if Path(output_filename).is_file():
            process_flag = easygui.ynbox('Output file\n{}\nis already present.\n\nShall I continue and overwrite file?'.format(output_filename), 'PDF simplify - File already present', ('Yes', 'No'))
        
        # 3. If file can be overwritten procede
        if process_flag == True:
            # 3.1. If file is a .pdf file procede
            if file_extension == '.pdf':
                # 3.1.1. Convert .pdf file to .ps
                command_output = subprocess.run(["pdftops", f, ps_filename], capture_output = True).stdout.decode()
                # pdftops input.pdf output_pdftops.ps
                #print(command_output)
                
                # 3.1.2. Convert .ps file back to .pdf
                gs = 'gswin32c' if (sys.platform == 'win32') else 'gs'
                command_output = subprocess.run([gs, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dDownsampleColorImages=true', '-dColorImageResolution='+dpi, '-dNOPAUSE', '-dBATCH', '-sOutputFile=' + output_filename, ps_filename], capture_output = True).stdout.decode()
                # gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dDownsampleColorImages=true -dColorImageResolution=250 -dNOPAUSE -dBATCH -sOutputFile=output_250dpi.pdf output_pdftops.ps
                #print(command_output)
                
                # 3.1.3. Check if file was created correctly by looking if it is present
                if Path(output_filename).is_file():
                    # 3.1.3.1. New file exists to we can remove no longer needed .ps file
                    os.remove(ps_filename)
                    print('Created:    ', output_filename)
                    print('---')
                else:
                    print('Simplified PDF could not be created!')
            else:
                print('WARNING:     This is not a .pdf file and cannot be simplified!\n---')
        else:
            print('NOTE:        File was not processed since alreasy present and overwrite was declined by user.\n---')
            process_flag = True
        
if __name__ == '__main__':
    main()