import os, re, argparse

def make_regex_from_hex_sign(hex_sign):
    regex_hex_sign = re.compile(hex_sign.decode('hex'))
    return regex_hex_sign

def xm_read(regex_hex_sign, xm_size):
    f = open(infile, 'rb')
    allbytes = f.read()
    xm_data = 0
    for xm_sign in regex_hex_sign.finditer(allbytes):
        if xm_data != 0:
            break # break to stop searching after first match
        offset = xm_sign.start()
        f.seek(offset)
        xm_data = f.read(xm_size)
        print "\nXM data offset: " + hex(offset)
	f.close()
    return xm_data

def xm_write(xm_data):
    f = open(os.path.splitext(infile)[0] + ".xm", 'wb')
    f.write(xm_data)
    f.close()


xm_signature = "457874656E646564204D6F64756C65"

# arg parser
parser = argparse.ArgumentParser(description="----- XM module extractor by podstanar -----")

# arguments
parser.add_argument('-b', '--byte_mode', default=False, action='store_true', help="Specify XM size in bytes instead of KB")
parser.add_argument('input_file', type=str, help="File from which XM module should be extracted")

args = parser.parse_args()

infile = args.input_file

if args.byte_mode == True:
    xm_size = raw_input("\nXM size(in Bytes): ")
else:
    xm_size = raw_input("\nXM size(in KB): ")

try:
    xm_size = int(xm_size, 0)
except:
    print "\nNot a valid size!"
else:
    if args.byte_mode == False:
        xm_size *= 1024 # mul by 1024 to get size in KB
    xm_data = xm_read(make_regex_from_hex_sign(xm_signature), xm_size)
    if xm_data != 0:
    	xm_write(xm_data)
    	print "XM successfully extracted to " + os.path.splitext(infile)[0] + ".xm"
    else:
    	print "\nNo XM module found."
