import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user',
    standalone: true,
  imports: [CommonModule],
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {

  users: any[] = [];

  // Search + Pagination
  searchText: string = '';
  page: number = 1;
  limit: number = 10;

  // Pagination info
  totalUsers: number = 0;
  totalPages: number = 0;
  startRecord: number = 0;
  endRecord: number = 0;

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  // Load users
  loadUsers(): void {
    this.userService.getUsers(this.page, this.limit, this.searchText).subscribe((res: any) => {
      this.users = res.data;
      this.totalUsers = res.total;

      this.totalPages = Math.ceil(this.totalUsers / this.limit);

      this.startRecord = (this.page - 1) * this.limit + 1;
      this.endRecord = Math.min(this.page * this.limit, this.totalUsers);
    });
  }

  // Page change
  onPageChanged(newPage: number): void {
    this.page = newPage;
    this.loadUsers();
  }

  // Rows per page change
  onLimitChange(): void {
    this.page = 1;
    this.loadUsers();
  }
}
