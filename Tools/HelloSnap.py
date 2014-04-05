import snap

G5 = snap.LoadEdgeList(snap.PNGraph, "Sample1000edge", 0, 1)

print "loaded!"

FOut = snap.TFOut("sample1000edge.graph")
G5.Save(FOut)
FOut.Flush()

print "saved!"

