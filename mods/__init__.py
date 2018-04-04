import scandir, sys, os
_mod_files = scandir.walk(os.path.dirname(os.path.realpath(__file__)))

_mod_names = []
for i in list(_mod_files)[0][2]:
	if i[-3:] == ".py" and i[0:1] != '_':
		_mod_names.append(i[:-3])
#mods = map(__import__, _mod_names)
mods = {k: __import__(k) for k in _mod_names}
#print 'mods:', mods
#__all__ = mods

