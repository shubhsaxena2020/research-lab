# Method

Our pipeline encodes each document into a dense vector and compares candidate passages
with a cosine similarity threshold that we tuned on the development split.

The threshold search used a small grid and is logged in the run folder.
