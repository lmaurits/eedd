import hashlib
import os
import tempfile

def main():

    # Write some random data to the chip, read it back, compare md5s
    print "Generating some random data..."
    noisefile = tempfile.NamedTemporaryFile(delete=False)
    os.system("dd if=/dev/urandom of=%s count=16" % noisefile.name)
    print "Writing random data to chip..."
    os.system("eedd --if %s --of /dev/ttyACM0" % noisefile.name)
    outputfile = tempfile.NamedTemporaryFile(delete=False)
    print "Reading data from chip..."
    os.system("eedd --if /dev/ttyACM0 --of %s" % outputfile.name)
    print "Comparing files...",
    noise = open(noisefile.name,"rb").read()
    noise_chksum = hashlib.md5(noise).hexdigest()
    chipoutput = open(outputfile.name,"rb").read()
    output_chksum = hashlib.md5(chipoutput).hexdigest()
    passed_randtest = noise_chksum == output_chksum
    if passed_randtest:
        print "files match!"
    else:
        print "files DO NOT match!"

    # Issue erase command, read chip contents, check it is empty
    print "Erasing chip..."
    os.system("eedd --erase /dev/ttyACM0")
    print "Reading data from chip..."
    emptyfile = tempfile.NamedTemporaryFile(delete=False)
    os.system("eedd --if /dev/ttyACM0 --of %s" % emptyfile.name)
    print "Checking chip is empty...",
    chipoutput = open(emptyfile.name,"rb").read()
    output_chksum = hashlib.md5(chipoutput).hexdigest()
    passed_erasetest = output_chksum == "84d04c9d6cc8ef35bf825d51a5277699"
    if passed_erasetest:
        print "chip is empty!"
    else:
        print "chip is NOT empty!"

    # Summarise
    if passed_randtest and passed_erasetest:
        print "All tests passed, firmware is good. :D"
        print "Deleting temporary files..."
        for file_ in (noisefile, outputfile, emptyfile):
            os.unlink(file_.name)
    elif passed_erasetest:
        print "Erasure test passed, but random write/read failed! :("
        print "Random data is in %s" % noisefile.name
        print "Read chip contents is in %s" % outputfile.name
        os.unlink(emptyfile.name)
    elif passed_randtest:
        print "Random write/read test passed, but failed to erase chip! :("
        print "Non-empty chip contents is in %s" % emptyfile.name
        for file_ in (noisefile, outputfile):
            os.unlink(file_.name)
    else:
        print "Nothing worked! D:"
        print "Random data is in %s" % noisefile.name
        print "Non-matching chip contents is in %s" % outputfile.name
        print "Non-empty chip contents is in %s" % emptyfile.name

if __name__ == "__main__":
    main()
