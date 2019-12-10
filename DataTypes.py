
class _DataTypeStruct(object):
    __slots__ = ('tql_type', 'is_vector')

    def __init__(self,tql_type,is_vector=False):
        self.tql_type = tql_type
        self.is_vector = is_vector

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not (hash(self) == hash(other))

    def __hash__(self):
        return hash((self.tql_type, self.is_vector))

    def __repr__(self):
        try:

            return "<TQL<<{}>>".format(self.tql_type.__name__)
        except AttributeError as er:
            print(er)


class DataType:
    BASE_ARRAY = _DataTypeStruct(tuple,True)
    BASE_FLOAT = _DataTypeStruct(float)
    BASE_STRING = _DataTypeStruct(str)
    BASE_UNDEFINED = None
    BASE_BOOLEAN = _DataTypeStruct(bool)
    BASE_NULL = _DataTypeStruct(type(None))

    @classmethod
    def from_rule_value(cls,rule_value):
        if isinstance(rule_value, str):
            return cls.BASE_STRING
        elif isinstance(rule_value, bool):
            return cls.BASE_BOOLEAN
        elif isinstance(rule_value,(tuple,list,dict)):
            return cls.BASE_ARRAY
        elif isinstance(rule_value, (int,float)):
            return cls.BASE_FLOAT
        elif rule_value is None:
            return cls.BASE_NULL
        else:
            dynamic_dtypes = cls.get_dynamic_pythn_dtypes()
            dynamic_tql_types = cls.get_dynamic_tql_datatypes()
            if rule_value in dynamic_dtypes:
                indx = dynamic_dtypes.index(rule_value)
                return dynamic_tql_types[indx]
            else:
                raise TypeError("Invalid type datatype {}".format(type(rule_value).__name__))

    @classmethod
    def register_new_tql_datatype(cls,native_dtype,new_type_name,is_vector_type=False):
        if new_type_name.startswith("DYNAMIC"):
            new_tql_datatype = _DataTypeStruct(native_dtype, is_vector_type)
            if new_tql_datatype not in cls.get_primitive_tql_datatypes() and new_tql_datatype not in cls.get_dynamic_tql_datatypes():
                setattr(cls, new_type_name, new_tql_datatype)
        else:
            raise TypeError("Expects new dtype startswith DYNAMIC_ keyword")

    @classmethod
    def get_primitive_tql_datatypes(cls):
        res = tuple(getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")
               and attr.startswith("BASE"))
        return res

    @classmethod
    def get_dynamic_tql_datatypes(cls):
        res = tuple(getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")
               and attr.startswith("DYNAMIC"))
        return res

    @classmethod
    def get_primitive_pythn_dtypes(cls):
        res = cls.get_primitive_tql_datatypes()
        return tuple(i.tql_type if i is not None else None for i in res)


    @classmethod
    def get_dynamic_pythn_dtypes(cls):
        res = cls.get_dynamic_tql_datatypes()
        return tuple(i.tql_type if i is not None else None for i in res)

    @classmethod
    def delete_tql_datatype(cls,attrib_name):
        delattr(cls, attrib_name)
