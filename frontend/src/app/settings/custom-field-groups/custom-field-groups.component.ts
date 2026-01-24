import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { catchError, of } from 'rxjs';

interface CustomField {
  id: number;
  name: string;
}

interface Group {
  id: number;
  questionText: string; // group name
  fields: CustomField[];
}

@Component({
  selector: 'app-custom-field-groups',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './custom-field-groups.component.html',
  styleUrls: ['./custom-field-groups.component.css']
})
export class CustomFieldGroupsComponent implements OnInit {

  pageMode: 'LIST' | 'EDIT' = 'LIST';
  searchText = '';
  groups: Group[] = [];
  form: Group = this.getEmptyForm();

  // Backend API URL
  private API_URL = 'http://localhost:8000/api/custom-field-groups';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadGroups();
  }

  // ----------------------
  // Load all groups
  // ----------------------
  loadGroups() {
    this.http.get<{ success: boolean, groups: Group[] }>(this.API_URL)
      .pipe(catchError(err => { console.error(err); return of({ success: false, groups: [] }); }))
      .subscribe(res => {
        if (res.success) {
          this.groups = res.groups;
        }
      });
  }

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

  // ----------------------
  // Save or update group
  // ----------------------
  updateGroup(): void {
    if (!this.form.questionText.trim()) return;

    if (this.form.id === 0) {
      // Create new group
      this.http.post<{ success: boolean, message: string }>(this.API_URL, this.form)
        .pipe(catchError(err => { console.error(err); return of({ success: false, message: 'Error' }); }))
        .subscribe(res => {
          if (res.success) {
            this.loadGroups();
            this.goBack();
          } else {
            alert('Failed to create group: ' + res.message);
          }
        });
    } else {
      // Update existing group
      const url = `${this.API_URL}/${this.form.id}`;
      this.http.put<{ success: boolean, message: string }>(url, this.form)
        .pipe(catchError(err => { console.error(err); return of({ success: false, message: 'Error' }); }))
        .subscribe(res => {
          if (res.success) {
            this.loadGroups();
            this.goBack();
          } else {
            alert('Failed to update group: ' + res.message);
          }
        });
    }
  }

  // ----------------------
  // Delete group
  // ----------------------
  deleteGroup(id: number) {
    if (!confirm('Are you sure you want to delete this group?')) return;
    const url = `${this.API_URL}/${id}`;
    this.http.delete<{ success: boolean, message: string }>(url)
      .pipe(catchError(err => { console.error(err); return of({ success: false, message: 'Error' }); }))
      .subscribe(res => {
        if (res.success) {
          this.loadGroups();
        } else {
          alert('Failed to delete group: ' + res.message);
        }
      });
  }

  // ----------------------
  // Field management
  // ----------------------
  addField() {
    this.form.fields.push({ id: Date.now(), name: 'New Field' });
  }

  editField(index: number): void {
    const name = prompt('Edit field name', this.form.fields[index].name);
    if (name) {
      this.form.fields[index].name = name;
    }
  }

  removeField(index: number) {
    this.form.fields.splice(index, 1);
  }

  moveUp(index: number) {
    if (index === 0) return;
    [this.form.fields[index - 1], this.form.fields[index]] =
      [this.form.fields[index], this.form.fields[index - 1]];
  }

  moveDown(index: number) {
    if (index === this.form.fields.length - 1) return;
    [this.form.fields[index + 1], this.form.fields[index]] =
      [this.form.fields[index], this.form.fields[index + 1]];
  }

  goBack() {
    this.pageMode = 'LIST';
    this.form = this.getEmptyForm();
  }

  private getEmptyForm(): Group {
    return {
      id: 0,
      questionText: '',
      fields: []
    };
  }
}
