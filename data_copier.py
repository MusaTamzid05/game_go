import os
import shutil


def copy_helper(src, dst, name):
    src_path = os.path.join(src, name)
    dst_path = os.path.join(dst, name)

    shutil.copyfile(src_path, dst_path)

def main():
    src = "/home/musa/python_pro/rl_pro/game_go/data_processed"
    count = 100
    dst = f"data_processed_{count}"

    if os.path.isdir(dst) == False:
        os.mkdir(dst)

    src_files = os.listdir(src)
    src_files = sorted([src_file for src_file in src_files if "features" in src_file])
    src_files = src_files[:count]


    for index, src_file in enumerate(src_files):
        feature_file = src_file
        label_file = feature_file.replace("features", "labels")

        copy_helper(src = src, dst = dst, name = feature_file)
        copy_helper(src = src, dst = dst, name = label_file)

        print(f"{index} / {len(src_files)}")







if __name__ == "__main__":
    main()



