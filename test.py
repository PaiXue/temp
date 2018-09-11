import javalang
import json

# tokens = javalang.tokenizer.tokenize(
#     "public void copy(final POIFSFileSystem poiFs, final POIFSDocumentPath path, final String name, final PropertySet ps) throws WritingNotSupportedException, IOException {")
# tokens = javalang.tokenizer.tokenize(
#     "public void run() throws IOException ")
# tokenList = list(tokens)
# for i in range(0, len(tokenList)):
#     print(tokenList[i].value)

data = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': [5,1,2,3]},{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': [5,1,2,3]},]

j = json.dumps(data)
print(j)
