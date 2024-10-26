'use-strict';

class NoteView {
  constructor() {
      this.notesContainer = document.getElementById('notesContainer');
      this.titleField = document.getElementById('fieldTitle').querySelector('.help');
      this.textField = document.getElementById('fieldText').querySelector('.help');
  }

  clearForm() {
      document.getElementById('title').value = '';
      document.getElementById('text').value = '';
      document.getElementById('color').value = 'is-primary';
  }

  renderNotes(notes) {
      this.notesContainer.innerHTML = '';

      const groupedNotes = notes.reduce((groups, note) => {
          if (!groups[note.color]) groups[note.color] = [];
          groups[note.color].push(note);
          return groups;
      }, {});

      Object.keys(groupedNotes).forEach(color => {
          const colorGroup = document.createElement('div');
          colorGroup.className = `message ${color}`;
          colorGroup.innerHTML = `<div class="message-header">${color.replace('is-', '').toUpperCase()}</div>`;

          groupedNotes[color].forEach(note => {
              const noteElement = document.createElement('div');
              noteElement.className = `message-body note`;
              noteElement.innerHTML = `
              <button class="delete deleteNote" data-id="${note.id}"></button>
                  <p><strong>${note.title}</strong> - ${note.date} </p>
                  <p>${note.text}</p>
                  
              `;
              colorGroup.appendChild(noteElement);
          });

          this.notesContainer.appendChild(colorGroup);
      });
  }

  showValidationErrors(missingTitle, missingText) {
      this.titleField.classList.toggle('is-hidden', !missingTitle);
      this.textField.classList.toggle('is-hidden', !missingText);
  }

  bindDeleteNoteHandler(handler) {
      this.notesContainer.addEventListener('click', (event) => {
          if (event.target.classList.contains('deleteNote')) {
              const id = event.target.getAttribute('data-id');
              handler(id);
          }
      });
  }
}
