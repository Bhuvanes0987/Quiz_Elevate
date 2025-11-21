// import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
// import { Router } from '@angular/router';
// import { FormsModule } from '@angular/forms';

// @Component({
//   selector: 'app-login-page',
//   standalone: true,
//   imports: [FormsModule], 
//   templateUrl: './login.html',
//   styleUrls: ['./login.css'],
//    schemas: [CUSTOM_ELEMENTS_SCHEMA]  
// })
// export class LoginPage {

//   email: string = "";
//   password: string = "";

//   constructor(private http: HttpClient, private router: Router) {}

//   login() {
//     if (!this.email || !this.password) {
//       alert("Please enter both email and password");
//       return;
//     }

//     const credentials = {
//       email: this.email,
//       password: this.password
//     };

//     this.http.post('http://localhost:5000/login', credentials)
//       .subscribe({
//         next: (res: any) => {
//           console.log("Login Response:", res);

//           if (res && res.success === true) {
//             alert("Login Successful");

//             // save token if backend sends
//             if (res.token) {
//               localStorage.setItem('token', res.token);
//             }

//             this.router.navigate(['/dashboard']);
//           } else {
//             alert("Invalid email or password");
//           }
//         },
//         error: (error) => {
//           console.error("Login error:", error);
//           alert("Server error, try again.");
//         }
//       });
//   }
// }

// import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
// import { HttpClient } from '@angular/common/http';
// import { Router } from '@angular/router';
// import { FormsModule } from '@angular/forms';
// import { CommonModule } from '@angular/common';

// @Component({
//   selector: 'app-login-page',
//   standalone: true,
//   imports: [FormsModule, CommonModule],
//   templateUrl: './login.html',
//   styleUrls: ['./login.css'],
//   schemas: [CUSTOM_ELEMENTS_SCHEMA]
// })
// export class LoginPage {

//   email: string = "";
//   password: string = "";

//   constructor(private http: HttpClient, private router: Router) {}

//   login() {

//     if (!this.email || !this.password) {
//       alert("Please enter both email and password");
//       return;
//     }

//     const credentials = {
//       email: this.email,
//       password: this.password
//     };

//     console.log("🔄 Sending login request...", credentials);

//     this.http.post('http://127.0.0.1:8000/api/login', credentials)
//       .subscribe({
//         next: (res: any) => {
//           console.log("✅ Login Response:", res);

//           if (res.success) {
//             alert("Login Successful!");

//             // Save token if exists
//             if (res.token) {
//               localStorage.setItem("token", res.token);
//             }

//             // Redirect to dashboard
//             this.router.navigate(['/dashboard']);
//           } else {
//             alert(res.message || "Invalid email or password");
//           }
//         },

//         error: (error) => {
//           console.error("❌ Login error:", error);
//           alert(error.error?.message || "Server error, please try again.");
//         }
//       });
//   }
// }


import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [FormsModule, CommonModule, HttpClientModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css'],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class LoginPage {

  email: string = "";
  password: string = "";

  constructor(private http: HttpClient, private router: Router) {}

  login() {

    if (!this.email || !this.password) {
      alert("Please enter both email and password");
      return;
    }

    const credentials = {
      email: this.email,
      password: this.password
    };

    console.log("🔄 Sending login request...", credentials);

    this.http.post('http://127.0.0.1:8000/api/login', credentials)
      .subscribe({
        next: (res: any) => {
          console.log("✅ Login Response:", res);

          if (res.success) {
            alert("Login Successful!");

            // store token if returned
            if (res.token) {
              localStorage.setItem("token", res.token);
            }

            // Navigate to dashboard
            // this.router.navigate(['/dashboard']);
          } else {
            alert(res.message || "Invalid email or password");
          }
        },

        error: (error) => {
          console.error("❌ Login error:", error);
          alert(error.error?.message || "Server error. Please try again.");
        }
      });
  }
}
