import constant
wfile = open(constant.mojo_info_dir+"score_"+constant.genres[5],"wb")
for i in range(0,5):
    hfile = open(constant.mojo_info_dir+"score_"+constant.genres[5]+str(i),"rb")
    content = hfile.read()
    wfile.write(content)
wfile.close()