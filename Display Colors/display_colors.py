import sublime
import sublime_plugin
import re

obj = ""
flag = False
line_total = 0
phantoms = []

class rgba(object):
	red = 0
	green = 0
	blue = 0
	alpha = 0

class ClearallCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print("clearall")
		global flag
		global phantoms
		flag = False
		#self.view.erase_phantoms("hex")
		#self.view.erase_phantoms("rgba")
		#self.view.erase_phantoms("@")
		phantoms.clear()
		line_total = self.view.rowcol(self.view.size())[0]+100
		for indx in range(line_total):
			self.view.erase_phantoms("hex"+str(indx))
			self.view.erase_phantoms("rgba"+str(indx))
			self.view.erase_phantoms("@"+str(indx))
		pass


class DisplaycolorsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#self.view.insert(edit, 0, "Hello, World!")
		#print( self.view.substr(sublime.Region(0, self.view.size())) )
		#print( self.view.find("#\w+", 0, sublime.IGNORECASE) )
		#print( self.view.find_all("#\w+", sublime.IGNORECASE) )
		#self.view.show(colors[0])

		global obj
		global flag
		global line_total

		obj = self
		flag = True

		#EventListener.inputview = self.view
		#EventListener.inputself = self
		#EventListener.output = self.view.window()

		self.start()

		pass

	def start(self):
		print("--------------")
		print("start...")
		#self.clear_all()

		self.clear_all()

		line_total = self.view.rowcol(self.view.size())[0]+1
		for indx in range(line_total):
			region = self.view.line(sublime.Region(self.view.text_point(indx, 0), self.view.text_point(indx, 0)))
			#linha = self.view.substr(region)
			self.reg_color(region, indx)

		#global phantoms
		#for phantom in phantoms:
			#p = self.view.query_phantom(phantom)
			#print(p)

		#doc = sublime.Region(0, self.view.size())
		#regions = self.view.lines(doc)
		pass

	def reg_find(self, region, indx, column):
		print("--------------")
		print("reg_find...")
		ret = sublime.Region(-1, -1)
		linha = self.view.substr(region)
		pos = linha.rfind("#", column-7, column)
		if pos < 0:
			pos = linha.rfind("rgba", max([0, column-22]), column)
		if pos < 0:
			pos = linha.rfind("@", column-7, column)

		reg_temp = sublime.Region(region.begin()+pos, region.end())
		linha_temp = self.view.substr(reg_temp)
		pos_end = re.search(";", linha_temp)
		if pos_end:
			reg_temp = sublime.Region(region.begin()+pos, region.begin()+pos+pos_end.start()+1)
			linha_temp = self.view.substr(reg_temp)

		print(linha_temp, reg_temp)

		if pos >= 0:
			regex = re.compile("#\w+", re.MULTILINE & re.IGNORECASE)
			regex_all = regex.findall(linha_temp)
			iterator = regex.finditer(linha_temp)
			for match in iterator:
				#print("iterator...", match.span()[0], match.span()[1])
				ret = sublime.Region(reg_temp.begin()+match.span()[0], reg_temp.begin()+match.span()[0]+match.span()[1])
				break

			regex = re.compile("rgba\s?\([^\)]+\)", re.MULTILINE & re.IGNORECASE)
			regex_all = regex.findall(linha_temp)
			iterator = regex.finditer(linha_temp)
			for match in iterator:
				#print("iterator...", match.span()[0], match.span()[1])
				ret = sublime.Region(reg_temp.begin()+match.span()[0], reg_temp.begin()+match.span()[0]+match.span()[1])
				break

			regex = re.compile("@\w+", re.MULTILINE & re.IGNORECASE)
			regex_all = regex.findall(linha_temp)
			iterator = regex.finditer(linha_temp)
			for match in iterator:
				#print("iterator...", match.span()[0], match.span()[1])
				ret = sublime.Region(reg_temp.begin()+match.span()[0], reg_temp.begin()+match.span()[0]+match.span()[1])
				break

		return ret
		pass

	def reg_del(self, region, indx, column):
		ret = sublime.Region(-1, -1)
		linha = self.view.substr(region)
		pos = linha.rfind("#", column-7, column)
		if pos < 0:
			pos = linha.rfind("rgba", max([0, column-22]), column)
		if pos < 0:
			pos = linha.rfind("@", column-7, column)

		if pos >= 0:
			ret = sublime.Region(region.begin()+pos, region.begin()+pos)

		#print(ret)
		return ret
		pass

	def reg_color(self, region, indx):
		print("--------------")
		print("reg_color...")

		linha = self.view.substr(region)
		print(linha)

		regex = re.compile("#\w+", re.MULTILINE & re.IGNORECASE)
		regex_all = regex.findall(linha)
		iterator = regex.finditer(linha)

		for match in iterator:
			color = match.group()
			c = sublime.Region( match.span()[0]+region.begin(), match.span()[1]+region.begin() )
			#print(c, color)
			if color:
				print("hex", c, color)
				self.draw("hex"+str(indx), c, color, indx)

		regex = re.compile("rgba\s?\([^\)]+\)", re.MULTILINE & re.IGNORECASE)
		regex_all = regex.findall(linha)
		iterator = regex.finditer(linha)

		for match in iterator:
			color = self.rgba2rgb(match.group())
			c = sublime.Region( match.span()[0]+region.begin(), match.span()[1]+region.begin() )
			if color:
				print("rgba", c, color)
				self.draw("rgba"+str(indx), c, color, indx)

		regex = re.compile("@\w+", re.MULTILINE & re.IGNORECASE)
		regex_all = regex.findall(linha)
		iterator = regex.finditer(linha)

		for match in iterator:
			nome = match.group()
			nome = nome.replace("@", "")
			color = self.arroba(nome)
			c = sublime.Region( match.span()[0]+region.begin(), match.span()[1]+region.begin() )
			if color:
				print("@", c, color)
				self.draw("@"+str(indx), c, color, indx)
		return False
		pass

	def arroba(self, nome):
		#print(nome)
		fn_colors = self.view.find("\s*"+nome+"\s+(#|@|rgba)\w+", sublime.IGNORECASE)
		fn_color = self.view.substr(fn_colors)
		#print(fn_color)
		temp = nome + " "
		fn_color = fn_color.replace(temp, "")
		#print(fn_color)
		if fn_color.find("#") >= 0:
			#fn_color = fn_color.replace(nome, "")
			return fn_color
		if fn_color.find("rgba") >= 0:
			return self.rgba2rgb(fn_color)
		if fn_color.find("@") >= 0:
			nome2 = fn_color.replace("@", "")
			self.arroba(nome2)
		pass

	def split_rgba(self, rgba_color):
		#fix = rgba_color.replace("rgba(", "")
		fix = re.sub("rgba\s?\(", "", rgba_color)
		fix = fix.replace(")", "")
		spt = fix.split(",")

		obj = rgba()
		obj.red = int(spt[0])
		obj.green = int(spt[1])
		obj.blue = int(spt[2])
		#obj.alpha = float(spt[3])

		return obj
		pass

	def rgba2rgb(self, rgba_color):
		#alpha = int(rgba_color.alpha*255)
		obj = self.split_rgba(rgba_color)

		red = int(obj.red)
		green = int(obj.green)
		blue = int(obj.blue)
		return '#{r:02x}{g:02x}{b:02x}'.format(r=red,g=green,b=blue)

	def clear_all(self):
		print("--------------")
		print("clearall...")
		line_total = self.view.rowcol(self.view.size())[0]+100
		for indx in range(line_total):
			self.view.erase_phantoms("hex"+str(indx))
			self.view.erase_phantoms("rgba"+str(indx))
			self.view.erase_phantoms("@"+str(indx))
		self.phantom_clear()
		pass

	def clear(self, region, indx, column):
		print("--------------")
		print("clear...")
		#self.view.erase_phantoms("hex"+str(indx))
		#self.view.erase_phantoms("rgba"+str(indx))
		#self.view.erase_phantoms("@"+str(indx))

		global phantoms
		for phantom in phantoms[::-1]:
			p = self.view.query_phantom(phantom)
			print("porra", p, region)
			if p[0].begin() == region.begin():
				print("eita", p)
				self.view.erase_phantom_by_id(phantom)
				phantoms.remove(phantom)
				break
			#print(region, p[0])
			#if region.begin() <= p[0].begin() and region.end() >= p[0].end():
				#self.view.erase_phantom_by_id(phantom)
				#phantoms.remove(phantom)
		pass

	def phantom_clear(self):
		print("--------------")
		print("phantom_clear...")
		global phantoms
		#print(phantoms)
		phantoms.clear()
		pass

	def phantom_fix(self):
		print("--------------")
		print("phantom_fix...")
		global phantoms
		for phantom in phantoms:
			p = self.view.query_phantom(phantom)
			if p[0].begin() < 0 and p[0].end() < 0:
				self.view.erase_phantom_by_id(phantom)
				phantoms.remove(phantom)
		pass

	def draw(self, layer, reg, cor, indx):
		print("--------------")
		print("draw...")
		global phantoms
		match = re.search("#(?:[0-9a-fA-F]{3}){1,2}", cor)
		if match:
			print(cor)
			phantoms.append( self.view.add_phantom(layer, reg, "<div style='padding: 8px; background-color: "+cor+";'></div>", sublime.LAYOUT_INLINE) )
		pass

class EventListener ( sublime_plugin.EventListener ):
	def on_modified ( self, view ):
		global line_total
		global flag
		if flag == False:
			return False
		#print( view.query_phantom(phantoms[1]) )
		#return False

		line_total_temp = view.rowcol(view.size())[0]+1
		if line_total != line_total_temp:
			line_total = line_total_temp
			#obj.clear_all()
			#flag = False
			#obj.start()
		else:
			#print("on_modified")
			line, column = view.rowcol(view.sel()[0].begin())
			print(line, column)
			region = view.line(sublime.Region(view.text_point(line, 0), view.text_point(line, 0)))
			reg_del = obj.reg_del(region, line, column)
			obj.clear(reg_del, line, column)
			obj.phantom_fix()
			reg_find = obj.reg_find(region, line, column)
			print("reg_find...", reg_find)
			obj.reg_color(reg_find, line)
			#print(line, column)
			#text = view.substr(view.line(view.sel()[0]))
		pass
	pass