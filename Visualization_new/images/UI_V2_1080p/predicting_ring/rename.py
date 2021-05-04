import glob,os

files = []

for file in glob.glob("*.png"):
    files.append(file)

for i in range(len(files)):
    rename_name = "pred_ring_"+str(i) + ".png"
    os.rename(files[i],rename_name)