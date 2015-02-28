# snotes

snotes, which stands for sticky notes is a terminal note taking application made in python

### Usage

The following command adds a note that is tagged with the corresponding tags:
Note that when the same note is added multiple time with different tags the actual tags are marged rather than replaced
snotes add -t tag1 tag2 ... tagn -n "This is my note"

The following commands gets all the notes filtered by the optional tags:
snotes get -t tag1 tag2 ... tagn

### Current limitations

This program is still in developpement, the following limitations exist in the current version:

 - It is not possible to remove notes
 - It is not possible to edit notes
 - Other missing features
