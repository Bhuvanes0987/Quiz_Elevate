// import { Component, OnInit } from '@angular/core';
// import { UserService } from '../../services/user.service';
// import { CommonModule } from '@angular/common';

// @Component({
//   selector: 'app-user',
//     standalone: true,
//   imports: [CommonModule],
//   templateUrl: './user.component.html',
//   styleUrls: ['./user.component.css']
// })
// export class UserComponent implements OnInit {

//   users: any[] = [];

//   // Search + Pagination
//   searchText: string = '';
//   page: number = 1;
//   limit: number = 10;

//   // Pagination info
//   totalUsers: number = 0;
//   totalPages: number = 0;
//   startRecord: number = 0;
//   endRecord: number = 0;

//   constructor(private userService: UserService) {}

//   ngOnInit(): void {
//     this.loadUsers();
//   }

//   // Load users
//   loadUsers(): void {
//     this.userService.getUsers(this.page, this.limit, this.searchText).subscribe((res: any) => {
//       this.users = res.data;
//       this.totalUsers = res.total;

//       this.totalPages = Math.ceil(this.totalUsers / this.limit);

//       this.startRecord = (this.page - 1) * this.limit + 1;
//       this.endRecord = Math.min(this.page * this.limit, this.totalUsers);
//     });
//   }

  // Page change
  // onPageChanged(newPage: number): void {
  //   this.page = newPage;
  //   this.loadUsers();
  // }

  // // Rows per page change
  // onLimitChange(): void {
  //   this.page = 1;
  //   this.loadUsers();
  // }
// }


import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-user',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  users: any[] = [];
  filteredUsers: any[] = [];

  // Search text if needed
  searchText: string = '';

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  // Load all users
  loadUsers(): void {
    this.userService.getUsers().subscribe((res: any) => {
      // Assuming your backend returns an array directly
      this.users = res; 
      this.filteredUsers = res;
      // If your backend returns { data: [...], total: ... }, use:
      // this.users = res.data;
    });
  }
   filterUsers(): void {
    const search = this.searchText.toLowerCase();

    this.filteredUsers = this.users.filter(user =>
      (user.name?.toLowerCase().includes(search)) ||
      (user.email?.toLowerCase().includes(search)) ||
      (user.phone?.toLowerCase().includes(search)) ||
      (user.position?.toLowerCase().includes(search)) ||
      (user.student_Class?.toLowerCase().includes(search)) ||
      (user.school_name?.toLowerCase().includes(search)) ||
      (user.school_code?.toLowerCase().includes(search))
    );
  }
  // Soft delete a user
deleteUser(userId: number): void {
  if (confirm("Are you sure you want to delete this user?")) {
    this.userService.softDeleteUser(userId).subscribe({
      next: (res) => {
        alert("User deleted successfully!");
        this.loadUsers(); // refresh list
      },
      error: (err) => {
        console.error(err);
        alert("Error deleting user.");
      }
    });
  }
}

// Optional: edit function placeholder
editUser(user: any): void {
  // Implement your edit modal or navigation here
  console.log("Edit user", user);
}


}
