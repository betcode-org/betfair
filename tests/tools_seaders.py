import datetime

from betfairlightweight.resources.baseresource import BaseResource

template_needle = '''
class {classname}(BaseResource):
    class Meta(BaseResource.Meta):
'''
template_replacewith = '''
class {classname}(BaseResource):
    """
{docstrings}
    """
{defines}

    class Meta(BaseResource.Meta):
'''
done = set()


def get_type_name(classobj):
    vtype = type(classobj)
    if isinstance(classobj, datetime.date):
        return 'datetime.{}'.format(vtype.__name__)
    return vtype.__name__


def docstring_class(classtype, classobj):
    if (classtype in done) or isinstance(classobj, dict):
        return
    done.add(classtype)

    items = []
    meta = classtype.Meta
    okeys = meta.attributes.values() + \
        [v.Meta.identifier for k, v in meta.sub_resources.items()
         if k not in meta.attributes.keys()]

    for k in okeys:
        v = getattr(classobj, k)
        if (v is None) and (k == 'error_code'):
            v = 'error_code'

        if (v is None) or (isinstance(v, list) and (0 == len(v))):
            raise Exception('Docstring creation error for {}.{} == {}'
                            .format(classobj, k, v))

        if isinstance(v, list) and (0 < len(v)):
            sub0 = v[0]
            items.append((k, 'list[{}]'.format(get_type_name(sub0))))
            if isinstance(sub0, BaseResource):
                docstring_class(type(sub0), sub0)

        else:
            items.append((k, get_type_name(v)))
            if isinstance(v, BaseResource):
                docstring_class(type(v), v)

    items = sorted(items, key=lambda item: item[0])

    print('-' * 50)
    print('from')
    print('-' * 50)
    needle = template_needle.format(classname=classtype.__name__)
    print(needle)
    print('-' * 50)
    print('to')
    print('-' * 50)
    replacewith = template_replacewith.format(
        classname=classtype.__name__,
        docstrings='\n'.join((
            '    :type {}: {}'.format(k, vtype)
            for k, vtype in items
        )),
        defines='\n'.join((
            '    {} = None'.format(k)
            for k, _ in items
        ))
    )
    print(replacewith)
    print('-' * 50)

    filename = '../{}.py'.format(classtype.__module__.replace('.', '/'))
    with open(filename) as f:
        towrite = f.read().replace(needle, replacewith)
    with open(filename, 'w') as f:
        f.write(towrite)


def assert_isinstance(iobject, itype):
    assert isinstance(iobject, itype)
    docstring_class(itype, iobject)

#
