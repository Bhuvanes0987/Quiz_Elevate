import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpErrorResponse, HttpClientModule } from '@angular/common/http';

// ================= INTERFACES =================

interface ClassItem {
  id: number;
  name: string;
  status: string;
  groupIds: number[];
  groupNames: string[];
}

interface Group {
  id: number;
  name: string;
}

@Component({
  selector: 'app-user-subjects',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './user-subjects.component.html',
  styleUrl: './user-subjects.component.css'
})
export class UserSubjectsComponent implements OnInit {

  pageMode: 'LIST' | 'ADD' = 'LIST';
  isEditMode = false;

  searchText = '';
  classes: ClassItem[] = [];
  groups: Group[] = [];

  isDropdownOpen = false;

  classForm: ClassItem = {
    id: 0,
    name: '',
    status: '',
    groupIds: [],
    groupNames: []
  };

  private API_URL = 'http://localhost:8000/api/user-classes';
  private GROUP_API_URL = 'http://localhost:8000/custom-field-groups';

  constructor(private http: HttpClient) {}

  // ================= INIT =================
  ngOnInit(): void {
    this.loadGroupsAndClasses();
  }

  // ================= LOAD GROUPS THEN CLASSES =================
  loadGroupsAndClasses(): void {
    this.http.get<any>(this.GROUP_API_URL).subscribe({
      next: res => {
        if (res.success) {
          this.groups = res.groups.map((g: any) => ({
            id: g.id,
            name: g.questionText || g.name
          }));

          // Load classes after groups are ready
          this.loadClasses();
        }
      },
      error: err => console.error('Failed to load groups', err)
    });
  }

  // ================= LOAD CLASSES =================
  loadClasses(): void {
    this.http.get<any>(this.API_URL).subscribe({
      next: res => {
        if (res.success) {

          this.classes = res.classes.map((c: any) => {

            const selectedIds: number[] = c.group_ids || [];

            const selectedNames = this.groups
              .filter(g => selectedIds.includes(g.id))
              .map(g => g.name);

            return {
              id: c.id,
              name: c.class_name,
              status: c.status || 'Active',
              groupIds: selectedIds,
              groupNames: selectedNames
            };
          });

        }
      },
      error: (err: HttpErrorResponse) =>
        console.error('Failed to load classes', err)
    });
  }

  // ================= FILTER =================
  filteredClasses(): ClassItem[] {
    if (!this.searchText.trim()) return this.classes;

    return this.classes.filter(c =>
      c.name.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }

  // ================= DROPDOWN =================
  toggleDropdown(): void {
    this.isDropdownOpen = !this.isDropdownOpen;
  }

  // ================= CHECKBOX CHANGE =================
  onGroupChange(event: any, id: number): void {

    if (event.target.checked) {
      if (!this.classForm.groupIds.includes(id)) {
        this.classForm.groupIds.push(id);
      }
    } else {
      this.classForm.groupIds =
        this.classForm.groupIds.filter(gid => gid !== id);
    }
  }

  // ================= DISPLAY SELECTED =================
  getSelectedNames(): string {
    const names = this.groups
      .filter(g => this.classForm.groupIds.includes(g.id))
      .map(g => g.name);

    return names.join(', ');
  }

  // ================= ADD =================
  openAddClass(): void {
    this.isEditMode = false;

    this.classForm = {
      id: 0,
      name: '',
      status: '',
      groupIds: [],
      groupNames: []
    };

    this.pageMode = 'ADD';
  }

  // ================= EDIT =================
  openEditClass(cls: ClassItem): void {

    this.isEditMode = true;

    this.classForm = {
      id: cls.id,
      name: cls.name,
      status: cls.status,
      groupIds: [...cls.groupIds],
      groupNames: []
    };

    this.pageMode = 'ADD';
  }

  // ================= SAVE =================
  saveClass(): void {

    if (!this.classForm.name.trim() ||
        !this.classForm.status ||
        this.classForm.groupIds.length === 0) {
      alert('Please fill all fields and select at least one subject');
      return;
    }

    const selectedSubjects = this.groups
      .filter(g => this.classForm.groupIds.includes(g.id))
      .map(g => g.name);

    const payload = {
      className: this.classForm.name,
      status: this.classForm.status,
      groupIds: this.classForm.groupIds,
      subjects: selectedSubjects,
      createdBy: 'admin',
      updatedBy: 'admin'
    };

    const request = this.isEditMode
      ? this.http.put<any>(`${this.API_URL}/${this.classForm.id}`, payload)
      : this.http.post<any>(this.API_URL, payload);

    request.subscribe({
      next: response => {
        console.log('Response:', response);
        this.goBack();
        this.loadClasses();
      },
      error: err => {
        console.error('Save failed', err);
      }
    });
  }

  // ================= DELETE =================
  deleteClass(id: number): void {

    if (!confirm('Are you sure you want to delete this class?')) return;

    this.http.delete<any>(`${this.API_URL}/${id}`)
      .subscribe(() => this.loadClasses());
  }

  // ================= NAV =================
  goBack(): void {
    this.pageMode = 'LIST';
    this.isEditMode = false;
    this.isDropdownOpen = false;
  }
}
