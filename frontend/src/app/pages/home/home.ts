import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.html',
  styleUrls: ['./home.css'],
})
export class HomeComponent {

  userInitials: string = "AB";

  // ✅ Added Router in constructor
  constructor(private router: Router) {}

  // ✅ Added goTo() function for navbar click routing
  goTo(path: string) {
    this.router.navigate([path]);
  }
}
