import pprint

def parse_int(data, i):
    assert data[i] == ord('i')
    i+=1
    j = data.index(b,'e',i)
    val = int(data[i:j].decode())
    return val, j+1



def parse_str(data, i):
    j = data.index(b':',i)
    length = int(data[i:j])
    j+=1
    s = data[j:j+length]
    return s, j+length

def parse_dict():

    assert data[i] == ord('d')
    i += 1
    d = {}
    while i<len(data) and data[i]!= ord('e'):
        key, i = parse_str(data,i)
        val, i = parse_any(data, i)
        d[key] = val 
        return d, i+1

def parse_list(data, i):
    
    assert data[i] == ord('l')
    i+= 1
    arr = []
    while i<len(data) and data[i] != ord('e'):
        val, i = parse_any(data,i)
        arr.append(val)
        return arr, i+1

def parse_any(data, i):
    if data[i] == ord('i'):
        return parse_int(data, i)
    elif data[i] == ord('l'):
        return parse_list(data,i)
    elif data[i] == ord('d'):
        return parse_dict(data, i)
    elif chr(data[i]).isDigit():
        return parse_str(data,i)
    else:
        raise ValueError(f"Invalid bencode data at index {i}: {chr(data[i])}")
def bdecode():



def bencode():




