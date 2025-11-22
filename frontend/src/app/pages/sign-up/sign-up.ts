// import { Component } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
// import { NgForm } from '@angular/forms';
// import { FormsModule } from '@angular/forms';
// import { CommonModule } from '@angular/common';

// @Component({
//   selector: 'app-signup',
//   standalone: true,
//   imports: [CommonModule, FormsModule],
//   templateUrl: './sign-up.html',
//   styleUrls: ['./sign-up.css']
// })
// export class SignupComponent {

//   user = {
//     name: '',
//     schoolname: '',
//     schoolcode: '',
//     email: '',
//     password: '',
//     confirmPassword: ''
//   };

//   constructor(private http: HttpClient) {}

//   onSubmit(form?: NgForm) {

//     // Validate passwords
//     if (this.user.password !== this.user.confirmPassword) {
//       alert('Passwords do not match!');
//       return;
//     }

//     // POST request to Flask backend
//     this.http.post('http://127.0.0.1:8000/api/signup', {
//       name: this.user.name,
//       schoolname: this.user.schoolname,
//       schoolcode: this.user.schoolcode,
//       email: this.user.email,
//       password: this.user.password
//     }).subscribe({
//       next: (res: any) => {
//         alert(res.message);
//         form?.reset();
//       },
//       error: (err) => {
//         alert(err.error?.message || 'Something went wrong. Please try again.');
//       }
//     });
//   }
// }


import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgForm } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './sign-up.html',
  styleUrls: ['./sign-up.css']
})
export class SignupComponent {

  user = {
    name: '',
    studentClass: '',
    schoolname: '',
    schoolcode: '',
    email: '',
    password: '',
    confirmPassword: ''
  };

  constructor(private http: HttpClient, private router: Router) {}

  onSubmit(form?: NgForm) {

    if (!form?.valid) {
      alert("Please fill all required fields.");
      return;
    }

    if (this.user.password !== this.user.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    const signupData = {
      name: this.user.name,
      studentClass: this.user.studentClass,
      schoolname: this.user.schoolname,
      schoolcode: this.user.schoolcode,
      email: this.user.email,
      password: this.user.password
    };

    this.http.post('http://127.0.0.1:8000/api/signup', signupData).subscribe({
        next: (res: any) => {
          alert(res.message);

          form?.resetForm();  // 🔥 better than reset()

          // Redirect to login page
          this.router.navigate(['/']);
        },
        error: (err) => {
          console.error(err);
          alert(err.error?.message || 'Something went wrong. Please try again.');
        }
      });
  }
}
