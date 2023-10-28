import os

if __name__ == "__main__":
    path = input("Enter file path: ")
    files = os.listdir(path)
    new_folder = path + "/txts"
    if(not os.path.exists(new_folder)):
        os.mkdir(new_folder)
    for file in files:
        if file.endswith("txt"):
            os.replace(f"{path}/{file}",f"{path}/txts/{file}")
    # print(files)
    new_file = os.listdir(path+"/txts")