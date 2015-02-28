empty = "empty"


class Entry:

    def __init__(self,
                 creation_timestamp=None,
                 update_timestamp=None,
                 tags=None,
                 value=None):
        self.creation_timestamp = creation_timestamp
        self.update_timestamp = update_timestamp
        if tags is None:
            self.tags = []
        else:
            self.tags = tags
        self.value = value

    def merge_with(self, other):
        merge_into(self.tags, other.tags)
        self.update_timestamp = other.update_timestamp

    @staticmethod
    def from_string(s, all_tags):
        entry = Entry()
        words = s.split(' ', 3)
        creation_timestamp = float(words[0])
        update_timestamp = float(words[1])
        if words[2] != empty:
            tags = deserialize_tags(words[2], all_tags)
        else:
            tags = []
        value = words[3]
        return Entry(creation_timestamp, update_timestamp, tags, value)

    def to_string(self, all_tags):
        tags_s = None
        if self.tags == []:
            tags_s = empty
        else:
            tags_s = serialize_tags(self.tags, all_tags)
        return "{0} {1} {2} {3}".format(self.creation_timestamp,
                                        self.update_timestamp,
                                        tags_s,
                                        self.value)


class Journal:

    def __init__(self, tags=None, entries=None):
        if tags is None:
            self.tags = []
        else:
            self.tags = tags
        if entries is None:
            self.entries = []
        else:
            self.entries = entries

    def merge_tags(self, tags):
        merge_into(self.tags, tags)

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_entry(self, entry):
        self.entries.append(entry)


    def add_or_merge_entry(self, entry):
        self.merge_tags(entry.tags)
        match = filter(lambda e: e.value == entry.value, self.entries)
        if match:
            match[0].merge_with(entry)
        else:
            self.add_entry(entry)


    def to_file(self, file_name):
        file = open(file_name, 'w')
        file.write(' '.join(self.tags))
        file.write('\n')
        for entry in self.entries:
            file.write(entry.to_string(self.tags))
            file.write('\n')
        file.close()


    def get_entries(self, tag_filter, sort):
        filtered_entries = filter(tag_filter, self.entries)
        return sorted(filtered_entries, key=sort, reverse=True)
        
    @staticmethod
    def from_file(file_name):
        journal = Journal()
        file = open(file_name, 'r')
        line = file.readline().rstrip()
        if line != '':
            journal.tags = line.split(' ')
        line = file.readline().rstrip()
        while line != '':
            entry = Entry.from_string(line, journal.tags)
            journal.add_entry(entry)
            line = file.readline().rstrip()
        file.close()
        return journal

def filter_tags_inclusive(tags1, tags2):
    if not tags1:
        return True
    for tag in tags1:
        if tag in tags2:
            return True
    return False


def serialize_tags(tags, all_tags):
    return ','.join(map(lambda tag: str(all_tags.index(tag)), tags))


def deserialize_tags(s, all_tags):
    return map(lambda v: all_tags[v], map(int, s.split(',')))


def merge_into(lst1, lst2):
    for v in lst2:
        if v not in lst1:
            lst1.append(v)
