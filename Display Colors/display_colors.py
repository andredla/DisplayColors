import sublime
import sublime_plugin
import re

class rgba(object):
	red = 0
	green = 0
	blue = 0
	alpha = 0

class ClearallCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print("clearall")
		self.view.erase_phantoms("hex")
		self.view.erase_phantoms("rgba")
		self.view.erase_phantoms("@")
		pass


class DisplaycolorsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#self.view.insert(edit, 0, "Hello, World!")
		#print( self.view.substr(sublime.Region(0, self.view.size())) )
		#print( self.view.find("#\w+", 0, sublime.IGNORECASE) )
		#print( self.view.find_all("#\w+", sublime.IGNORECASE) )
		#self.view.show(colors[0])

		self.clear()

		#self.view.erase_phantoms ("hex")
		colors = self.view.find_all("#\w+", sublime.IGNORECASE)
		for c in colors:
			color = self.view.substr(c)
			#self.view.add_phantom("hex", c, "<div style='padding: 8px; background-color: "+color+";'></div>", sublime.LAYOUT_INLINE)
			self.draw("hex", c, color)

		#self.view.erase_phantoms ("rgba")
		colors = self.view.find_all("rgba\s?\([^\)]+\)", sublime.IGNORECASE)
		for c in colors:
			color = self.rgba2rgb(self.view.substr(c))
			#self.view.add_phantom("rgba", c, "<div style='padding: 8px; background-color: "+color+";'></div>", sublime.LAYOUT_INLINE)
			self.draw("rgba", c, color)

		#self.view.erase_phantoms ("@")
		colors = self.view.find_all("@\w+", sublime.IGNORECASE)
		for c in colors:
			nome = self.view.substr(c)
			nome = nome.replace("@", "")
			color = self.arroba(nome)
			print(color)
			if color:
				#self.view.add_phantom("@", c, "<div style='padding: 8px; background-color: "+color+";'></div>", sublime.LAYOUT_INLINE)
				self.draw("@", c, color)
		pass

	def arroba(self, nome):
		print(nome)
		fn_colors = self.view.find("\s*"+nome+"\s+(#|@|rgba)\w+", sublime.IGNORECASE)
		fn_color = self.view.substr(fn_colors)
		print(fn_color)
		temp = nome + " "
		fn_color = fn_color.replace(temp, "")
		print(fn_color)
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


	def clear(self):
		self.view.erase_phantoms("hex")
		self.view.erase_phantoms("rgba")
		self.view.erase_phantoms("@")
		pass

	def draw(self, layer, reg, cor):
		match = re.search("#(?:[0-9a-fA-F]{3}){1,2}", cor)
		if match:
			self.view.add_phantom(layer, reg, "<div style='padding: 8px; background-color: "+cor+";'></div>", sublime.LAYOUT_INLINE)
		pass