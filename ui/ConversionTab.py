import os
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QLineEdit, QPushButton, QCheckBox, QComboBox, QTextEdit, QProgressBar, QFileDialog, QMenu
from PySide6.QtCore import Qt, Slot

from threads.Conversion import ConversionThread

class ConversionTab(QWidget):
	update_progress = Slot(str, int, str)

	def __init__(self, conversion_preset, parent=None):
		super().__init__(parent)
		self.conversion_preset = conversion_preset
		self.conversion_thread = None

		# Main Layout
		main_layout = QHBoxLayout()

		# Left Frame Section
		left_frame = QFrame()
		left_frame.setFrameShape(QFrame.Panel)
		left_frame.setFrameShadow(QFrame.Plain)
		left_frame.setLineWidth(2)

		left_frame_layout = QVBoxLayout(left_frame)

		# File List Section
		list_layout = QVBoxLayout()
		list_label = QLabel("Files")
		self.file_list = QListWidget()

		list_layout.addWidget(list_label)
		list_layout.addWidget(self.file_list)
		list_layout.setStretch(0, 0)
		list_layout.setStretch(1, 1)

		left_frame_layout.addLayout(list_layout)

		# Right frame Section
		right_frame = QFrame()
		right_frame.setFrameShape(QFrame.Panel)
		right_frame.setFrameShadow(QFrame.Plain)
		right_frame.setLineWidth(2)

		right_frame_layout = QVBoxLayout(right_frame)

		# Add and Remove Buttons Section
		button_layout = QHBoxLayout()
		self.add_button = QPushButton("Add")
		self.add_button.setAccessibleName("Add")
		self.add_button.setAccessibleDescription("Click to add one or more media files.")
		self.add_button.setToolTip("Click to add one or more media files.")
		self.add_button.clicked.connect(self.add_files)

		self.remove_button = QPushButton("Remove")
		self.remove_button.setAccessibleName("Remove")
		self.remove_button.setAccessibleDescription("Removing items from the file list. Choose to remove selected items or all items.")
		self.remove_button.setToolTip("Removing items from the file list. Choose to remove selected items or all items.")
		self.remove_button.clicked.connect(self.show_remove_menu)

		button_layout.addWidget(self.add_button)
		button_layout.addWidget(self.remove_button)

		right_frame_layout.addLayout(button_layout)

		# Destination Section
		dest_layout = QHBoxLayout()
		self.dest_label = QLabel("Destination Folder:")

		PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		SAVED_FOLDER = os.path.join(PROJECT_ROOT, 'converted')
		os.makedirs(SAVED_FOLDER, exist_ok=True)

		self.dest_input = QLineEdit(SAVED_FOLDER)
		self.dest_input.setAccessibleName("Destination Folder:")
		self.dest_input.setAccessibleDescription("Specify the folder where converted files will be saved.")
		self.dest_input.setToolTip("Specify the folder where converted files will be saved.")

		self.browse_button = QPushButton("Browse...")
		self.browse_button.setAccessibleName("Browse...")
		self.browse_button.setAccessibleDescription("Open a dialog to select the destination folder.")
		self.browse_button.setToolTip("Open a dialog to select the destination folder.")
		self.browse_button.clicked.connect(self.browse_folder)

		dest_layout.addWidget(self.dest_label)
		dest_layout.addWidget(self.dest_input)
		dest_layout.addWidget(self.browse_button)

		right_frame_layout.addLayout(dest_layout)

		# Preset Options
		options_layout = QVBoxLayout()

		preset_options = QVBoxLayout()
		self.preset_label = QLabel("Conversion Preset")
		self.preset_combo = QComboBox()
		self.preset_combo.addItems(self.conversion_preset.keys())
		self.preset_combo.setCurrentIndex(1)
		self.preset_combo.setAccessibleName("Conversion Preset")
		self.preset_combo.setAccessibleDescription("Choose a conversion preset.")
		self.preset_combo.setToolTip("Choose a conversion preset.")

		preset_options.addWidget(self.preset_label)
		preset_options.addWidget(self.preset_combo)

		options_layout.addLayout(preset_options)

		right_frame_layout.addLayout(options_layout)

		# Convert Button Section
		conversion_layout = QHBoxLayout()
		self.convert_button = QPushButton("Convert")
		self.convert_button.setAccessibleName("Convert")
		self.convert_button.setAccessibleDescription("Start converting the selected media file.")
		self.convert_button.setToolTip("Start converting the selected media file.")
		self.convert_button.clicked.connect(self.convert_file)
		conversion_layout.addWidget(self.convert_button, alignment=Qt.AlignCenter)

		right_frame_layout.addLayout(conversion_layout)

		# Log Section
		log_layout = QVBoxLayout()
		self.log_label = QLabel("Conversion Status")
		self.log_output = QTextEdit()
		self.log_output.setReadOnly(True)
		self.log_output.setAccessibleName("Conversion Status")
		self.log_output.setAccessibleDescription("The conversion progress and status logs.")
		self.log_output.setToolTip("The conversion progress and status logs.")

		log_layout.addWidget(self.log_label)
		log_layout.addWidget(self.log_output)

		log_layout.setStretch(0, 0)
		log_layout.setStretch(1, 1)

		right_frame_layout.addLayout(log_layout)

		# Progress Bar
		progress_bar_layout = QHBoxLayout()
		self.progress_bar = QProgressBar()
		self.progress_bar.setMinimum(0)
		self.progress_bar.setMaximum(100)
		progress_bar_layout.addWidget(self.progress_bar)



		# Set Layout
		main_layout.addWidget(left_frame)
		main_layout.addWidget(right_frame)

		main_layout.setStretch(0, 1)
		main_layout.setStretch(1, 2)

		main_layout.addLayout(progress_bar_layout)

		main_layout.setContentsMargins(10, 10, 10, 10)
		main_layout.setSpacing(15)
		self.setLayout(main_layout)



	# Class Method
	def add_files(self):
		"""	Open a file dialog to allow the user to select one or more files. """
		file_filter = "Media Files (*.mp3 *.mp4 *.avi *.wav *.mkv *.flv *.mov *.webm);;All Files (*)"

		files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", file_filter)
		if files:
			for file in files:
				normalize_path = os.path.normpath(file)
				self.file_list.addItem(normalize_path)

	def show_remove_menu(self):
		"""	Shows a context menu with options to remove selected item or all items. """
		context_menu = QMenu(self.remove_button)
		context_menu.setAccessibleName("Context Menu")

		remove_selected_action = context_menu.addAction("Remove selected item")
		remove_selected_action.triggered.connect(self.remove_selected_item)

		remove_all_action = context_menu.addAction("Remove all")
		remove_all_action.triggered.connect(self.remove_all_items)

		context_menu.exec_(self.remove_button.mapToGlobal(self.remove_button.pos()))

	def remove_selected_item(self):
		"""	Removes the selected item from the list. """
		selected_items = self.file_list.selectedItems()
		if selected_items:
			for item in selected_items:
				row = self.file_list.row(item)
				self.file_list.takeItem(row)

	def remove_all_items(self):
		"""	Removes all items from the list. """
		self.file_list.clear()

	def browse_folder(self):
		"""	Opens a dialog to select a destination folder and updates the destination input field. """
		folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
		if folder:
			normalize_path = os.path.normpath(folder)
			self.dest_input.setText(normalize_path)

	def convert_file(self):
		self.media_files = []
		destination = self.dest_input.text().strip()
		selected_preset = self.preset_combo.currentText()

		for index in range(self.file_list.count()):
			file = self.file_list.item(index)
			self.media_files.append(file.text())

		self.conversion_thread = ConversionThread(
			self.media_files,
			destination,
			selected_preset,
			self.conversion_preset,
		)

		self.conversion_thread.progress_signal.connect(self.update_progress)
		self.conversion_thread.completion_signal.connect(self.display_completion_message)
		self.conversion_thread.finished.connect(self.conversion_finished)

		self.add_button.setEnabled(False)
		self.remove_button.setEnabled(False)

		self.preset_combo.setEnabled(False)

		self.convert_button.setEnabled(False)
		self.convert_button.setText("Converting...")
		self.convert_button.setAccessibleName("Converting...")
		self.convert_button.setAccessibleDescription("Conversion is in progress")
		self.convert_button.setToolTip("Conversion is in progress")

		self.log_output.append("Preparing conversion process")
		self.conversion_thread.start()

	def display_completion_message(self, message):
		self.log_output.append(message)

	def conversion_finished(self):
		"""	Handles post-conversion cleanup and resets the convert button. """
		self.file_list.clear()
		self.media_files.clear()

		self.add_button.setEnabled(True)
		self.remove_button.setEnabled(True)

		self.preset_combo.setEnabled(True)

		self.convert_button.setEnabled(True)
		self.convert_button.setText("Convert")
		self.convert_button.setAccessibleName("Convert")
		self.convert_button.setAccessibleDescription("Start converting the selected media file.")
		self.convert_button.setToolTip("Start converting the selected media file.")

		self.conversion_thread = None

	def stop_conversion(self):
		"""	Stops the ongoing conversion by terminating the conversion thread if it's running. """
		if self.conversion_thread and self.conversion_thread.isRunning():
			self.conversion_thread.terminate()
			self.conversion_thread.wait()
			self.conversion_thread = None

	@Slot(str, int, str)
	def update_progress(self, message, percent, status):
		if status != "processing":
			self.log_output.clear()
			self.progress_bar.setValue(0)

		self.log_output.append(message)
		self.progress_bar.setValue(percent)