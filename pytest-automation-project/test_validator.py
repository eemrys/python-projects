import pytest
from random import randint
from random import choices
from ipaddress import IPv6Address
def randomizeIPv4(complete):
    ipv4 = ""
    for i in range(3):
        ipv4 += str(randint(0,255)) + '.'
    if (complete):
        ipv4 += str(randint(0,255))
    return ipv4

def getHex():
    return ''.join(choices('1234567890abcdef', k = randint(1,4)))

def randomizeIPv6(complete):
    ipv6 = ""
    for i in range(7):
        ipv6 += getHex() + ':'            
    if (complete):
        ipv6 += getHex()
    return ipv6

def randomizeIPv6_short():
    n = randint(0,6)
    ipv6 = ""
    for i in range(6):
        if i == n:
            ipv6 += '::'
        else:
            ipv6 += getHex() + ':'   
        if n == 6 :
            ipv6 += ':'
        else:
            ipv6 += getHex()
    return ipv6

@pytest.fixture
def validator():
    from ip_validator import Validate
    validator = Validate()
    return validator

@pytest.mark.parametrize("test_input,expected", [
        
    (randomizeIPv4(False)+"255", "Valid IPv4"),
    (randomizeIPv4(False)+"254", "Valid IPv4"),
    (randomizeIPv4(False)+"256", "Wrong IPv4"),
    (randomizeIPv4(False)+"0", "Valid IPv4"),     
    (randomizeIPv4(False)+"1", "Valid IPv4"),
    (randomizeIPv4(False)+"-1", "Wrong IPv4"),
    (randomizeIPv4(False)+"001", "Valid IPv4"),
    (randomizeIPv4(False)+"000", "Valid IPv4"),
    
    (randomizeIPv4(False), "Wrong IPv4"),
    (randomizeIPv4(True)+"Z", "Wrong IPv4"),    
    (randomizeIPv4(True)+"a", "Wrong IPv4"),    
    (randomizeIPv4(True)+"/", "Wrong IPv4"),
    (randomizeIPv4(True)+"?", "Wrong IPv4"),
    (randomizeIPv4(True)+"`", "Wrong IPv4"), 
    (randomizeIPv4(True)+"]", "Wrong IPv4"),
    (randomizeIPv4(True)+"~", "Wrong IPv4"),
    (randomizeIPv4(True)+"}", "Wrong IPv4"),
    (randomizeIPv4(True)+"!", "Wrong IPv4"),
    (randomizeIPv4(True)+",", "Wrong IPv4"),
        
    (randomizeIPv6(False)+"0000", "Valid IPv6"),
    (randomizeIPv6(False)+"1111", "Valid IPv6"),
    (randomizeIPv6(False)+"ffff", "Valid IPv6"), 
    (randomizeIPv6(False)+"FFFF", "Valid IPv6"),
    (randomizeIPv6(False)+"aaaa", "Valid IPv6"),
    (randomizeIPv6(False)+"AAAA", "Valid IPv6"),
    (randomizeIPv6(False)+"9999", "Valid IPv6"),
    (randomizeIPv6(False)+"gggg", "Wrong IPv6"),
    (randomizeIPv6(False)+"GGGG", "Wrong IPv6"),
    (randomizeIPv6(False)+"-0000", "Wrong IPv6"),
    (randomizeIPv6(False)+"-0", "Wrong IPv6"),
    (randomizeIPv6(False)+"0", "Valid IPv6"),
    (randomizeIPv6(False)+"000f", "Valid IPv6"),
    (randomizeIPv6(False)+"0001", "Valid IPv6"),
    (randomizeIPv6(False)+"-f", "Wrong IPv6"),
    (randomizeIPv6(False)+"12340", "Wrong IPv6"),
    (randomizeIPv6(False)+"1234a", "Wrong IPv6"),

    (randomizeIPv6_short(), "Valid IPv6"),
    (randomizeIPv6_short(), "Valid IPv6"),
    (randomizeIPv6_short(), "Valid IPv6"),
    (randomizeIPv6_short(), "Valid IPv6"),
    (randomizeIPv6_short(), "Valid IPv6"),
    (randomizeIPv6_short(), "Valid IPv6"),
    
    (getHex()+"::", "Valid IPv6"),
    ("::"+getHex(), "Valid IPv6"), 
    ("::"+getHex()+"::", "Wrong IPv6"), 
    (":"+getHex()+":", "Wrong IPv6"),
    ("::"+getHex()+":", "Wrong IPv6"),
    (":"+getHex()+"::", "Wrong IPv6"),
    (":"+getHex(), "Wrong IPv6"), 
    (getHex()+":", "Wrong IPv6"),
    ("::", "Valid IPv6"),
    ("::"+getHex(), "Valid IPv6"),
    (getHex()+"::"+getHex(), "Valid IPv6"),       
    
    (randomizeIPv6(True)+"/", "Wrong IPv6"),
    (randomizeIPv6(True)+"?", "Wrong IPv6"),
    (randomizeIPv6(True)+"`", "Wrong IPv6"),
    (randomizeIPv6(True)+"]", "Wrong IPv6"), 
    (randomizeIPv6(True)+"~", "Wrong IPv6"), 
    (randomizeIPv6(True)+"}", "Wrong IPv6"),
    (randomizeIPv6(True)+"!", "Wrong IPv6"),
    (randomizeIPv6(True)+",", "Wrong IPv6"),
    (randomizeIPv6(False), "Wrong IPv6"),
        
    (randomizeIPv4(True)+".3", "Wrong"),
    (randomizeIPv4(True)+".", "Wrong"),
    (randomizeIPv6(True)+":3", "Wrong"),
    (randomizeIPv6(True)+":", "Wrong"),
    (randomizeIPv6(False)+":4", "Wrong"),
    (":", "Wrong"),
    ("", "Wrong"),
    (" ", "Wrong"),
    ("hello", "Wrong"),
    ("кириллица", "Wrong")
])

def test_validator(validator, test_input, expected):
    assert validator.validateIPAddress([test_input])[0][1] == expected

@pytest.mark.parametrize("invalid_input", [
        1234,
        55.50,
        6+4j,
        [1,2,3,4],
        (1,2,3,4),
        {1:"one", 2:"two", 3:"three"}
])

def test_error(validator, invalid_input):
    with pytest.raises(Exception):
        validator.validateIPAddress([invalid_input])