import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface CustomField {
  id: number;
  name: string;
}

interface Group {
  id: number;
  questionText: string; // group name (kept same as your HTML)
  fields: CustomField[];
}

@Component({
  selector: 'app-custom-field-groups',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './custom-field-groups.component.html',
  styleUrls: ['./custom-field-groups.component.css']
})
// export class CustomFieldGroupsComponent {


//   showAddPanel = false;
//   showEditPanel = false;
//   editingId: number | null = null;

//   searchText = '';


//   questions: CustomFieldGroup[] = [
//     {
//       id: 1,
//       questionText: 'General Information',
//       fields: [
//         { id: 1, name: 'Email' },
//         { id: 2, name: 'Phone Number' }
//       ]
//     },
//     {
//       id: 2,
//       questionText: 'Address Details',
//       fields: []
//     }
//   ];

//   form: CustomFieldGroup = this.getEmptyForm();


//   get filteredQuestions(): CustomFieldGroup[] {
//     if (!this.searchText.trim()) {
//       return this.questions;
//     }
//     return this.questions.filter(q =>
//       q.questionText.toLowerCase().includes(this.searchText.toLowerCase())
//     );
//   }

//   openAddPanel(): void {
//     this.form = this.getEmptyForm();
//     this.editingId = null;
//     this.showAddPanel = true;
//     this.showEditPanel = false;
//   }

//   openEditPanel(group: CustomFieldGroup): void {
//     this.form = JSON.parse(JSON.stringify(group)); 
//     this.editingId = group.id;
//     this.showEditPanel = true;
//     this.showAddPanel = false;
//   }

//   closePanel(): void {
//     this.showAddPanel = false;
//     this.showEditPanel = false;
//     this.editingId = null;
//   }

//   saveQuestion(): void {
//     if (!this.form.questionText.trim()) {
//       return;
//     }

//     // ADD
//     if (this.editingId === null) {
//       this.form.id = Date.now();
//       this.questions.push({ ...this.form });
//     }
//     // UPDATE
//     else {
//       const index = this.questions.findIndex(q => q.id === this.editingId);
//       if (index !== -1) {
//         this.questions[index] = { ...this.form };
//       }
//     }

//     this.closePanel();
//   }

//   deleteQuestion(id: number): void {
//     this.questions = this.questions.filter(q => q.id !== id);
//   }


//   addField(): void {
//     const name = prompt('Enter field name');
//     if (!name) return;

//     this.form.fields.push({
//       id: Date.now(),
//       name
//     });
//   }

//   deleteField(index: number): void {
//     this.form.fields.splice(index, 1);
//   }

//   moveFieldUp(index: number): void {
//     if (index === 0) return;
//     [this.form.fields[index - 1], this.form.fields[index]] =
//       [this.form.fields[index], this.form.fields[index - 1]];
//   }

//   moveFieldDown(index: number): void {
//     if (index === this.form.fields.length - 1) return;
//     [this.form.fields[index + 1], this.form.fields[index]] =
//       [this.form.fields[index], this.form.fields[index + 1]];
//   }

//   editField(index: number): void {
//     const name = prompt('Edit field name', this.form.fields[index].name);
//     if (name) {
//       this.form.fields[index].name = name;
//     }
//   }

//   private getEmptyForm(): CustomFieldGroup {
//     return {
//       id: 0,
//       questionText: '',
//       fields: []
//     };
//   }
// }
// import { Component } from '@angular/core';

// interface CustomField {
//   name: string;
// }

// interface Group {
//   id: number;
//   questionText: string;
//   fields: CustomField[];
// }

// @Component({
//   selector: 'app-custom-field-groups',
//   templateUrl: './custom-field-groups.component.html',
//   styleUrls: ['./custom-field-groups.component.css']
// })
export class CustomFieldGroupsComponent {

  pageMode: 'LIST' | 'EDIT' = 'LIST';

  searchText = '';

groups: Group[] = [];

  form: Group = this.getEmptyForm();

  // Filtered list based on search text
  get filteredGroups() {
    if (!this.searchText.trim()) return this.groups;
    return this.groups.filter(g =>
      g.questionText.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }

  // Open edit page
  openEditPage(group: Group) {
    this.form = JSON.parse(JSON.stringify(group)); // deep copy
    this.pageMode = 'EDIT';
  }

  // Open add page
  openAddPage() {
    this.form = this.getEmptyForm();
    this.pageMode = 'EDIT';
  }

  // Save or update the group
  saveGroup() {
    if (!this.form.questionText.trim()) return;

    if (this.form.id === 0) {
      // Add new
      this.form.id = Date.now();
      this.groups.push(JSON.parse(JSON.stringify(this.form)));
    } else {
      // Update existing
      const index = this.groups.findIndex(g => g.id === this.form.id);
      if (index !== -1) {
        this.groups[index] = JSON.parse(JSON.stringify(this.form));
      }
    }

    this.goBack();
  }

  // Delete a group
  deleteGroup(id: number) {
    this.groups = this.groups.filter(g => g.id !== id);
  }

  // Add a field
addField() {
  this.form.fields.push({ id: Date.now(), name: 'New Field' });
}
editField(index: number): void {
  const name = prompt('Edit field name', this.form.fields[index].name);
  if (name) {
    this.form.fields[index].name = name;
  }
}
updateGroup(): void {
  if (!this.form.questionText.trim()) return;

  // Add new group
  if (this.form.id === 0) {
    this.form.id = Date.now(); // unique ID
    this.groups.push(JSON.parse(JSON.stringify(this.form)));
  } 
  // Update existing group
  else {
    const index = this.groups.findIndex(g => g.id === this.form.id);
    if (index !== -1) {
      this.groups[index] = JSON.parse(JSON.stringify(this.form));
    }
  }

  this.goBack(); // return to LIST mode
}


  // Remove a field
  removeField(index: number) {
    this.form.fields.splice(index, 1);
  }

  // Move field up
  moveUp(index: number) {
    if (index === 0) return;
    [this.form.fields[index - 1], this.form.fields[index]] =
    [this.form.fields[index], this.form.fields[index - 1]];
  }

  // Move field down
  moveDown(index: number) {
    if (index === this.form.fields.length - 1) return;
    [this.form.fields[index + 1], this.form.fields[index]] =
    [this.form.fields[index], this.form.fields[index + 1]];
  }

  // Cancel and go back to list
  goBack() {
    this.pageMode = 'LIST';
  }

  // Utility to get empty form
  private getEmptyForm(): Group {
    return {
      id: 0,
      questionText: '',
      fields: []
    };
  }
  get filteredQuestions() {
  if (!this.searchText.trim()) return this.groups;
  return this.groups.filter(g =>
    g.questionText.toLowerCase().includes(this.searchText.toLowerCase())
  );
}

}
