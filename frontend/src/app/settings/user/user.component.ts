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
  selectedUser: any = null;
  isNewUser: boolean = false;


  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.loadUsers();
  }

loadUsers(): void {
  this.userService.getUsers().subscribe({
    next: (res: any) => {
      console.log('Users loaded:', res);  // check this output in console
      this.users = res;
      this.filteredUsers = res;
    },
    error: (err) => console.error('Error loading users', err)
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
   this.selectedUser = { ...user };
  console.log("Edit user", user);
}
openAddUserForm(): void {
  this.selectedUser = {
    name: '',
    email: '',
    phone: '',
    position: '',
    student_class: '',
    school_name: '',
    school_code: ''
  };
  this.isNewUser = true;
}

// Save user (create or update)
saveUser(): void {
  if (this.isNewUser) {
    this.userService.addUser(this.selectedUser).subscribe({
      next: (res) => {
        alert('User created successfully!');
        this.selectedUser = null;
        this.isNewUser = false;
        this.loadUsers(); // refresh list
      },
      error: (err) => {
        console.error(err);
        alert('Error creating user');
      }
    });
  } else {
    // update user
    this.userService.updateUser(this.selectedUser.id, this.selectedUser).subscribe({
      next: (res) => {
        alert('User updated successfully!');
        this.selectedUser = null;
        this.loadUsers();
      },
      error: (err) => {
        console.error(err);
        alert('Error updating user');
      }
    });
  }
}

// Cancel modal
cancelEdit(): void {
  this.selectedUser = null;
  this.isNewUser = false;
}

}
