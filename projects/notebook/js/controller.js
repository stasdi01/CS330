'use-strict';

class NoteController {
  constructor(model, view) {
      this.model = model;
      this.view = view;

      document.getElementById('addNote').addEventListener('click', this.handleAddNote.bind(this));
      this.view.bindDeleteNoteHandler(this.handleDeleteNote.bind(this));

      this.view.renderNotes(this.model.getNotes());
  }

  handleAddNote() {
      const title = document.getElementById('title').value.trim();
      const text = document.getElementById('text').value.trim();
      const color = document.getElementById('color').value;

      const missingTitle = !title;
      const missingText = !text;

      if (missingTitle || missingText) {
          this.view.showValidationErrors(missingTitle, missingText);
          return;
      }

      const date = new Date().toLocaleString();
      const note = { title, text, color, date };

      this.model.addNote(note);
      this.view.renderNotes(this.model.getNotes());
      this.view.clearForm();
      this.view.showValidationErrors(false, false);
  }

  handleDeleteNote(id) {
      this.model.deleteNote(id);
      this.view.renderNotes(this.model.getNotes());
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const model = new NoteModel();
  const view = new NoteView();
  new NoteController(model, view);
});
