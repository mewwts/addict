class Dict(dict):
	"""
	Dict is a subclass of dict, which allows you to get AND SET(!!)
	items in the dict using the attribute syntax!

	When you previously had to write:

	my_dict = {'a': {'b': {'c': [1, 2, 3]}}}

	you can now do the same simply by:

	my_Dict = Dict()
	my_Dict.a.b.c = [1, 2, 3]

	Or for instance, if you'd like to add some additional stuff,
	where you'd with the normal dict would write

	my_dict['a']['b']['d'] = [4, 5, 6],

	you may now do the AWESOME

	my_Dict.a.b.d = [4, 5, 6]

	instead. But hey, you can always use the same syntax as a regular dict,
	however, this will not raise TypeErrors or AtrributeErrors at any time
	while you try to get an item.

	"""
	def __init__(self, *args, **kwargs):
		super(Dict, self).__init__(*args, **kwargs)
		print args
		if (args and isinstance(args[0], dict)):
			for key, val in args[0].iteritems():
				self[key] = val
#		else:
#			self

	def __setattr__(self, name, value):
#		if isinstance(value, dict):
#			value = self.__class__(value)
		if isinstance(name, str):
			super(Dict, self).__setattr__(name, value)
		if name not in self:
			super(Dict, self).__setitem__(name, value)

	def __setitem__(self, name, value):
		super(Dict, self).__setitem__(name, value)
		self.__setattr__(name, value)

	def __getattr__(self, name):
		val = self.__class__()
		self.__setitem__(name, val)
		return super(Dict, self).__getattribute__(name)

	def __getitem__(self, name):
		if name in self:
			return super(Dict, self).__getitem__(name)
		else:
			val = self.__class__()
			self.__setitem__(name, val)
			#return self[name]
			return super(Dict, self).__getitem__(name)

