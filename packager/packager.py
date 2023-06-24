
import os


def package_the_texts(original_file, summary_file, packaged_file):
    with open(original_file, 'r', encoding='utf-8') as original, \
            open(summary_file, 'r', encoding='utf-8') as summary, \
            open(packaged_file, 'w', encoding='utf-8') as packaged:
        packaged.write(original.read())
        packaged.write('\n\n')

        packaged.write("Summary\n\n")  # Write "Summary" at the beginning
        packaged.write(summary.read())


# Define the paths and filenames
original_file = "output.txt"
summary_file = "summary.txt"
packaged_file = "package.txt"

# Call the function to package the texts
package_the_texts(original_file, summary_file, packaged_file)

# Delete all the files
files_to_delete = [original_file, summary_file, packaged_file]
for file in files_to_delete:
    if os.path.exists(file):
        os.remove(file)
