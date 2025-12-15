// import { Component } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { FormsModule } from '@angular/forms';
// import { HttpClient, HttpClientModule } from '@angular/common/http';

// @Component({
//   selector: 'app-custom-fields',
//   standalone: true,
//   imports: [CommonModule, FormsModule, HttpClientModule],
//   templateUrl: './custom-fields.html',
//   styleUrls: ['./custom-fields.css'],
// })
// export class CustomFieldsComponent {
//   searchText = '';
//   questions: any[] = [];
//   showAddPanel = false;
//   editingQuestion: any | null = null;


//   form: any = {
//     id: null,
//     questionText: '',
//     questionType: 'choose',
//     options: ['', '', '', ''],
//     correctAnswer: 0,
//     matchPairs: [{ left: '', right: '' }],
//     correctAnswerText: '',
//     mapImageBase64: '',
//   };

//   constructor(private http: HttpClient) {
//     this.loadQuestions();
//   }

//   loadQuestions() {
//     this.http.get('http://localhost:8000/questions').subscribe((res: any) => {
//       this.questions = res?.questions ?? [];
//     });
//   }

//   get filteredQuestions() {
//     const t = this.searchText?.trim().toLowerCase();
//     if (!t) return this.questions;
//     return this.questions.filter(q =>
//       (q.question_text ?? '').toLowerCase().includes(t)
//     );
//   }

//   openAddPanel() {
//     this.resetForm();
//     this.showAddPanel = true;
//     this.editingQuestion = null;
//   }

//   openEditPanel(q: any) {
//     this.editingQuestion = q;
//     this.showAddPanel = true;

//     this.form.id = q.id;
//     this.form.questionText = q.question_text ?? '';
//     this.form.questionType = q.question_type ?? 'choose';

//     try {
//       const ans = typeof q.answer_data === 'string'
//         ? JSON.parse(q.answer_data)
//         : q.answer_data;

//       if (ans) {
//         if (Array.isArray(ans.options)) this.form.options = ans.options;
//         if (ans.correct !== undefined) this.form.correctAnswer = ans.correct;
//         if (Array.isArray(ans.matchPairs)) this.form.matchPairs = ans.matchPairs;
//         if (ans.fillup_answer) this.form.correctAnswerText = ans.fillup_answer;
//       }
//     } catch {}

//     if (q.map_image) {
//       this.form.mapImageBase64 = q.map_image;
//     }
//   }

//   closePanel() {
//     this.showAddPanel = false;
//     this.resetForm();
//     this.editingQuestion = null;
//     this.loadQuestions();
//   }

//   deleteQuestion(id: number) {
//     if (!confirm('Delete this question?')) return;
//     this.http.delete(`http://localhost:8000/questions/${id}`).subscribe(() => {
//       this.loadQuestions();
//     });
//   }

//   resetForm() {
//     this.form = {
//       id: null,
//       questionText: '',
//       questionType: 'choose',
//       options: ['', '', '', ''],
//       correctAnswer: 0,
//       matchPairs: [{ left: '', right: '' }],
//       correctAnswerText: '',
//       mapImageBase64: '',
//     };
//   }

//   addOption() {
//     this.form.options.push('');
//   }

//   removeOption(i: number) {
//     if (this.form.options.length > 1) this.form.options.splice(i, 1);
//   }

//   addMatchPair() {
//     this.form.matchPairs.push({ left: '', right: '' });
//   }

//   removeMatchPair(i: number) {
//     if (this.form.matchPairs.length > 1) this.form.matchPairs.splice(i, 1);
//   }

//   onMapUpload(event: any) {
//     const file = event.target.files?.[0];
//     if (!file) return;

//     const reader = new FileReader();
//     reader.onload = () => {
//       this.form.mapImageBase64 = reader.result as string;
//     };
//     reader.readAsDataURL(file);
//   }

//   saveQuestion() {
//     const payload = {
//       questionText: this.form.questionText,
//       questionType: this.form.questionType,
//       options: this.form.options,
//       correctAnswer: this.form.correctAnswer,
//       matchPairs: this.form.matchPairs,
//       correctAnswerText: this.form.correctAnswerText,
//       mapImageBase64: this.form.mapImageBase64,
//     };

//     if (this.form.id) {
    
//       this.http
//         .put(`http://localhost:8000/questions/${this.form.id}`, payload)
//         .subscribe(() => {
//           alert('Question updated');
//           this.closePanel();
//         });
//     } else {
  
//       this.http.post('http://localhost:8000/questions', payload).subscribe(() => {
//         alert('Question created');
//         this.closePanel();
//       });
//     }
//   }
// }

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-custom-fields',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './custom-fields.component.html',
  styleUrls: ['./custom-fields.component.css']
})
export class CustomFieldsComponent {

  /* =====================
     STATE
  ===================== */

  searchText = '';
  questions: any[] = [];
  showAddPanel = false;
  editingQuestion: any | null = null;

  /* =====================
     FORM MODEL
  ===================== */

  form = this.emptyForm();

  constructor(private http: HttpClient) {
    this.loadQuestions();
  }

  /* =====================
     API
  ===================== */

  loadQuestions() {
    this.http.get<any>('http://localhost:8000/customfields').subscribe(res => {
      this.questions = res?.questions ?? [];
    });
  }

  /* =====================
     SEARCH FILTER
  ===================== */

  get filteredQuestions() {
    const t = this.searchText.trim().toLowerCase();
    if (!t) return this.questions;

    return this.questions.filter(q =>
      (q.question_text ?? '').toLowerCase().includes(t)
    );
  }

  /* =====================
     MODAL CONTROLS
  ===================== */

  openAddPanel() {
    this.editingQuestion = null;
    this.form = this.emptyForm();
    this.showAddPanel = true;
  }

  openEditPanel(q: any) {
    this.editingQuestion = q;
    this.showAddPanel = true;

    this.form.id = q.id;
    this.form.questionText = q.question_text ?? '';
    this.form.questionType = q.question_type ?? 'choose';

    // Parse answer_data
    try {
      const ans =
        typeof q.answer_data === 'string'
          ? JSON.parse(q.answer_data)
          : q.answer_data;

      if (ans) {
        this.form.options = Array.isArray(ans.options) ? ans.options : [''];
        this.form.correctAnswer = ans.correct ?? 0;
        this.form.matchPairs = Array.isArray(ans.matchPairs)
          ? ans.matchPairs
          : [{ left: '', right: '' }];
        this.form.correctAnswerText = ans.fillup_answer ?? '';
      }
    } catch {
      // ignore malformed JSON
    }

    this.form.mapImageBase64 = q.map_image ?? '';
  }

  closePanel() {
    this.showAddPanel = false;
    this.form = this.emptyForm();
    this.editingQuestion = null;
  }

  /* =====================
     CRUD
  ===================== */

  saveQuestion() {
    const payload = {
      questionText: this.form.questionText,
      questionType: this.form.questionType,
      options: this.form.options,
      correctAnswer: this.form.correctAnswer,
      matchPairs: this.form.matchPairs,
      correctAnswerText: this.form.correctAnswerText,
      mapImageBase64: this.form.mapImageBase64,
    };

    if (this.form.id) {
      // UPDATE
      this.http
        .put(`http://localhost:8000/questions/${this.form.id}`, payload)
        .subscribe(() => {
          alert('Question updated');
          this.closePanel();
          this.loadQuestions();
        });
    } else {
      // CREATE
      this.http
        .post('http://localhost:8000/questions', payload)
        .subscribe(() => {
          alert('Question created');
          this.closePanel();
          this.loadQuestions();
        });
    }
  }

  deleteQuestion(id: number) {
    if (!confirm('Are you sure you want to delete this question?')) return;

    this.http
      .delete(`http://localhost:8000/questions/${id}`)
      .subscribe(() => this.loadQuestions());
  }

  /* =====================
     FORM HELPERS
  ===================== */

  emptyForm() {
    return {
      id: null,
      questionText: '',
      questionType: 'choose',

      options: ['', ''],
      correctAnswer: 0,

      matchPairs: [{ left: '', right: '' }],
      correctAnswerText: '',

      mapImageBase64: '',
    };
  }

  /* =====================
     CHOOSE (MCQ)
  ===================== */

  addOption() {
    this.form.options.push('');
  }

  removeOption(i: number) {
    if (this.form.options.length > 1) {
      this.form.options.splice(i, 1);
    }
  }

  /* =====================
     MATCH
  ===================== */

  addMatchPair() {
    this.form.matchPairs.push({ left: '', right: '' });
  }

  removeMatchPair(i: number) {
    if (this.form.matchPairs.length > 1) {
      this.form.matchPairs.splice(i, 1);
    }
  }

  /* =====================
     MAP IMAGE
  ===================== */

  onMapUpload(event: any) {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      this.form.mapImageBase64 = reader.result as string;
    };
    reader.readAsDataURL(file);
  }
}
