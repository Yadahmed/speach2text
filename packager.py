# Takes two file name or paths. 
# Adds the contents of both files to a new file called package.txt
def package_the_texts(original, summary):
    with open("package.txt", "a") as packaged_file:
        packaged_file.truncate(0)

        original = open(original, "r")
        packaged_file.write("Original:\n")
        packaged_file.write(original.read())

        summary = open(summary, "r")
        packaged_file.write("Summary:\n")
        packaged_file.write(summary.read())

        return packaged_file

package_the_texts("a.txt", "summary.txt")
