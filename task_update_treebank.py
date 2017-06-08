from os.path import dirname, join, basename
from os import listdir, remove
import pandas as pd
import io
import re


def transform_line(input_file, output_file):
    """ split lines and save file with unix line seperator
    
    :param input_file: 
    :param output_file: 
    :return: 
    """
    with open(input_file) as infile:
        with io.open(output_file, 'w', newline="\n", encoding="utf-8") as outfile:
            for line in infile:
                outfile.writelines(line.replace(".\tCH", ".\tCH\n").decode("utf-8"))


def check_missing_token(corpus):
    """ ensure all tokens is tagging

    :type corpus: DataFrame 
    """
    for i in range(corpus.shape[0] - 1):
        d = corpus.ix[i + 1, "start"] - corpus.ix[i, "end"]
        if d != 1 and d != 2:
            raise Exception("Error in Check Missing Token")
    print "Check missing token\t: Pass"


def make_treebank_file(brat_annotation_file, treebank_folder="."):
    df = pd.read_csv(brat_annotation_file, sep="\t", names=["id", "token", "word"])
    df["tag"] = df.apply(lambda row: row["token"].split(" ")[0], axis=1)
    df["start"] = df.apply(lambda row: int(row["token"].split(" ")[1]), axis=1)
    df["end"] = df.apply(lambda row: int(row["token"].split(" ")[2]), axis=1)
    df = df.sort_values("start").reset_index()
    check_missing_token(df)
    temp_file = "tmp"
    df.to_csv("tmp", sep="\t", header=False, index=False, encoding="utf-8", line_terminator="\n",
              columns=["word", "tag"])
    file_id = re.match("p_(.*).ann", basename(brat_annotation_file)).group(1)
    output_file = join(treebank_folder, "%s.conll" % file_id)
    transform_line(temp_file, output_file)
    remove(temp_file)
    print "Make treebank\t\t: Complete"


if __name__ == '__main__':
    brat_folder = join(dirname(__file__), "brat")
    treebank_folder = join(dirname(__file__), "treebank")
    files = listdir(brat_folder)
    files = [join(brat_folder, file) for file in files if file.startswith("p_") and file.endswith(".ann")]
    for file in files:
        make_treebank_file(file, treebank_folder)