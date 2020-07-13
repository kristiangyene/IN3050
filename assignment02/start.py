class RUList:

    def __init__(self):
        self._rulist = []
        self._MAX = 5

    
    def add(self, e):
        if e == "":
            return "error: empty string."
        if len(self._rulist) > self._MAX:
            return "error: reached max number of elements."
        if e in self._rulist:
            self._rulist.remove(e)
        self._rulist.insert(0, e)
    
    def get_list(self):
        return self._rulist
        
    def get(self, e):
        return self._rulist[e]




def test_insert_element():
    ru = RUList()
    ru.add("1st")
    ru.add("2nd")
    assert len(ru.get_list()) == 2

def test_empty_string():
    ru = RUList()
    assert ru.add("") == "error: empty string."

def test_index_lookup():
    ru = RUList()
    for e in range(0, 5):
        ru.add(e)
    assert ru.get(2) == 2

def test_duplicate():
    ru = RUList()
    for e in range(0, 5):
        ru.add(e)
    print(ru.get_list())
    ru.add(2)
    print(ru.get_list())
    assert ru.get(0) == 2
    assert ru.get(2) == 3

def test_max_elements():
    ru = RUList()
    for e in range(0, 6):
        ru.add(e)
    assert ru.add(6) == "error: reached max number of elements."

test_insert_element()
test_index_lookup()
test_empty_string()
test_duplicate()
test_max_elements()