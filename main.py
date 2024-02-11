import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
import markdown2

class Note:
    def __init__(self, name, content):
        self.name = name
        self.content = content

class NoteLibrary:
    def __init__(self):
        self.notes = {}

    def add_note(self, note):
        self.notes[note.name] = note

    def delete_note(self, name):
        if name in self.notes:
            del self.notes[name]

    def get_note_names(self):
        return list(self.notes.keys())

    def get_note_content(self, name):
        if name in self.notes:
            return self.notes[name].content
        return None

    def update_note_content(self, name, content):
        if name in self.notes:
            self.notes[name].content = content

class NoteEditor(BoxLayout):
    note_name = StringProperty()
    note_content = StringProperty()

    def __init__(self, **kwargs):
        super(NoteEditor, self).__init__(**kwargs)
        self.note_name = ""
        self.note_content = ""
        self.note_library = NoteLibrary()

    def create_note_popup(self):
        popup = Popup(title='Create New Note', size_hint=(0.8, 0.6))
        layout = BoxLayout(orientation='vertical')
        name_input = TextInput(hint_text='Enter note name', multiline=False)
        content_input = TextInput(hint_text='Enter note content (supports Markdown)', multiline=True)
        save_button = Button(text='Save', size_hint=(1, 0.2))

        def save_note(instance):
            note_name = name_input.text.strip()
            note_content = content_input.text.strip()
            if note_name:
                note = Note(note_name, note_content)
                self.note_library.add_note(note)
                self.update_notes_list()
                popup.dismiss()

        save_button.bind(on_press=save_note)

        layout.add_widget(name_input)
        layout.add_widget(content_input)
        layout.add_widget(save_button)

        popup.content = layout
        popup.open()

    def update_notes_list(self):
        self.clear_widgets()
        for note_name in self.note_library.get_note_names():
            note_label = Button(text=note_name, size_hint_y=None, height=40)
            note_label.bind(on_release=self.load_note)
            self.add_widget(note_label)

    def load_note(self, instance):
        note_name = instance.text
        self.note_name = note_name
        self.note_content = self.note_library.get_note_content(note_name)

    def save_note(self):
        if self.note_name:
            self.note_library.update_note_content(self.note_name, self.note_content)
            self.update_notes_list()
            self.note_name = ""
            self.note_content = ""

    def delete_note_popup(self):
        if self.note_name:
            popup = Popup(title='Delete Note', content=Label(text=f'Delete note "{self.note_name}"?'), size_hint=(None, None), size=(300, 200))
            popup.open = self.delete_note
            popup.open()

    def delete_note(self, _):
        self.note_library.delete_note(self.note_name)
        self.update_notes_list()
        self.note_name = ""
        self.note_content = ""
        popup.dismiss()

class NotesApp(App):
    def build(self):
        return NoteEditor()

if __name__ == '__main__':
    NotesApp().run()
