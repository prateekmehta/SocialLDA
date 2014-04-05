__author__ = 'prateek'
infile=open('obama-url-summary.txt', 'r')
lines=infile.readlines()
infile.close()
outtext = ['%d %s' % (i, line) for i, line in enumerate(lines)]
outfile = open("obama-url-summary-enumerate.txt","w")
outfile.writelines(str("".join(outtext)))
outfile.close()
