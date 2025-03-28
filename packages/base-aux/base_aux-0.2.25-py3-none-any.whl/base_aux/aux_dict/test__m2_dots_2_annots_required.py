from base_aux.aux_callable.m2_lambda import *
from base_aux.aux_dict.m3_dict_attr1_simple import *


# =====================================================================================================================
dict_example = {
    "lowercase": "lowercase",
    # "nested": {"n1":1},
}


class Victim(DictAttrAnnotRequired):
    lowercase: str


# =====================================================================================================================
def test__obj():
    # victim = DictAttrAnnotRequired()
    # assert victim == {}
    #
    # victim = DictAttrAnnotRequired(hello=1)
    # assert victim == {"hello": 1}

    try:
        victim = Victim()
    except:
        assert True
    else:
        assert False


def test__dict_only():
    assert LambdaTrySuccess(DictAttrAnnotRequired) == True
    assert LambdaTrySuccess(DictAttrAnnotRequired)

    assert LambdaTryFail(DictAttrAnnotRequired) != True
    assert not LambdaTryFail(DictAttrAnnotRequired)

    assert LambdaTrySuccess(DictAttrAnnotRequired, **dict_example)
    assert LambdaTrySuccess(DictAttrAnnotRequired, lowercase="lowercase")
    assert LambdaTrySuccess(DictAttrAnnotRequired, LOWERCASE="lowercase")


def test__with_annots():
    assert LambdaTryFail(Victim)
    assert not LambdaTrySuccess(Victim)

    victim = Victim(lowercase="lowercase")
    assert victim["lowercase"] == "lowercase"

    assert LambdaTrySuccess(Victim, **dict_example)
    assert LambdaTrySuccess(Victim, lowercase="lowercase")
    assert LambdaTrySuccess(Victim, LOWERCASE="lowercase")

    assert LambdaTryFail(Victim, hello="lowercase")

    victim = Victim(lowercase="lowercase")
    assert victim == {"lowercase": "lowercase"}
    assert victim[1] == None
    assert victim.lowercase == "lowercase"


# =====================================================================================================================
