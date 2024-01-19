import os
import shutil
import glob
import random

# specify source and destination directories
src_dir = 'D:/Rubix/models/sat/test/images'
dst_dir = 'D:/Rubix/models/dataset/test/images'

# create destination directory if it doesn't exist
os.makedirs(dst_dir, exist_ok=True)

# get a list of all "post" PNG files in source directory
test_files = glob.glob(os.path.join(src_dir, '*.png'))
test_files = list(filter(lambda x: 'post' in x, test_files))

# randomly select 1500 files
selected_files = random.sample(test_files, 500)

# move the selected files to the destination directory
for file_path in selected_files:
    # construct destination file path
    dst_file_path = os.path.join(dst_dir, os.path.basename(file_path))
    
    # move the file
    shutil.copy(file_path, dst_file_path)

print(f'Copied {len(selected_files)} files.')