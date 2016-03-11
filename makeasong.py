#!/usr/bin/env python
import random
import sys
import getopt


def make_song_title(song_title):
    s = song_title.upper()
    for n in ["#", "$", ",", "*", "<", ">", "%"]:
        s = s.replace(n, " ")
    s = s.strip()
    return " ".join(s.split())


def main(argv):
    inputfile = ''
    outputfile = ''
    output_path = ''
    verse_count = 2
    chorus_count = 1
    verse_length = 5
    chorus_lenght = 5

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "verses=", "choruses=",
                                   "verse_lenght=", "chorus_lenght="])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == ("-h", "--help"):
            print 'test.py -i <inputfile> -o <outputfile> -vc <count of verses> -cc <count_of_coruses> -lv <lenght of a verse (rows)> -lc <lenght of a chorus (rows)>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            output_path = arg
        elif opt in ("-v", "--verses"):
            verse_count = int(arg)
        elif opt in ("-c", "--choruses"):
            chorus_count = int(arg)
        elif opt in ("-e", "--verse_lenght"):
            verse_length = int(arg)
        elif opt in ("-h", "--chorus_lenght"):
            chorus_lenght = int(arg)

    if not inputfile:
        raise ValueError("Usage: makeasong.py -i <inputfile> -o <outputfile>")
    print "starting"
    f = open(inputfile)
    # TODO: Don't read the file to memory if its too large
    entire_file = f.read()
    # split the whole file into a list
    file_in_a_list = entire_file.split("\n")
    num_lines = len(file_in_a_list)
    # create random list of numbers
    #random_nums = random.sample(xrange(num_lines), num_lines)
    # Now, create random lines for verses and choruses
    verses = []
    choruses = []

    for i in range(0, verse_count):
        verses.append(random.sample(xrange(num_lines), verse_length))
    for i in range(0, chorus_count):
        choruses.append(random.sample(xrange(num_lines), chorus_lenght))

    output = []
    song_title = ""
    previous_chorus = None
    # print out the result
    while True:
        verse = verses.pop() if verses else []
        chorus = choruses.pop() if choruses else []
        if verse:
            output.append("\n \n --- verse ---- \n \n")
        for vn in verse:
            output.append(file_in_a_list[vn] + "\n")

        output.append("\n \n --- chorus ---- \n \n")
        for cn in chorus:
            if not song_title:
                song_title = make_song_title(file_in_a_list[cn])
                output.insert(
                    0, "####################################################")
                output.insert(0, "\n%s\n" % song_title)
                output.insert(
                    0, "####################################################")
            output.append(file_in_a_list[cn] + "\n")
        if not chorus:
            for cn in previous_chorus:
                output.append(file_in_a_list[cn] + "\n")
        if chorus:
            previous_chorus = chorus
        if not verse and not chorus:
            break
    print
    print
    print
    print "".join(output)
    print
    print
    print
    if not outputfile:
        outputfile = "%s%s.txt" % ("%s/" % output_path if output_path else "", song_title.replace(" ", "_"))

    o = open(outputfile, "w")

    print 'Input file is "', inputfile
    print 'Output file is "', outputfile

    o.write("".join(output))

    o.close()
    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])

