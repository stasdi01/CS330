'use-strict';
class NoteModel {
  constructor() {
      this.notes = JSON.parse(localStorage.getItem('notes')) || [];
  }

  getNotes() {
      return this.notes;
  }

  addNote(note) {
      note.id = Date.now().toString();
      this.notes.push(note);
      this._commit();
  }

  deleteNote(id) {
      this.notes = this.notes.filter(note => note.id !== id);
      this._commit();
  }

  _commit() {
      localStorage.setItem('notes', JSON.stringify(this.notes));
  }
}
