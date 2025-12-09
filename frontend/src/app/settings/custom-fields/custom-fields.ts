import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-custom-fields',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './custom-fields.html',
  styleUrls: ['./custom-fields.css'],
})
export class CustomFieldsComponent {
  searchText = '';
  questions: any[] = [];
  showAddPanel = false;
  editingQuestion: any | null = null; // hold question object while editing

  // form model for add/edit inside panel
  form: any = {
    id: null,
    class: '',
    subject: '',
    unit: '',
    questionText: '',
    questionType: 'choose',
    options: ['', '', '', ''],
    correctAnswer: 0,
    matchPairs: [{ left: '', right: '' }],
    correctAnswerText: '',
    mapImageBase64: '',
  };

  constructor(private http: HttpClient) {
    this.loadQuestions();
  }

  // load all questions
  loadQuestions() {
    this.http.get('http://localhost:8000/questions').subscribe((res: any) => {
      this.questions = res?.questions ?? [];
    });
  }

  // computed filtered list (used in template)
  get filteredQuestions() {
    const t = this.searchText?.trim().toLowerCase() ?? '';
    if (!t) return this.questions;
    return this.questions.filter((q) =>
      (q.question_text ?? '')
        .toString()
        .toLowerCase()
        .includes(t)
    );
  }

  // open panel to add new question
  openAddPanel() {
    this.resetForm();
    this.showAddPanel = true;
    this.editingQuestion = null;
  }

  // open panel to edit existing question
  openEditPanel(q: any) {
    this.editingQuestion = q;
    this.showAddPanel = true;
    // populate form from q (mapping existing fields)
    this.form.id = q.id;
    this.form.class = q.class ?? '';
    this.form.subject = q.subject ?? '';
    this.form.unit = q.unit ?? '';
    this.form.questionText = q.question_text ?? '';
    this.form.questionType = q.question_type ?? 'choose';

    // try to parse answer_data if JSON
    try {
      const ans = typeof q.answer_data === 'string' ? JSON.parse(q.answer_data) : q.answer_data;
      if (ans) {
        if (Array.isArray(ans.options)) this.form.options = ans.options;
        if (ans.correct !== undefined) this.form.correctAnswer = ans.correct;
        if (Array.isArray(ans.matchPairs) && ans.matchPairs.length) this.form.matchPairs = ans.matchPairs;
        if (ans.fillup_answer !== undefined) this.form.correctAnswerText = ans.fillup_answer;
      }
    } catch (e) {
      // ignore parse errors
    }

    // map image
    if (q.map_image) {
      this.form.mapImageBase64 = q.map_image;
    }
  }

  closePanel() {
    this.showAddPanel = false;
    this.resetForm();
    this.editingQuestion = null;
    this.loadQuestions();
  }

  deleteQuestion(id: number) {
    if (!confirm('Are you sure you want to delete this question?')) return;
    this.http.delete(`http://localhost:8000/questions/${id}`).subscribe(() => {
      this.loadQuestions();
    });
  }

  // form helpers
  resetForm() {
    this.form = {
      id: null,
      class: '',
      subject: '',
      unit: '',
      questionText: '',
      questionType: 'choose',
      options: ['', '', '', ''],
      correctAnswer: 0,
      matchPairs: [{ left: '', right: '' }],
      correctAnswerText: '',
      mapImageBase64: '',
    };
  }

  addOption() {
    this.form.options.push('');
  }

  removeOption(i: number) {
    if (this.form.options.length > 1) this.form.options.splice(i, 1);
  }

  addMatchPair() {
    this.form.matchPairs.push({ left: '', right: '' });
  }

  removeMatchPair(i: number) {
    if (this.form.matchPairs.length > 1) this.form.matchPairs.splice(i, 1);
  }

  onMapUpload(event: any) {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      this.form.mapImageBase64 = reader.result as string;
    };
    reader.readAsDataURL(file);
  }

  // Save (create or update)
  saveQuestion() {
    const payload: any = {
      class: this.form.class,
      subject: this.form.subject,
      unit: this.form.unit,
      questionText: this.form.questionText,
      questionType: this.form.questionType,
      options: this.form.options,
      correctAnswer: this.form.correctAnswer,
      matchPairs: this.form.matchPairs,
      correctAnswerText: this.form.correctAnswerText,
      mapImageBase64: this.form.mapImageBase64,
    };

    if (this.form.id) {
      // update
      this.http.put(`http://localhost:8000/questions/${this.form.id}`, payload).subscribe(() => {
        alert('Question updated');
        this.closePanel();
      });
    } else {
      // create
      this.http.post('http://localhost:8000/questions', payload).subscribe(() => {
        alert('Question created');
        this.closePanel();
      });
    }
  }
}

