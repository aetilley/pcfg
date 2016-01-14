from revscoring.datasources import revision
from revscoring.datasources import diff
from revscoring.extractors import APIExtractor
import mwapi


#File to dump data
DUMP_TARGET_NAME = "dump.txt"
dump_target = open(DUMP_TARGET_NAME, 'w')


#Select rev_ids to examine.
IDS_FILE_NAME = "data.tsv"
ids_file = open(IDS_FILE_NAME)
MAX_REVISIONS = 10
rev_ids = []
count = 0
for line in ids_file:
    if count < MAX_REVISIONS:
        rev_ids.append(int(line.strip().split("\t")[0]))
        count += 1
    else:
        break

"""
Feature to examine.  Let FEATURE be one of
diff.added_tokens
diff.removed_tokens
diff.added_segments
diff.removed_segments
revision.content
revision.content_tokens
"""
FEATURE = diff.added_segments


#Extract data from selected revisions and write to selected file
extr = APIExtractor(mwapi.Session("https://en.wikipedia.org"))
for id in rev_ids:

    data = extr.extract(id, FEATURE)
    dump_target.write("\n\nBeginning %s of revision %d\n\n" % (FEATURE, id))
    if type(data) is str:
        dump_target.write(data)
    elif type(data) is list:
        dump_target.writelines(data)
    else:
        print("Unknown Type")
        exit()
    dump_target.write("\n\nEnd %s of revision %d" % (FEATURE, id))
