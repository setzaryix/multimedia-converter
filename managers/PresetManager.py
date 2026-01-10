import json
import os

class PresetManager:

	PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	PRESET_FOLDER = os.path.join(PROJECT_ROOT, 'preset')
	CONVERSION_PRESET_FILE = os.path.join(PRESET_FOLDER, 'preset.json')

	def __init__(self):
		self.conversion_preset = self.load_conversion_preset()

	def load_conversion_preset(self):
		""" Load the list of conversion preset. """
		with open(self.CONVERSION_PRESET_FILE, 'r', encoding='utf-8') as f:
			return json.load(f)