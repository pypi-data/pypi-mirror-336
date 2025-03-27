# from dataclasses import fields


# def dataprops(cls):
#     """A decorator to make dataclasses fields acting as properties
#     getter and setter methods names must initate with `get_` and `set_`"""
#     ignored_fields = getattr(cls, "__dataprops_ignore__", [])

#     for field in fields(cls):
#         if field.name not in ignored_fields:
#             setattr(
#                 cls,
#                 field.name,
#                 property(
#                     getattr(cls, f"get_{field.name}"), getattr(cls, f"set_{field.name}")
#                 ),
#             )
#     return cls
