import numpy as np

"""
"""
class ObjLoader:
	def __init__(self):
		self.vertex_cords  = []
		self.texture_cords = []
		self.norm_cords    = []

		self.vertex_index  = []
		self.texture_index = []
		self.normal_index  = []
		self.model         = []

	def load_model(self, file):
		for line in open(file, 'r'):
			if line.startswith('#'):
				continue
			values = line.split()
			if not values:
				continue
			if values[0] == 'v':
				self.vertex_cords.append(values[1:4])
			if values[0] == 'vt':
				self.texture_cords.append(values[1:3])
			if values[0] == 'vn':
				self.norm_cords.append(values[1:4])
			if values[0] == 'f':
				face_i = []
				texture_i = []
				normal_i = []
				for v in values[1:4]:
					w = v.split('/')
					face_i.append(int(w[0])-1)
					if w[1]:
						texture_i.append(int(w[1])-1)
					else:
						texture_i.append(0)
					normal_i.append(int(w[2])-1)
				self.vertex_index.append(face_i)
				self.texture_index.append(texture_i)
				self.normal_index.append(normal_i)
		self.vertex_index = [y for x in self.vertex_index for y in x]
		self.texture_index = [y for x in self.texture_index for y in x]
		self.normal_index = [y for x in self.normal_index for y in x]

		for i in self.vertex_index:
			self.model.extend(self.vertex_cords[i])
		for i in self.texture_index:
			self.model.extend(self.texture_cords[i])
		# for i in self.normal_index:
			# self.model.extend(self.norm_cords[i])
		self.model = np.array(self.model, dtype='float32')