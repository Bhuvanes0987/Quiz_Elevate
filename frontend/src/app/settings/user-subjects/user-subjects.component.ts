// import { Component } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { FormsModule } from '@angular/forms';

// interface ClassItem {
//   id: number;
//   name: string;
// }


// @Component({
//   selector: 'app-user-subjects',
//   imports: [CommonModule, FormsModule],
//   standalone: true,
//   templateUrl: './user-subjects.component.html',
//   styleUrl: './user-subjects.component.css',
// })
// export class UserSubjectsComponent {

  
//   pageMode: 'LIST' | 'ADD' | 'EDIT' = 'LIST';

//   searchText = '';

//   classes: ClassItem[] = [
//     { id: 1, name: 'Class 1' },
//     { id: 2, name: 'Class 2' }
//   ];

//   classForm: ClassItem = {
//     id: 0,
//     name: ''
//   };

//   // ===== FILTER =====
//   get filteredClasses(): ClassItem[] {
//     if (!this.searchText.trim()) return this.classes;
//     return this.classes.filter(c =>
//       c.name.toLowerCase().includes(this.searchText.toLowerCase())
//     );
//   }

//   // ===== ADD =====
//   openAddClass() {
//     this.classForm = { id: 0, name: '' };
//     this.pageMode = 'ADD';
//   }

//   saveClass() {
//     if (!this.classForm.name.trim()) return;

//     this.classes.push({
//       id: Date.now(),
//       name: this.classForm.name
//     });

//     this.goBack();
//   }

//   // ===== DELETE =====
//   deleteClass(id: number) {
//     this.classes = this.classes.filter(c => c.id !== id);
//   }

//   // ===== NAV =====
//   goBack() {
//     this.pageMode = 'LIST';
//   }
// }

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';


interface ClassItem {
  id: number;
  name: string;
}

@Component({
  selector: 'app-user-subjects',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-subjects.component.html',
  styleUrl: './user-subjects.component.css'
})
export class UserSubjectsComponent implements OnInit {

  pageMode: 'LIST' | 'ADD' = 'LIST';

  searchText = '';
  classes: { id: number; name: string }[] = [];

  classForm = {
    id: 0,
    name: ''
  };

  private API_URL = 'http://localhost:8000/user-classes';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadClasses();
  }

  // ================= LOAD CLASSES =================
  loadClasses() {
    this.http.get<any>(this.API_URL).subscribe({
      next: res => {
        if (res.success) {
          this.classes = res.classes.map((c: any) => ({
            id: c.id,
            name: c.class_name
          }));
        }
      },
      error: (err: HttpErrorResponse) => {
        console.error('Failed to load classes', err);
      }
    });
  }

  // ================= FILTER =================
  get filteredClasses() {
    if (!this.searchText.trim()) return this.classes;
    return this.classes.filter(c =>
      c.name.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }

  // ================= ADD =================
  openAddClass() {
    this.classForm = { id: 0, name: '' };
    this.pageMode = 'ADD';
  }

  saveClass() {
    if (!this.classForm.name.trim()) return;

    const payload = {
      className: this.classForm.name,
      createdBy: 'admin'
    };

    this.http.post<any>(this.API_URL, payload).subscribe({
      next: res => {
        if (res.success) {
          this.goBack();
          this.loadClasses();
        }
      },
      error: (err: HttpErrorResponse) => {
        console.error('Failed to save class', err);
      }
    });
  }

  // ================= DELETE =================
  deleteClass(id: number) {
    if (!confirm('Are you sure you want to delete this class?')) return;

    this.http.delete<any>(`${this.API_URL}/${id}`).subscribe({
      next: res => {
        if (res.success) {
          this.loadClasses();
        }
      },
      error: (err: HttpErrorResponse) => {
        console.error('Failed to delete class', err);
      }
    });
  }

  // ================= NAV =================
  goBack() {
    this.pageMode = 'LIST';
  }
}
